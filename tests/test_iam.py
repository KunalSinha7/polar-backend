from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import db

import sys
import pytest

class IAMTestCase(BaseTestCase):

    auth = None
    unauth = None

    @pytest.mark.run(order=1)
    def test_iam_create_unauth(self):
        self.fake_user()
        self.__class__.unauth = self.jwt
        response = self.post('/iam/createRole', {
            "auth": self.jwt,
            "roleName": "Veteran",
            "permissions": [1,2,3]
        })
        self.assertEqual(response.status_code, 403)
    

    @pytest.mark.run(order=2)
    def test_iam_create_login(self):
        response = self.post('/user/login', {
            "email": "admin@polarapp.xyz",
            "password": "password"
        })
        data = response.get_json()
        self.assertIn("auth", data)
        self.__class__.auth = data['auth']
        self.assertEqual(response.status_code, 200)


    @pytest.mark.run(order=3)
    def test_iam_create_auth(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Veteran",
            "permissions": [1,2,3]
        })
        self.assertEqual(response.status_code, 200)
    

    def test_iam_create_missing(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "permissions": [1,2,3]
        })
        self.assertEqual(response.status_code, 400)
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Volunteer"
        })
        self.assertEqual(response.status_code, 400)

    
    @pytest.mark.run(order=4)
    def test_iam_create_duplicate(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Veteran",
            "permissions": [1,2,3]
        })
        self.assertEqual(response.status_code, 400)
    

    def test_iam_create_invalid(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Volunteer",
            "permissions": [12,20,30]
        })
        self.assertEqual(response.status_code, 400)
    
    
    @pytest.mark.run(order=5)
    def test_iam_remove_unauth(self):
        response = self.post('/iam/removeRole', {
            "auth": self.__class__.unauth,
            "roleId": 1
        })
        self.assertEqual(response.status_code, 403)
    

    @pytest.mark.run(order=6)
    def test_iam_remove_auth(self):
        response = self.post('/iam/removeRole', {
            "auth": self.__class__.auth,
            "roleId": 2
        })
        self.assertEqual(response.status_code, 200)
    

    def test_iam_remove_invalid(self):
        response = self.post('/iam/removeRole', {
            "auth": self.__class__.auth,
            "roleId": 20
        })
        self.assertEqual(response.status_code, 200)
    

    def test_iam_remove_missing(self):
        response = self.post('/iam/removeRole', {
            "auth": self.__class__.auth
        })
        self.assertEqual(response.status_code, 400)
    

    @pytest.mark.run(order=7)
    def test_iam_assign_unauth(self):
        response = self.post('/iam/assignRole', {
            "auth": self.__class__.unauth
        })
        self.assertEqual(response.status_code, 403)
    

    @pytest.mark.run(order=8)
    def test_iam_assign_auth(self):
        response = self.post('/iam/assignRole', {
            "auth": self.__class__.auth,
            "roleId": 1,
            "userId": 2
        })
        self.assertEqual(response.status_code, 200)


    def test_iam_assign_missing(self):
        response = self.post('/iam/assignRole', {
            "auth": self.__class__.auth,
            "roleId": 1
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/iam/assignRole', {
            "auth": self.__class__.auth,
            "userId": 2
        })
        self.assertEqual(response.status_code, 400) 
    

    @pytest.mark.run(order=9)
    def test_iam_assign_duplicate(self):
        response = self.post('/iam/assignRole', {
            "auth": self.__class__.auth,
            "roleId": 1,
            "userId": 2
        })
        self.assertEqual(response.status_code, 400)


    def test_iam_assign_invalid(self):
        response = self.post('/iam/assignRole', {
            "auth": self.__class__.auth,
            "roleId": 11,
            "userId": 2
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/iam/assignRole', {
            "auth": self.__class__.auth,
            "roleId": 1,
            "userId": 202
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/iam/assignRole', {
            "auth": self.__class__.auth,
            "roleId": 112,
            "userId": 224
        })
        self.assertEqual(response.status_code, 400)

