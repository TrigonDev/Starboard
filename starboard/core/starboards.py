# MIT License
#
# Copyright (c) 2022 TrigonDev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Awaitable, Sequence

import hikari
from apgorm import sql

from starboard.database import Guild, Message, SBMessage, Star, Starboard

from .config import StarboardConfig, get_config
from .messages import get_sbmsg_content
from .has_image import has_image

if TYPE_CHECKING:
    from starboard.bot import Bot


async def refresh_message(
    bot: Bot,
    orig_message: Message,
    sbids: Sequence[int] | None = None,
    force: bool = False,
    _nest: int = 0,
) -> None:
    if orig_message.id in bot.refresh_message_lock:
        if _nest >= 4:
            return
        await asyncio.sleep(5)
        return await refresh_message(
            bot, orig_message, sbids, force, _nest + 1
        )
    bot.refresh_message_lock.add(orig_message.id)
    try:
        await orig_message.refetch()
        if orig_message.trashed:
            await _handle_trashed_message(bot, orig_message)
        else:
            await _refresh_message(bot, orig_message, sbids, force)
    finally:
        bot.refresh_message_lock.remove(orig_message.id)


async def _handle_trashed_message(bot: Bot, orig_message: Message) -> None:
    starboards = {
        sb.id: sb
        for sb in await Starboard.fetch_query()
        .where(guild_id=orig_message.guild_id)
        .fetchmany()
    }
    for sid, sb in starboards.items():
        config = await get_config(sb, orig_message.channel_id)
        sbmsg = await SBMessage.exists(
            message_id=orig_message.id, starboard_id=sid
        )
        if not sbmsg or not sbmsg.sb_message_id:
            continue

        sbmsg_obj = await bot.cache.gof_message(
            sbmsg.starboard_id, sbmsg.sb_message_id
        )
        if not sbmsg_obj:
            continue

        await _edit(
            bot,
            config,
            sbmsg_obj,
            content=None,
            embeds=[
                hikari.Embed(
                    title="Trashed Message",
                    description="This message was trashed by a moderator.",
                )
            ],
            author_id=orig_message.author_id,
        )

    await asyncio.sleep(10)


async def _refresh_message(
    bot: Bot, orig_message: Message, sbids: Sequence[int] | None, force: bool
) -> None:
    if sbids:
        _s = (
            await Starboard.fetch_query()
            .where(Starboard.id.eq(sql(sbids).any))
            .fetchmany()
        )
    else:
        _s = (
            await Starboard.fetch_query()
            .where(guild_id=orig_message.guild_id)
            .fetchmany()
        )
    configs = [await get_config(s, orig_message.channel_id) for s in _s]

    tasks: list[asyncio.Task] = []
    for c in configs:
        t = asyncio.create_task(
            _refresh_message_for_starboard(bot, orig_message, c, force)
        )
        tasks.append(t)
    await asyncio.gather(*tasks)


async def _refresh_message_for_starboard(
    bot: Bot, orig_msg: Message, config: StarboardConfig, force: bool
) -> None:
    if orig_msg.is_nsfw:
        sbchannel = await bot.cache.gof_guild_channel_wnsfw(
            config.starboard.id
        )
        if sbchannel is None or sbchannel.is_nsfw is False:
            return

    orig_msg_obj = await bot.cache.gof_message(
        orig_msg.channel_id, orig_msg.id
    )

    starcount = await _get_star_count(orig_msg.id, config.starboard.id)
    action = _get_action(
        orig_msg, orig_msg_obj, config, starcount, orig_msg_obj is None
    )

    sbmsg = await SBMessage.exists(
        message_id=orig_msg.id, starboard_id=config.starboard.id
    )
    if (
        sbmsg is not None
        and sbmsg.last_known_star_count == starcount
        and not action.remove
        and not force
    ):
        return
    if not sbmsg:
        sbmsg = await SBMessage(
            message_id=orig_msg.id, starboard_id=config.starboard.id
        ).create()
    if sbmsg.sb_message_id is not None:
        sbmsg_obj = await bot.cache.gof_message(
            sbmsg.starboard_id, sbmsg.sb_message_id
        )
    else:
        sbmsg_obj = None

    if action.add and sbmsg_obj is None:
        if orig_msg_obj:
            content, embed, embeds = await get_sbmsg_content(
                bot, config, orig_msg_obj, orig_msg, starcount
            )
            assert embed
            guild = await Guild.fetch(id=orig_msg.guild_id)
            ip = guild.premium_end is not None
            sbmsg_obj = await _send(
                bot, config, content, [embed, *embeds], orig_msg.author_id, ip
            )
            if sbmsg_obj:
                sbmsg.sb_message_id = sbmsg_obj.id
                await sbmsg.save()
                if config.autoreact:
                    for emoji in config.star_emojis:
                        assert emoji
                        _emoji: hikari.UnicodeEmoji | hikari.CustomEmoji
                        try:
                            __emoji = bot.cache.get_emoji(int(emoji))
                            if __emoji is None:
                                continue
                            _emoji = __emoji
                        except ValueError:
                            _emoji = hikari.UnicodeEmoji.parse(emoji)
                        try:
                            await sbmsg_obj.add_reaction(_emoji)
                        except (
                            hikari.ForbiddenError,
                            hikari.BadRequestError,
                            hikari.NotFoundError,
                        ):
                            pass

    elif action.remove:
        if sbmsg_obj is not None:
            sbmsg.sb_message_id = None
            await _delete(bot, config, sbmsg_obj)

    elif sbmsg_obj is not None:
        # edit the message

        if orig_msg_obj:
            content, embed, embeds = await get_sbmsg_content(
                bot, config, orig_msg_obj, orig_msg, starcount
            )
            assert embed
            if config.link_edits:
                await _edit(
                    bot,
                    config,
                    sbmsg_obj,
                    content,
                    [embed, *embeds],
                    orig_msg.author_id,
                )
            else:
                await _edit(
                    bot, config, sbmsg_obj, content, None, orig_msg.author_id
                )
        else:
            content, _, _ = await get_sbmsg_content(
                bot, config, None, orig_msg, starcount
            )
            await _edit(
                bot, config, sbmsg_obj, content, None, orig_msg.author_id
            )

        await asyncio.sleep(10)

    else:
        sbmsg.sb_message_id = None

    sbmsg.last_known_star_count = starcount
    await sbmsg.save()


async def _edit(
    bot: Bot,
    config: StarboardConfig,
    message: hikari.Message,
    content: str | None,
    embeds: list[hikari.Embed] | None,
    author_id: int,
) -> None:
    if message.author.id != bot.me.id:
        wh = await _webhook(bot, config, False)
        if (not wh) or wh.webhook_id != message.author.id:
            return

        await wh.edit_message(
            message,
            content=content or hikari.UNDEFINED,
            embeds=embeds or hikari.UNDEFINED,
            user_mentions=(author_id,),
        )

    else:
        await message.edit(
            content=content or hikari.UNDEFINED,
            embeds=embeds or hikari.UNDEFINED,
            user_mentions=(author_id,),
        )


async def _delete(
    bot: Bot, config: StarboardConfig, message: hikari.Message
) -> None:
    if message.author.id == bot.me.id:
        return await message.delete()

    else:
        wh = await _webhook(bot, config, False)
        if wh is not None:
            await wh.delete_message(message)

        else:
            # try anyways. will work if bot has manage_messages
            try:
                await message.delete()
            except hikari.ForbiddenError:
                pass


async def _send(
    bot: Bot,
    config: StarboardConfig,
    content: str,
    embeds: list[hikari.Embed] | None,
    author_id: int,
    premium: bool,
) -> hikari.Message | None:
    webhook = await _webhook(bot, config)

    if webhook and config.use_webhook and premium:
        try:
            botuser = bot.get_me()
            assert botuser
            return await webhook.execute(
                content,
                embeds=embeds or hikari.UNDEFINED,
                username=config.webhook_name,
                avatar_url=(
                    config.webhook_avatar
                    or botuser.avatar_url
                    or botuser.default_avatar_url
                ),
                user_mentions=(author_id,),
            )
        except hikari.NotFoundError:
            pass

    try:
        return await bot.rest.create_message(
            config.starboard.id,
            content,
            embeds=embeds or hikari.UNDEFINED,
            user_mentions=(author_id,),
        )
    except (hikari.ForbiddenError, hikari.NotFoundError):
        return None


async def _webhook(
    bot: Bot, config: StarboardConfig, allow_create: bool = True
) -> hikari.ExecutableWebhook | None:
    create = allow_create and config.use_webhook
    wh = None
    if config.starboard.webhook_id is not None:
        wh = await bot.cache.gof_webhook(config.starboard.webhook_id)
        if not wh:
            config.starboard.webhook_id = None
            await config.starboard.save()

    if wh is not None:
        assert isinstance(wh, hikari.ExecutableWebhook)
        return wh

    if not create:
        return None

    try:
        wh = await bot.rest.create_webhook(
            config.starboard.id,
            name="Starboard Webhook",
            reason="This starboard has use_webhook set to True.",
        )
    except (hikari.ForbiddenError, hikari.NotFoundError):
        return None

    config.starboard.webhook_id = wh.id
    await config.starboard.save()

    return wh


def _get_star_count(orig_msg_id: int, starboard_id: int) -> Awaitable[int]:
    return (
        Star.fetch_query()
        .where(message_id=orig_msg_id, starboard_id=starboard_id)
        .count()
    )


@dataclass(order=True)
class _Actions:
    add: bool
    remove: bool


def _get_action(
    orig_msg: Message,
    orig_msg_obj: hikari.Message | None,
    config: StarboardConfig,
    points: int,
    deleted: bool,
) -> _Actions:
    add_trib: bool | None = None

    # check points
    if points >= config.required:
        add_trib = True
    elif points <= config.required_remove:
        add_trib = False

    # check deletion
    if deleted and config.link_deletes:
        add_trib = False

    # check image
    if orig_msg_obj and config.require_image and not has_image(orig_msg_obj):
        add_trib = False

    # check if frozen
    if orig_msg.frozen:
        add_trib = None

    # check if forced
    if config.starboard.id in orig_msg.forced_to:
        add_trib = True

    # return
    if add_trib is True:
        return _Actions(True, False)
    elif add_trib is None:
        return _Actions(False, False)
    else:
        return _Actions(False, True)
