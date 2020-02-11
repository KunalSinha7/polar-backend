from tests import BaseTestCase

import unittest as ut
import json



class UserTestCase(BaseTestCase):

    def test_register_phone(self):
        response = self.post('/user/register', dict(
            firstName="Test",
            lastName="User",
            phone="1234567890",
            email="abc@polarapp.xyz",
            password="password123"
        ))
        self.assertEqual(response.status_code, 200)

    def test_register_no_phone(self):
        response = self.post('/user/register', dict(
            firstName="Bob",
            lastName="User",
            email="bob@polarapp.xyz",
            password="password123"
        ))
        self.assertEqual(response.status_code, 200)

