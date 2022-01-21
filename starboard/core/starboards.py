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

from dataclasses import dataclass
from typing import TYPE_CHECKING, Awaitable

import hikari

from starboard.database import Message, SBMessage, Star, Starboard

from . import emojis
from .embed_message import embed_message

if TYPE_CHECKING:
    from starboard.bot import Bot


async def get_orig_message(message_id: int) -> Message | None:
    if sbm := await SBMessage.exists(sb_message_id=message_id):
        return await Message.fetch(id=sbm.message_id.v)

    if m := await Message.exists(id=message_id):
        return m

    return None


async def refresh_message(bot: Bot, orig_message: Message) -> None:
    if orig_message.id.v in bot.refresh_message_lock:
        return
    bot.refresh_message_lock.add(orig_message.id.v)
    try:
        await _refresh_message(bot, orig_message)
    finally:
        bot.refresh_message_lock.remove(orig_message.id.v)


async def _refresh_message(bot: Bot, orig_message: Message) -> None:
    starboards = (
        await Starboard.fetch_query()
        .where(guild_id=orig_message.guild_id.v)
        .fetchmany()
    )

    for sb in starboards:
        await _refresh_message_for_starboard(bot, orig_message, sb)


async def _refresh_message_for_starboard(
    bot: Bot, orig_msg: Message, starboard: Starboard
) -> None:
    starcount = await _get_star_count(orig_msg.id.v, starboard.id.v)
    action = _get_action(orig_msg, starboard, starcount)

    sbmsg = await SBMessage.exists(
        message_id=orig_msg.id.v,
        starboard_id=starboard.id.v,
    )
    if not sbmsg:
        sbmsg = await SBMessage(
            message_id=orig_msg.id.v, starboard_id=starboard.id.v
        ).create()
    if sbmsg.sb_message_id.v is not None:
        sbmsg_obj = await bot.cache.gof_message(
            sbmsg.starboard_id.v,
            sbmsg.sb_message_id.v,
        )
    else:
        sbmsg_obj = None

    if action.add and sbmsg_obj is None:
        orig_msg_obj = await bot.cache.gof_message(
            orig_msg.channel_id.v, orig_msg.id.v
        )
        if orig_msg_obj:
            content, embed = await embed_message(
                bot,
                orig_msg_obj,
                orig_msg.guild_id.v,
                starboard.color.v or bot.config.color,
                (
                    emojis.stored_to_emoji(starboard.display_emoji.v, bot)
                    if starboard.display_emoji.v is not None
                    else None
                ),
                starcount,
            )
            sbmsg_obj = await bot.rest.create_message(
                starboard.id.v, embed=embed, content=content
            )
            sbmsg.sb_message_id.v = sbmsg_obj.id
            await sbmsg.save()
            if starboard.autoreact.v:
                for emoji in starboard.star_emojis.v:
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
            sbmsg.sb_message_id.v = None
            await sbmsg_obj.delete()

    elif sbmsg_obj is not None:
        # edit the message

        orig_msg_obj = await bot.cache.gof_message(
            orig_msg.channel_id.v,
            orig_msg.id.v,
        )
        if orig_msg_obj:
            content, embed = await embed_message(
                bot,
                orig_msg_obj,
                orig_msg.guild_id.v,
                starboard.color.v or bot.config.color,
                (
                    emojis.stored_to_emoji(starboard.display_emoji.v, bot)
                    if starboard.display_emoji.v is not None
                    else None
                ),
                starcount,
            )
            await sbmsg_obj.edit(content=content, embed=embed)

    else:
        sbmsg.sb_message_id.v = None

    sbmsg.last_known_star_count.v = starcount
    await sbmsg.save()


def _get_star_count(orig_msg_id: int, starboard_id: int) -> Awaitable[int]:
    return (
        Star.fetch_query()
        .where(
            message_id=orig_msg_id,
            starboard_id=starboard_id,
        )
        .count()
    )


@dataclass(order=True)
class _Actions:
    add: bool
    remove: bool


def _get_action(
    orig_msg: Message, starboard: Starboard, points: int
) -> _Actions:
    add_trib: bool | None = None

    # check points
    if points >= starboard.required.v:
        add_trib = True
    elif points <= starboard.required_remove.v:
        add_trib = False

    # check if forced
    if starboard.id.v in orig_msg.forced_to.v:
        add_trib = True

    # check trashed
    if orig_msg.trashed.v:
        add_trib = False

    # return
    if add_trib is True:
        return _Actions(True, False)
    elif add_trib is None:
        return _Actions(False, False)
    else:
        return _Actions(False, True)