from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import db

import sys
import pytest

class RegisterTestCase(BaseTestCase):

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