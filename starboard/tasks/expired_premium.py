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
from datetime import datetime
from typing import TYPE_CHECKING

import pytz

from starboard.core.premium import try_autoredeem
from starboard.database import Guild

if TYPE_CHECKING:
    from starboard.bot import Bot


async def check_expired_premium(bot: Bot) -> None:
    while True:
        await _check_expired_premium(bot)
        await asyncio.sleep(60)


async def _check_expired_premium(bot) -> None:
    now = datetime.now(pytz.UTC)

    q = Guild.fetch_query()
    q.where(Guild.premium_end.is_null.not_)
    q.where(Guild.premium_end.lt(now))
    expired = await q.fetchmany()

    tasks = [
        asyncio.create_task(_check_for_server(bot, g, now)) for g in expired
    ]
    await asyncio.gather(*tasks, return_exceptions=True)


async def _check_for_server(bot: Bot, g: Guild, now: datetime) -> None:
    uid = await try_autoredeem(bot, g)
    if not uid:
        # NOTE: we do this to prevent the possibility that someone
        # redeemed premium between the original query (that fetched
        # expired guilds) and this query. We don't want any added
        # premium to disappear.
        await Guild.update_query().where(
            Guild.premium_end.lt(now), id=g.id
        ).set(premium_end=None).execute()

    # TODO: notify users