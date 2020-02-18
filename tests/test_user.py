from tests import BaseTestCase

import unittest as ut
import json

import sys
import pytest

class UserTestCase(BaseTestCase):

    @pytest.mark.run(order=1)
    def test_register_phone(self):
        response = self.post('/user/register', dict(
            firstName="Test",
            lastName="User",
            phone="1234567890",
            email="abc@polarapp.xyz",
            password="password123"
        ))
        self.assertEqual(response.status_code, 200)

    @pytest.mark.run(order=3)
    def test_a(self):
        assert True

    @pytest.mark.run(order=2)
    def test_register_no_phone(self):
        response = self.post('/user/register', dict(
            firstName="Bob",
            lastName="User",
            email="bob@polarapp.xyz",
            password="password123"
        ))
        self.assertEqual(response.status_code, 200)
    
    def test_login_register(self):
        response = self.post('/user/register', {
            "email": "test@polarapp.xyz",
            "firstName": "Waddle",
            "lastName": "Dee",
            "password": "something"
        })
        self.assertIn("auth", response.get_json())
    
    def test_login(self):
        response = self.post('/user/login', {
            "email": "test@polarapp.xyz",
            "password": "something",
        })
        print(response.get_json())
        self.assertIn("auth", response.get_json())
    
    def test_login_wrong_password(self):
        response = self.post('/user/login', {
            "email": "test@polarapp.xyz",
            "password": "somethig",
        })
        self.assertEqual(response.status_code, 400)
    
    def test_login_wrong_info(self):
        response = self.post('/user/login', {
            "email": "test@app.xyz",
            "password": "somethig",
        })
        self.assertEqual(response.status_code, 400)
    
    def test_login_missing_info(self):
        response = self.post('/user/login', {})
        self.assertEqual(response.status_code, 400)