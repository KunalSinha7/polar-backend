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

    def test_contents_remove(self):
        response = self.post('/table/view', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        rowcount = len(data)

        response = self.post('/table/removeEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "id": rowcount - 1
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/table/view', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(rowcount, len(data) + 1)

    def test_contents_remove_invalid(self):
        response = self.post('/table/removeEntry', {
            "tableId": self.__class__.tableId
        })
        self.assertEqual(response.status_code, 401)

        response = self.post('/table/removeEntry', {
            "auth": self.fake_user(),
        })
        self.assertEqual(response.status_code, 403)

        response = self.post('/table/removeEntry', {
            "auth": self.__class__.auth,
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/table/removeEntry', {
            "auth": self.__class__.auth,
            "tableId": "non_existent_table",
            "id": 1
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/table/removeEntry', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
            "id": 1000
        })
        self.assertEqual(response.status_code, 200)

    def test_contents_view(self):
        response = self.post('/table/view', {
            "auth": self.__class__.auth,
            "tableId": self.__class__.tableId,
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) >= 3)
        self.assertEqual(data[0], ["id", "name", "major", "gpa"])
        self.assertEqual(len(data[1]), 4)

    def test_contents_view_invalid(self):
        response = self.post('/table/view', {
            "auth": self.__class__.auth,
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/table/view', {
            "auth": self.fake_user(),
            "tableId": self.__class__.tableId,
        })
        self.assertEqual(response.status_code, 403)

        response = self.post('/table/view', {
            "tableId": self.__class__.tableId
        })
        self.assertEqual(response.status_code, 401)

        response = self.post('/table/view', {
            "auth": self.__class__.auth,
            "tableId": "non_existent_table",
        })
        self.assertEqual(response.status_code, 400)


class TableTestCase(BaseTestCase):

    def test_all_tables_noauth(self):
        response = self.post('/table/all', {})
        self.assertEqual(response.status_code, 401)

    def test_create_table(self):
        response = self.post('/table/create', {})
        self.assertEqual(response.status_code, 401)

        response = self.post('table/create', {
            "auth": self.get_admin_user()
        })

        self.assertEqual(response.status_code, 400)

        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": "my table name",
            "columns": ["col 1", 'col 2', 'col 3']
        })

        self.assertEqual(response.status_code, 200)

    def test_create_table_duplicate(self):
        table_name = self.rand_string(10)

        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": table_name,
            "columns": [self.rand_string(10), self.rand_string(20), self.rand_string(30)]
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": table_name,
            "columns": [self.rand_string(10), self.rand_string(20), self.rand_string(30)]
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.get_json())

    def test_all_tables(self):
        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": self.rand_string(10),
            "columns": [self.rand_string(10), self.rand_string(20), self.rand_string(30)]
        })

        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": self.rand_string(10),
            "columns": [self.rand_string(10), self.rand_string(20), self.rand_string(30)]
        })

        response = self.post('/table/all', {
            "auth": self.get_admin_user()
        })

        print(response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.get_json()), 2)

    def test_delete_table(self):
        table_name = self.rand_string(50)

        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": table_name,
            "columns": [self.rand_string(10), self.rand_string(20), self.rand_string(30)]
        })

        response = self.post('/table/all', {
            "auth": self.get_admin_user()
        })

        data = response.get_json()

        table_id = -1
        for a in data:
            if a[1] == table_name:
                table_id = a[0]
                break

        if table_id == -1:
            assert False

        response = self.post('table/delete', {
            "auth": self.get_admin_user(),
            "tableId": table_id
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('/table/all', {
            "auth": self.get_admin_user()
        })

        data = response.get_json()

        table_id = -1
        for a in data:
            if a[1] == table_name:
                assert False

    def test_add_column(self):
        table_name = self.rand_string(50)
        col1 = self.rand_string(50)
        col2 = self.rand_string(50)

        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": table_name,
            "columns": [self.rand_string(10)]
        })

        response = self.post('/table/all', {
            "auth": self.get_admin_user()
        })

        data = response.get_json()

        table_id = -1
        for a in data:
            if a[1] == table_name:
                table_id = a[0]
                break

        if table_id == -1:
            assert False

        response = self.post('table/addColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "columnName": col1
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/addColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "columnName": col2
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/columns', {
            "auth": self.get_admin_user(),
            "tableId": table_id
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(col1, response.get_json())
        self.assertIn(col2, response.get_json())


    def test_delete_column(self):
        table_name = self.rand_string(50)
        col1 = self.rand_string(50)
        col2 = self.rand_string(50)

        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": table_name,
            "columns": [self.rand_string(10)]
        })

        response = self.post('/table/all', {
            "auth": self.get_admin_user()
        })

        data = response.get_json()

        table_id = -1
        for a in data:
            if a[1] == table_name:
                table_id = a[0]
                break

        if table_id == -1:
            assert False

        response = self.post('table/addColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "columnName": col1
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/addColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "columnName": col2
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/deleteColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "columnName": col1
        })

        self.assertEqual(response.status_code, 200)


        response = self.post('table/deleteColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "columnName": col2
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/columns', {
            "auth": self.get_admin_user(),
            "tableId": table_id
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(col1, response.get_json())
        self.assertNotIn(col2, response.get_json())


    def test_modify_column(self):
        table_name = self.rand_string(50)
        col1 = self.rand_string(50)
        col2 = self.rand_string(50)
        col_1_new = self.rand_string(50)
        col_2_new = self.rand_string(50)

        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": table_name,
            "columns": [self.rand_string(10)]
        })

        response = self.post('/table/all', {
            "auth": self.get_admin_user()
        })

        data = response.get_json()

        table_id = -1
        for a in data:
            if a[1] == table_name:
                table_id = a[0]
                break

        if table_id == -1:
            assert False

        response = self.post('table/addColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "columnName": col1
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/addColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "columnName": col2
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/columns', {
            "auth": self.get_admin_user(),
            "tableId": table_id
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(col1, response.get_json())
        self.assertIn(col2, response.get_json())

        response = self.post('table/modifyColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "originalColumn":col1,
            "newColumn":col_1_new
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/modifyColumn', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "originalColumn":col2,
            "newColumn":col_2_new
        })

        self.assertEqual(response.status_code, 200)

        response = self.post('table/columns', {
            "auth": self.get_admin_user(),
            "tableId": table_id
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(col_1_new, response.get_json())
        self.assertIn(col_2_new, response.get_json())



    def test_modify_table_name(self):
        table_name = self.rand_string(50)
        new_table_name = self.rand_string(60)


        response = self.post('table/create', {
            "auth": self.get_admin_user(),
            "tableName": table_name,
            "columns": [self.rand_string(10)]
        })

        response = self.post('/table/all', {
            "auth": self.get_admin_user()
        })

        data = response.get_json()

        table_id = -1
        for a in data:
            if a[1] == table_name:
                table_id = a[0]
                break

        if table_id == -1:
            assert False

        response = self.post('table/modifyTableName', {
            "auth": self.get_admin_user(),
            "tableId": table_id,
            "name": new_table_name
        })

        self.assertEqual(response.status_code,200)

        response = self.post('/table/all', {
            "auth": self.get_admin_user()
        })

        data = response.get_json()

        table_id = -1
        for a in data:
            if a[1] == new_table_name:
                table_id = a[0]
                break

        if table_id == -1:
            assert False
        else:
            assert True

