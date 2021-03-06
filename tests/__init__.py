import os
import flaskapp
from flask import g
from flaskapp import app

import unittest as ut
import db


import sys
import json
import random
import string




class BaseTestCase(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        if 'run' not in app.config:
            db.util.setupTestDB()
            print('setup')
            app.config['run'] = True
        

    def setUp(self):
        self.app = flaskapp.app.test_client()
        self.app.TESTING = True
        app.config['TESTING'] = True
        

    def post(self, route, data, headers=None):
        if headers is not None:
            return self.app.post(route, data=json.dumps(data), content_type='application/json', headers=headers)
        else:
            return self.app.post(route, data=json.dumps(data), content_type='application/json')

    def make_auth_headers(self):
        return dict(
            Authorization=self.jwt
        )

    def auth_get(self, route):
        return self.app.get(route, headers=self.make_auth_headers())

    def auth_post(self, route, data=None):
        return self.post(route, data=data, headers=self.make_auth_headers())

    def fake_user(self):
        response = self.post('/user/register', dict(
            firstName = self.rand_string(10),
            lastName = self.rand_string(10),
            email = '{}@polarapp.com'.format(self.rand_string(5)),
            phone = self.rand_number(10),
            password = self.rand_string(20)
        ))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.jwt = data['auth']

        return data['auth']

    def fake_user_object(self):
        user = dict(
            firstName = self.rand_string(10),
            lastName = self.rand_string(10),
            email = '{}@polarapp.com'.format(self.rand_string(5)),
            phone = self.rand_number(10),
            password = self.rand_string(20)
        )

        response = self.post('/user/register', user)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        user['jwt'] = data['auth']

        return user


    def get_admin_user(self):
        response = self.post('/user/login', dict(
            email = 'admin@polarapp.xyz',
            password = 'password'
        ))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        return data['auth']

    def rand_string(self, size):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(size))

    def rand_number(self, size):
        return ''.join(random.choice(string.digits) for _ in range(size))

    def db_query(self, command, args):
        with app.app_context() as context:
            conn = db.conn()
            cursor = conn.cursor()
            cursor.execute(command, args)
            return cursor.fetchall()


if __name__ == "__main__":
    ut.main()
