
from tests import BaseTestCase

import unittest as ut


class BasicTestCase(BaseTestCase):
    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello', str(response.data))