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

from pycooldown import FixedCooldown

from starboard.config import CONFIG
from starboard.database import Member, Starboard, Vote

REFRESH_XP_COOLDOWN: FixedCooldown[tuple[int, int]] = FixedCooldown(
    CONFIG.refresh_xp_period, CONFIG.refresh_xp_cap
)


async def refresh_xp(guild_id: int, user_id: int) -> bool | None:
    if REFRESH_XP_COOLDOWN.update_ratelimit((guild_id, user_id)) is not None:
        return False

    member = await Member.exists(guild_id=guild_id, user_id=user_id)
    if not member:
        return None

    starboards = (
        await Starboard.fetch_query().where(guild_id=guild_id).fetchmany()
    )
    member.xp = sum(
        [
            (await _count_votes(sb, user_id)) * sb.xp_multiplier
            for sb in starboards
        ]
    )
    await member.save()
    return True


async def _count_votes(starboard: Starboard, user_id: int) -> int:
    upvotes = await Vote.count(
        starboard_id=starboard.id, target_author_id=user_id, is_downvote=False
    )
    downvotes = await Vote.count(
        starboard_id=starboard.id, target_author_id=user_id, is_downvote=True
    )
    return upvotes - downvotes


async def get_leaderboard(
    guild_id: int, limit: int = CONFIG.leaderboard_length
) -> dict[int, MemberStats]:
    q = Member.fetch_query()
    q.where(guild_id=guild_id)
    q.where(Member.xp.gt(0))
    q.order_by(Member.xp, reverse=True)
    ret = await q.fetchmany(limit=limit)

    return {
        m.user_id: MemberStats(round(m.xp, 2), x + 1)
        for x, m in enumerate(ret)
    }


@dataclass
class MemberStats:
    xp: float
    rank: int
