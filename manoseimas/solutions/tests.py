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

import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from sboard.tests import NodesTestsMixin

from manoseimas.votings.models import Voting
from manoseimas.votings.tests import load_fixtures


class SolutionTests(NodesTestsMixin, TestCase):
    def testSolutions(self):
        db = Voting.get_db()
        load_fixtures(db)

        self._login_superuser()

        # Create new solution
        response = self._create('solution', title='S1', _f=('body',))
        self.assertRedirects(response, reverse('node', args=['~']))


        # Visit voting page
        v1_id = '16aa1e75-a5fb-4233-9213-4ddcc0380fe5'
        v1_url = reverse('node', args=[v1_id])
        response = self.client.get(v1_url)
        self.assertEqual(response.status_code, 200)


        # Link voting to solution
        v1_link_url = reverse('node', args=[v1_id, 'link-solution'])
        response = self.client.post(v1_link_url, {
            'solution': 's1',
            'position': '-1',
        })
        self.assertRedirects(response, v1_url)


        # Link voting to solution
        v2_id = '7b2427c4-4304-4230-a284-f63a126f8e5d'
        v2_url = reverse('node', args=[v2_id])
        v2_link_url = reverse('node', args=[v2_id, 'link-solution'])
        response = self.client.post(v2_link_url, {
            'solution': 's1',
            'position': '-3',
        })
        self.assertRedirects(response, v2_url)


        # Try to get user voting match results
        results_url = reverse('node', args=['s1', 'quick-results'])
        response = self.client.get(results_url, {'vote': '2'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['mps'][0]['id'], '000078')
        self.assertEqual(data['mps'][0]['score'], 87)
