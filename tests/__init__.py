import os
import flaskapp
from flask import g
from flaskapp import app

import unittest as ut
import db.util as db


import sys
import json


class BaseTestCase(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseTestCase, cls).setUpClass()
        db.setupTestDB()

    def setUp(self):
        self.app = flaskapp.app.test_client()
        self.app.TESTING = True
        app.config['TESTING'] = True
        

    def post(self, route, data, headers=None):
        if headers is not None:
            return self.app.post(route, data=json.dumps(data),
                                 content_type='application/json', headers=headers)
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





if __name__ == "__main__":
    ut.main()
