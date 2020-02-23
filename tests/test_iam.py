from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import db

import sys
import pytest
import time

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


    @pytest.mark.run(order=10)
    def test_iam_revoke_auth(self):
        response = self.post('/iam/revokeRole', {
            "auth": self.__class__.auth,
            "roleId": 1,
            "userId": 2
        })
        self.assertEqual(response.status_code, 200)


    def test_iam_revoke_unauth(self):
        response = self.post('/iam/revokeRole', {
            "auth": self.__class__.unauth,
            "roleId": 1,
            "userId": 2
        })
        self.assertEqual(response.status_code, 403)


    def test_iam_revoke_missing(self):
        response = self.post('/iam/revokeRole', {
            "auth": self.__class__.auth,
            "roleId": 1
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/iam/revokeRole', {
            "auth": self.__class__.auth,
            "userId": 2
        })
        self.assertEqual(response.status_code, 400)


    def test_iam_revoke_invalid(self):
        response = self.post('/iam/revokeRole', {
            "auth": self.__class__.auth,
            "roleId": 20,
            "userId": 2
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/iam/revokeRole', {
            "auth": self.__class__.auth,
            "roleId": 2,
            "userId": 220
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/iam/revokeRole', {
            "auth": self.__class__.auth,
            "roleId": 1,
            "userId": 2
        })
        self.assertEqual(response.status_code, 200)



class IAMManagementTestCase(BaseTestCase):

    def make_role(self, jwt, name, perms):
        response = self.post('/iam/createRole', {
            'auth': jwt,
            'roleName': name,
            'permissions': perms
        })
        self.assertEqual(response.status_code, 200)

    def add_to_role(self, jwt, user, role):
        response = self.post('/iam/assignRole', {
            'auth': self.__class__.auth,
            'roleId': 1,
            'userId': 2
        })
        self.assertEqual(response.status_code, 200)

    def test_iam_get_roles_no_auth(self):
        response = self.post('/iam/getRoles', {})
        self.assertEqual(response.status_code, 401)

    def test_iam_get_roles_bad_auth(self):
        user = self.fake_user()
        response = self.post('/iam/getRoles', {
            'auth':user
        })
        self.assertEqual(response.status_code, 403)

    def test_iam_get_roles_one(self):
        admin_user_jwt = self.get_admin_user()
        role_name = 'vol'
        perms = [1, 4, 5, 11]

        self.__class__.make_role(self, admin_user_jwt, role_name, perms)
        response = self.post('/iam/getRoles', {
            'auth':admin_user_jwt
        })
        data = response.get_json()

        for row in data:
            if row['roleName'] == role_name and row['permissions'] == perms:
                self.assertTrue

        self.assertFalse


    def test_iam_get_roles_mult(self):
        admin_user_jwt = self.get_admin_user()
        role_name_one = 'brass'
        role_name_two = 'percussion'

        perms_one = [1,5,7]
        perms_two = [2,5,7]

        self.__class__.make_role(self, admin_user_jwt, role_name_one, perms_one)
        self.__class__.make_role(self, admin_user_jwt, role_name_two, perms_two)

        response = self.post('/iam/getRoles', {
            'auth':admin_user_jwt
        })    

        data = response.get_json()
        count = 0

        for row in data:
            if row['roleName'] == role_name_one and row['permissions'] == perms_one:
                count += 1

            if row['roleName'] == role_name_two and row['permissions'] == perms_two:
                count += 1

        if count >= 2:
            self.assertTrue
        else:
            self.assertFalse