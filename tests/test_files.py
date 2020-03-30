from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import pytest
import os
import boto3
import files.db as db
import time

class FilesTestCase(BaseTestCase):

    unauth = None
    auth = None
    
    @pytest.mark.run(order=1)
    def test_file_setup(self):
        self.__class__.unauth = self.fake_user()
        response = self.post('/user/login', {
            "email": "admin@polarapp.xyz",
            "password": "password"
        })
        data = response.get_json()
        self.__class__.auth = data['auth']
        self.assertEqual(response.status_code, 200)
    
    @pytest.mark.run(order=2)
    def test_file_upload(self):
        os.system("touch test.txt")
        os.system("echo hello > test.txt")
        file = open('test.txt', 'rb')
        
        data = {
            "store": "test.txt",
            "name": "test.txt",
            "desc": "upload unit test",
            "roles": [1],
            "userId": 1
        }

        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(file, 'polar-files', data['name'])

        with app.app_context() as context:
            db.upload(data)
        
        os.system("rm test.txt")
    
    @pytest.mark.run(order=2)
    def test_file_upload_diff_role(self):
        os.system("touch test.txt")
        os.system("echo hello > test.txt")
        file = open('test.txt', 'rb')
        
        data = {
            "store": "diff.txt",
            "name": "diff.txt",
            "desc": "upload unit test",
            "roles": [2],
            "userId": 1
        }

        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(file, 'polar-files', data['name'])

        with app.app_context() as context:
            db.upload(data)
        
        os.system("rm test.txt")

    @pytest.mark.run(order=2)
    def test_file_upload_no_roles(self):
        os.system("touch test.txt")
        os.system("echo hello > test.txt")
        file = open('test.txt', 'rb')
        
        data = {
            "store": "none.txt",
            "name": "none.txt",
            "desc": "upload unit test",
            "roles": [],
            "userId": 1
        }

        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(file, 'polar-files', data['name'])

        with app.app_context() as context:
            db.upload(data)
        
        os.system("rm test.txt")

    def test_file_upload_unauth(self):
        response = self.post('/files/upload', {
            "auth": self.__class__.unauth
        })
        self.assertEqual(response.status_code, 403)

    def test_file_view_unauth(self):
        response = self.post('/files/view', {
            "auth": self.__class__.unauth
        })
        self.assertEqual(response.status_code, 403)
        response = self.post('/files/view', {})
        self.assertEqual(response.status_code, 401)
    
    @pytest.mark.run(order=3)
    def test_file_view(self):
        response = self.post('/files/view', {
            "auth": self.__class__.auth
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(len(data[0]), 7)
        self.assertEqual(data[1][1], 'none.txt')
    
    @pytest.mark.run(order=3)
    def test_file_download(self):
        response = self.post('/files/download', {
            "auth": self.__class__.auth,
            "name": "test.txt"
        })
        self.assertEqual(response.status_code, 200)

    def test_file_download_unauth(self):
        response = self.post('/files/download', {
            "auth": self.__class__.unauth,
            "name": "test.txt"
        })
        self.assertEqual(response.status_code, 403)
        response = self.post('/files/download', {
            "name": "test.txt"
        })
        self.assertEqual(response.status_code, 401)
    
    def test_file_download_invalid(self):
        response = self.post('/files/download', {
            "auth": self.__class__.auth,
        })
        self.assertEqual(response.status_code, 400)
        response = self.post('/files/download', {
            "auth": self.__class__.auth,
            "name": "exists.txt"
        })
        self.assertEqual(response.status_code, 400)

    @pytest.mark.run(order=4)
    def test_file_delete_valid(self):
        response = self.post('/files/delete', {
            "auth": self.__class__.auth,
            "fileId": 1,
            "name": "test.txt"
        })
        self.assertEqual(response.status_code, 200)

    def test_file_delete_unauth(self):
        response = self.post('/files/delete', {
            "auth": self.__class__.unauth,
            "fileId": 1,
            "name": "test.txt"
        })
        self.assertEqual(response.status_code, 403)
        response = self.post('/files/delete', {
            "fileId": 1,
            "name": "test.txt"
        })
        self.assertEqual(response.status_code, 401)
    
    @pytest.mark.run(order=5)
    def test_file_delete_invalid(self):
        response = self.post('/files/delete', {
            "auth": self.__class__.auth,
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/files/delete', {
            "auth": self.__class__.auth,
            "fileId": 4,
            "name": "test.txt"
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/files/delete', {
            "auth": self.__class__.auth,
            "fileId": 2,
            "name": "info.txt"
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/files/delete', {
            "auth": self.__class__.auth,
            "fileId": 2,
            "name": "none.txt"
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/files/delete', {
            "auth": self.__class__.auth,
            "fileId": 3,
            "name": "none.txt"
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/files/delete', {
            "auth": self.__class__.auth,
            "fileId": 3,
            "name": "none.txt"
        })
        self.assertEqual(response.status_code, 400)