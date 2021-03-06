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
from typing import TYPE_CHECKING, Any, Iterable, TypeVar

import crescent
import hikari

from starboard.core.config import StarboardConfig
from starboard.core.emojis import stored_to_emoji
from starboard.undefined import UNDEF
from starboard.utils import seconds_to_human

if TYPE_CHECKING:
    from starboard.bot import Bot


TRIBOOL = {"True": True, "False": False, "Default": None}
TRIBOOL_CHOICES = [(k, k) for k in TRIBOOL]


_T = TypeVar("_T")


def optiond(type: type[_T], *args, **kwargs) -> _T | UNDEF:
    return crescent.option(
        type, *args, **kwargs, default=UNDEF.UNDEF  # type: ignore
    )


@dataclass
class _PrettyConfig:
    general_style: str
    embed_style: str
    behavior: str
    requirements: str


def pretty_sb_config(
    config: StarboardConfig, bot: Bot, bold: Iterable[str] | None = None
) -> _PrettyConfig:
    b: set[str] = set(b.replace("_", "-") for b in bold) if bold else set()

    de = pretty_emoji_str(config.display_emoji, bot=bot)
    general_style = {
        "display-emoji": de,
        "ping-author": config.ping_author,
        "use-server-profile": config.use_server_profile,
        "extra-embeds": config.extra_embeds,
        "use-webhook": config.use_webhook,
    }

    embed_style = {
        "color": pretty_color(config.color),
        "jump-to-message": config.jump_to_message,
        "attachments-list": config.attachments_list,
        "replied-to": config.replied_to,
    }

    upvote_emojis = pretty_emoji_str(*config.upvote_emojis, bot=bot)
    downvote_emojis = pretty_emoji_str(*config.downvote_emojis, bot=bot)
    requirements = {
        "required": config.required,
        "required-remove": config.required_remove,
        "upvote-emojis": upvote_emojis,
        "downvote-emojis": downvote_emojis,
        "self-vote": config.self_vote,
        "allow-bots": config.allow_bots,
        "require-image": config.require_image,
        "older-than": seconds_to_human(config.older_than)
        if config.older_than
        else "disabled",
        "newer-than": seconds_to_human(config.newer_than)
        if config.newer_than
        else "disabled",
    }

    votes = config.cooldown_count
    secs = config.cooldown_period
    behavior = {
        "autoreact-upvote": config.autoreact_upvote,
        "autoreact-downvote": config.autoreact_downvote,
        "remove-invalid": config.remove_invalid,
        "link-deletes": config.link_deletes,
        "link-edits": config.link_edits,
        "private": config.private,
        "xp-multiplier": config.xp_multiplier,
        "enabled": config.enabled,
        "cooldown-enabled": config.cooldown_enabled,
        "cooldown": f"{votes} votes per {secs} seconds",
    }

    if "cooldown-period" in b or "cooldown-count" in b:
        b.add("cooldown")

    def gen(dct: dict[str, Any]) -> str:
        return "\n".join(
            (f"{k}: {v}" if k not in b else f"**{k}**: {v}")
            for k, v in dct.items()
        )

    return _PrettyConfig(
        general_style=gen(general_style),
        embed_style=gen(embed_style),
        behavior=gen(behavior),
        requirements=gen(requirements),
    )


def pretty_emoji_str(*emojis: str | None, bot: Bot) -> str:
    converted = ((stored_to_emoji(e, bot), e) for e in emojis if e is not None)

    out: list[str] = []
    for e, orig in converted:
        if isinstance(e, hikari.CustomEmoji):
            out.append(e.mention)
        elif e is None:
            out.append(f"Unknown Emoji {orig}")
        else:
            out.append(str(e))

    return ", ".join(out) or "none"


def pretty_color(color: int) -> str:
    return f"#{color:06X}"


def pretty_channel_str(bot: Bot, channels: Iterable[int]) -> str:
    mentions: list[str] = []
    for id in channels:
        obj = bot.cache.get_guild_channel(id)
        mentions.append(obj.mention if obj else f"Deleted Channel {id}")

    return ", ".join(mentions) or "none"
