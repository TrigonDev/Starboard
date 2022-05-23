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

from .database import Database
from .models.aschannel import AutoStarChannel
from .models.guild import Guild, goc_guild
from .models.member import Member, goc_member
from .models.message import Message, goc_message
from .models.override import Override
from .models.permrole import PermRole, PermRoleStarboard
from .models.posrole import PosRole, PosRoleMember
from .models.sb_message import SBMessage
from .models.starboard import Starboard, validate_sb_changes
from .models.user import PatreonStatus, Patron, User, goc_patron, goc_user
from .models.vote import UpVote
from .models.xprole import XPRole

__all__ = (
    "Database",
    "AutoStarChannel",
    "Guild",
    "Member",
    "Message",
    "Override",
    "PermRole",
    "PermRoleStarboard",
    "PosRole",
    "PosRoleMember",
    "SBMessage",
    "UpVote",
    "Starboard",
    "User",
    "Patron",
    "PatreonStatus",
    "XPRole",
    "goc_guild",
    "goc_member",
    "goc_message",
    "goc_user",
    "goc_patron",
    "validate_sb_changes",
)
