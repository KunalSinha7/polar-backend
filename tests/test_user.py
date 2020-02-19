from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import db

import sys
import pytest

class UserTestCase(BaseTestCase):

    auth = None

    @pytest.mark.run(order=1)
    def test_register_phone(self):
        response = self.post('/user/register', dict(
            firstName='Test',
            lastName='User',
            phone='1234567890',
            email='abc@polarapp.xyz',
            password='password123'
        ))
        self.assertEqual(response.status_code, 200)

        with app.app_context() as context:
            data = response.get_json()
            user_id = auth.jwt.check_jwt(data['auth'])
            find_user = '''select * from Users where userId = %s;'''
            conn = db.conn()
            cursor = conn.cursor()

            cursor.execute(find_user, [user_id])
            user = cursor.fetchall()
            self.assertEqual(1, len(user))
            user = user[0]

            self.assertIn('Test', user)
            self.assertIn('User', user)
            self.assertIn('1234567890', user)
            self.assertIn('abc@polarapp.xyz', user)
            self.assertIn(auth.hash_password('password123', 'abc@polarapp.xyz'), user)


    def test_register_no_phone(self):
        response = self.post('/user/register', dict(
            firstName='Bob',
            lastName='User',
            email='bob@polarapp.xyz',
            password='password123'
        ))
        self.assertEqual(response.status_code, 200)

        with app.app_context() as context:
            data = response.get_json()
            user_id = auth.jwt.check_jwt(data['auth'])
            find_user = '''select * from Users where userId = %s;'''
            conn = db.conn()
            cursor = conn.cursor()

            cursor.execute(find_user, [user_id])
            user = cursor.fetchall()
            self.assertEqual(1, len(user))
            user = user[0]

            self.assertIn('Bob', user)
            self.assertIn('User', user)
            self.assertIn('bob@polarapp.xyz', user)
            self.assertIn(auth.hash_password('password123', 'bob@polarapp.xyz'), user)

    def test_register_no_name(self):
        response = self.post('/user/register', dict(
            email='bob@polarapp.xyz',
            password='password123'
        ))
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('firstName', data['message'])
        self.assertIn('lastName', data['message'])


    def test_register_no_email(self):
        response = self.post('/user/register', dict(
            firstName='Bob',
            lastName='User',
            password='password123'
        ))
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('email', data['message'])


    def test_register_no_password(self):
        response = self.post('/user/register', dict(
            firstName='Bob',
            lastName='User',
            email='bob@polarapp.xyz'
        ))
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('password', data['message'])
    
    @pytest.mark.run(order=4)
    def test_login_register(self):
        response = self.post('/user/register', {
            "email": "test@polarapp.xyz",
            "firstName": "Waddle",
            "lastName": "Dee",
            "password": "something"
        })
        self.assertIn("auth", response.get_json())
    
    @pytest.mark.run(order=5)
    def test_login(self):
        response = self.post('/user/login', {
            "email": "test@polarapp.xyz",
            "password": "something",
        })
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
        response = self.post('/user/login', {
            "email": "random@polarapp.xyz"
        })
        self.assertEqual(response.status_code, 400)
        response = self.post('/user/login', {
            "password": "12ytghrwerh"
        })
        self.assertEqual(response.status_code, 400)
    
    def test_info_unauth(self):
        response = self.post('/user/getInfo', {})
        self.assertEqual(response.status_code, 401)
        response = self.post('/user/setInfo', {})
        self.assertEqual(response.status_code, 401)
    
    @pytest.mark.run(order=6)
    def test_info_auth(self):
        response = self.post('/user/register', {
            "firstName": "Waddle",
            "lastName": "Doo",
            "email": "wade@polarapp.xyz",
            "password": "something"
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth', data)
        self.__class__.auth = data['auth']
        self.assertIn('permissions', data)
    
    @pytest.mark.run(order=7)
    def test_info_get(self):
        response = self.post('/user/getInfo', {
            "auth": self.__class__.auth
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['firstName'], "Waddle")
        self.assertEqual(data['lastName'], "Doo")
        self.assertEqual(data['email'], "wade@polarapp.xyz")
        self.assertIsNone(data['phone'])

    @pytest.mark.run(order=8)
    def test_info_set_missing(self):
        response = self.post('/user/setInfo', {
            "auth": self.__class__.auth
        })
        self.assertEqual(response.status_code, 400)

    @pytest.mark.run(order=9)
    def test_info_set_some(self):
        response = self.post('/user/setInfo', {
            "auth": self.__class__.auth,
            "firstName": "James",
            "phone": "1234567890"
        })
        self.assertEqual(response.status_code, 400)

    @pytest.mark.run(order=10)
    def test_info_set_all(self):
        response = self.post('/user/setInfo', {
            "auth": self.__class__.auth,
            "firstName": "James",
            "lastName": "Bond",
            "phone": None
        })
        self.assertEqual(response.status_code, 200)
