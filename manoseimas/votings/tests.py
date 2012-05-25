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

import os
import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from sboard.tests import NodesTestsMixin

from .models import Voting


def load_fixtures(db):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'fixtures', 'voting.json')) as f:
        db.save_docs(json.load(f))


class SearchTest(NodesTestsMixin, TestCase):
    def testSolutions(self):
        db = Voting.get_db()
        load_fixtures(db)

        search_url = reverse('search')
        response = self.client.get(search_url, {
            'q': 'http://www3.lrs.lt/pls/inter/w5_sale.bals?p_bals_id=-13013',
        })
        self.assertRedirects(response, reverse('node',
                args=['16aa1e75-a5fb-4233-9213-4ddcc0380fe5']))
