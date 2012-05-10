# Copyright (C) 2012  Mantas Zimnickas <sirexas@gmail.com>
#
# This file is part of manoseimas.lt project.
#
# manoseimas.lt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# manoseimas.lt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with manoseimas.lt.  If not, see <http://www.gnu.org/licenses/>.

from sboard.profiles.interfaces import IGroup
from sboard.profiles.interfaces import IProfile


class IMPProfile(IProfile): pass

class ICommission(IGroup): pass
class ICommittee(IGroup): pass
class IFraction(IGroup): pass
class IParliament(IGroup): pass
class IParliamentaryGroup(IGroup): pass
class IParty(IGroup): pass
class IPoliticalGroup(IGroup): pass