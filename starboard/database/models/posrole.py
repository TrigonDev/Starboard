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
from apgorm import types

from starboard.config import CONFIG

from ._converters import DecimalC
from ._validators import num_range
from .guild import Guild
from .user import User


class PosRole(apgorm.Model):
    __slots__: Iterable[str] = ()

    role_id = types.Numeric().field().with_converter(DecimalC)
    guild_id = types.Numeric().field().with_converter(DecimalC)
    max_members = types.Int().field()

    guild_id_fk = apgorm.ForeignKey(guild_id, Guild.guild_id)

    primary_key = (role_id,)

    max_members.add_validator(
        num_range("max-members", CONFIG.min_pr_members, CONFIG.max_pr_members)
    )


class PosRoleMember(apgorm.Model):
    __slots__: Iterable[str] = ()

    role_id = types.Numeric().field().with_converter(DecimalC)
    user_id = types.Numeric().field().with_converter(DecimalC)

    role_id_fk = apgorm.ForeignKey(role_id, PosRole.role_id)
    user_id_fk = apgorm.ForeignKey(user_id, User.user_id)

    primary_key = (role_id, user_id)
