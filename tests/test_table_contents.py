from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import pytest


class TableContentsTestCase(BaseTestCase):

    auth = None
    tableId = None

    @pytest.mark.run(order=1)
    def test_contents_setup(self):
        response = self.post('/user/login', {
            "email": "admin@polarapp.xyz",
            "password": "password"
        })
        data = response.get_json()
        self.__class__.auth = data['auth']
        self.assertEqual(response.status_code, 200)
        
        response = self.post('/table/create', {
            "auth": self.__class__.auth,
            "tableName": "Students",
            "columns": ["name", "major", "gpa"]
        })

        response = self.post('/table/all', {
            "auth": self.__class__.auth
        })
        data = response.get_json()
        for table in data:
            if table[1] == "Students":
                self.__class__.tableId = table[0]
        self.assertEqual(response.status_code, 200)
    

    def test_contents_add_view(self):
        response = self.post('/table/addEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "contents": ["Darwin", "CS", 4]
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/table/addEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "contents": ["Will", "CS", 4]
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/table/addEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "contents": ["Kunal", "CS", 4]
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/table/addEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "contents": ["Adam", "CS", 4]
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/table/view', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) >= 4)
        self.assertEqual(data[-1][1:], ["Adam", "CS", '4'])


    def test_contents_add_invalid(self):
        response = self.post('/table/addEntry', {
            "auth": self.__class__.auth,
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/table/addEntry', {
            "tableId": self.__class__.tableId
        })
        self.assertEqual(response.status_code, 401)

        response = self.post('/table/addEntry', {
            "auth": self.fake_user(),
            "tableId": self.__class__.tableId,
            "contents": ["Adam", "CS", 4]
        })
        self.assertEqual(response.status_code, 403)

        response = self.post('/table/addEntry', {
            "auth": self.__class__.auth,
            "tableId": "non_existent_table",
            "contents": ["Adam", "CS", 4]
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/table/addEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "contents": [4]
        })
        self.assertEqual(response.status_code, 400)


    def test_contents_modify(self):
        response = self.post('/table/view', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        rowcount = len(data)

        response = self.post('/table/modifyEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "contents": [1, "Sbeve", "Comm", 3]
        })
        self.assertEqual(response.status_code, 200)
        
        response = self.post('/table/view', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[1], [1, "Sbeve", "Comm", "3"])
        self.assertEqual(len(data), rowcount)


    def test_contents_modify_invalid(self):
        response = self.post('/table/modifyEntry', {
            "tableId": self.__class__.tableId,
        })
        self.assertEqual(response.status_code, 401)

        response = self.post('/table/modifyEntry', {
            "auth": self.fake_user(),
            "tableId": self.__class__.tableId,
            "contents": [0, "Sbeve", "Comm", 3]
        })
        self.assertEqual(response.status_code, 403)

        response = self.post('/table/modifyEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/table/modifyEntry', {
            "auth": self.__class__.auth,
            "tableId": "non_existent_table",
            "contents": [0, "Sbeve", "Comm", 3]
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/table/modifyEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "contents": [0, 3]
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/table/modifyEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "contents": [1000, "Sbeve", "Comm", 3]
        })
        self.assertEqual(response.status_code, 200)





    
