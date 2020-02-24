from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt

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
            "permissions": [1, 2, 3]
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
            "permissions": [1, 2, 3]
        })
        self.assertEqual(response.status_code, 200)

    def test_iam_create_missing(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "permissions": [1, 2, 3]
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
            "permissions": [1, 2, 3]
        })
        self.assertEqual(response.status_code, 400)

    def test_iam_create_invalid(self):
        response = self.post('/iam/createRole', {
            "auth": self.__class__.auth,
            "roleName": "Volunteer",
            "permissions": [12, 20, 30]
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
            'auth': jwt,
            'roleId': role,
            'userId': user
        })
        self.assertEqual(response.status_code, 200)

    def test_iam_get_roles_no_auth(self):
        response = self.post('/iam/getRoles', {})
        self.assertEqual(response.status_code, 401)

    def test_iam_get_roles_bad_auth(self):
        user = self.fake_user()
        response = self.post('/iam/getRoles', {
            'auth': user
        })
        self.assertEqual(response.status_code, 403)

    def test_iam_get_roles_one(self):
        admin_user_jwt = self.get_admin_user()
        role_name = self.rand_string(10)
        perms = [1, 4, 5, 11]

        self.__class__.make_role(self, admin_user_jwt, role_name, perms)
        response = self.post('/iam/getRoles', {
            'auth': admin_user_jwt
        })
        data = response.get_json()

        for row in data:
            if row['roleName'] == role_name and row['permissions'] == perms:
                self.assertTrue

        self.assertFalse

    def test_iam_get_roles_mult(self):
        admin_user_jwt = self.get_admin_user()
        role_name_one = self.rand_string(5)
        role_name_two = self.rand_string(5)

        perms_one = [1, 5, 7]
        perms_two = [2, 5, 7]

        self.__class__.make_role(self, admin_user_jwt,
                                 role_name_one, perms_one)
        self.__class__.make_role(self, admin_user_jwt,
                                 role_name_two, perms_two)

        response = self.post('/iam/getRoles', {
            'auth': admin_user_jwt
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

    def test_iam_get_user_roles_one(self):
        admin_user_jwt = self.get_admin_user()
        role_name = self.rand_string(50)
        perms = [1, 4, 5, 11]

        self.__class__.make_role(self, admin_user_jwt, role_name, perms)
        response = self.post('/iam/getRoles', {
            'auth': admin_user_jwt
        })
        data = response.get_json()
        roleId = self.db_query(
            'select roleId from Roles where roleName = %s', [role_name])[0][0]

        user1 = self.fake_user_object()

        response = self.post('/iam/assignRole', {
            'auth': admin_user_jwt,
            'userId': auth.jwt.check_jwt(user1['jwt']),
            'roleId': roleId
        })

        response = self.post('/iam/getUserRoles', {
            'auth': admin_user_jwt
        })

        data = response.get_json()

        for row in data:
            if row['email'] == user1['email'] and \
                    row['firstName'] == user1['firstName'] and \
                    row['lastName'] == user1['lastName'] and \
                    row['phone'] == user1['phone'] \
                    and roleId in row['roles']:

                self.assertTrue

        self.assertFalse

    def test_iam_get_user_roles_mult(self):
        admin_user_jwt = self.get_admin_user()
        role_name = self.rand_string(50)
        role_name_2 = self.rand_string(50)
        perms = [1, 4, 5, 11]
        perms_2 = [2, 3, 6]

        self.__class__.make_role(self, admin_user_jwt, role_name, perms)
        self.__class__.make_role(self, admin_user_jwt, role_name_2, perms_2)
        response = self.post('/iam/getRoles', {
            'auth': admin_user_jwt
        })
        data = response.get_json()
        roleId = self.db_query(
            'select roleId from Roles where roleName = %s', [role_name])[0][0]

        roleId2 = self.db_query(
            'select roleId from Roles where roleName = %s', [role_name_2])[0][0]

        user1 = self.fake_user_object()

        response = self.post('/iam/assignRole', {
            'auth': admin_user_jwt,
            'userId': auth.jwt.check_jwt(user1['jwt']),
            'roleId': roleId
        })

        response = self.post('/iam/getUserRoles', {
            'auth': admin_user_jwt
        })

        data = response.get_json()

        for row in data:
            if row['email'] == user1['email'] and \
                    row['firstName'] == user1['firstName'] and \
                    row['lastName'] == user1['lastName'] and \
                    row['phone'] == user1['phone'] and \
                    roleId in row['roles'] and \
                    roleId2 in row['roles']:

                self.assertTrue

        self.assertFalse

    def test_iam_get_user_roles_bad(self):
        response = self.post('/iam/getUserRoles', {})
        self.assertEqual(response.status_code, 401)

    def test_iam_get_user_roles_noauth(self):
        user = self.fake_user_object()

        response = self.post('/iam/getUserRoles', {
            'auth': user['jwt']
        })
        self.assertEqual(response.status_code, 403)
