from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import db

import sys
import pytest


class MessageTestCase(BaseTestCase):

    def test_reset_password_full(self):
        user = self.fake_user_object()

        response = self.post('/user/forgotPassword', dict(
            email=user['email']
        ))
        user['id'] = auth.jwt.check_jwt(user['jwt'])

        with app.app_context() as context:
            sql_stmt = '''select link from Links where userId=%s;'''
            conn = db.conn()
            cursor = conn.cursor()
            cursor.execute(sql_stmt, [user['id']])
            token = cursor.fetchone()[0]

            response = self.post('/user/resetPassword', dict(
                email=user['email'],
                newPassword='blahblahblah',
                token=token
            ))

            self.assertEqual(response.status_code, 200)

            response = self.post('/user/login', dict(
                email=user['email'],
                password='blahblahblah'
            ))

            self.assertEqual(response.status_code, 200)
