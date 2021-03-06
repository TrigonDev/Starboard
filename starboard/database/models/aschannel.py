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

from typing import Iterable

import apgorm
from apgorm import Unique, types

from starboard.config import CONFIG
from starboard.exceptions import ASCNotFound

from ._converters import DecimalC, NonNullArray
from ._validators import num_range, str_len
from .guild import Guild


class AutoStarChannel(apgorm.Model):
    __slots__: Iterable[str] = ()

    id = types.Serial().field()
    name = types.Text().field()
    channel_id = types.Numeric().field().with_converter(DecimalC)
    guild_id = types.Numeric().field().with_converter(DecimalC)

    prem_locked = types.Boolean().field(default=False)

    emojis = (
        types.Array(types.Text())
        .field(default_factory=lambda: ["⭐"])
        .with_converter(NonNullArray(str))
    )
    min_chars = types.SmallInt().field(default=0)
    max_chars = types.SmallInt().nullablefield()
    require_image = types.Boolean().field(default=False)
    delete_invalid = types.Boolean().field(default=False)

    guild_id_fk = apgorm.ForeignKey(guild_id, Guild.guild_id)

    asc_guild_name_unique = Unique(guild_id, name)

    primary_key = (id,)

    # validators:
    min_chars.add_validator(num_range("min-chars", 0, CONFIG.max_minchars))
    max_chars.add_validator(num_range("max-chars", 0, CONFIG.max_maxchars))
    name.add_validator(
        str_len("name", CONFIG.min_asc_name, CONFIG.max_asc_name)
    )

    # methods
    @staticmethod
    async def from_name(guild_id: int, name: str) -> AutoStarChannel:
        if asc := await AutoStarChannel.exists(guild_id=guild_id, name=name):
            return asc
        else:
            raise ASCNotFound(name)
