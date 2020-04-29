from tests import BaseTestCase
from flaskapp import app

import unittest as ut
import json
import auth.jwt
import pytest
from datetime import datetime, timedelta

class EventTestCase(BaseTestCase):

    auth = None

    @pytest.mark.run(order=1)
    def test_event_setup(self):
        response = self.post('/user/login', {
            "email": "admin@polarapp.xyz",
            "password": "password"
        })
        data = response.get_json()
        self.__class__.auth = data['auth']
        self.assertEqual(response.status_code, 200)

        response = self.post('/event/all', {
            "auth": self.__class__.auth
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_event_create_valid(self):
        response = self.post('/event/create', {
            "auth": self.__class__.auth,
            "name": "Party",
            "startTime": None,
            "endTime": None,
            "location": "Dunham, NC",
            "desc": "party for recent grads",
            "reminder": 0,
            "reminderTime": -1,
            "questions": ["Major", "Name", "Grad Year"]
        })

        response = self.post('/event/all', {
            "auth": self.fake_user()
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)

    def test_event_create_invalid(self):
        response = self.post('/event/create', {})
        self.assertEqual(response.status_code, 401)

        response = self.post('/event/create', {
            "auth": self.fake_user(),
        })
        self.assertEqual(response.status_code, 403)

        response = self.post('/event/create', {
            "auth": self.__class__.auth,
        })
        self.assertEqual(response.status_code, 400)

    def test_event_details(self):
        response = self.post('/event/details', {
            "auth": self.__class__.auth,
            "id": 1
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) > 9)
        n = len(data)
    
        response = self.post('/event/details', {
            "auth": self.fake_user(),
            "id": 1
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data) != n)
    
    def test_event_edit(self):
        response = self.post("/event/modify", {
            "auth": self.__class__.auth,
            "id": 1,
            "name": "PARTY!!!",
            "startTime": None,
            "endTime": None,
            "location": "Dublin, NC",
            "desc": "party for recent grads has been moved",
            "reminder": 0,
            "reminderTime": -1
        })
        self.assertEqual(response.status_code, 200)

    def test_event_edit_confirm(self):
        response = self.post('/event/details', {
            "auth": self.__class__.auth,
            "id": 1
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], "PARTY!!!")
        self.assertEqual(data["startTime"], None)
        self.assertEqual(data["endTime"], None)
        self.assertEqual(data["location"], "Dublin, NC")
        self.assertEqual(data["desc"], "party for recent grads has been moved")
    
    def test_event_edit_invalid(self):
        response = self.post("/event/modify", {
            "auth": self.fake_user()
        })
        self.assertEqual(response.status_code, 403)

        response = self.post("/event/modify", {})
        self.assertEqual(response.status_code, 401)

        response = self.post("/event/modify", {
            "auth": self.__class__.auth
        })
        self.assertEqual(response.status_code, 400)

    def test_event_rsvp(self):
        response = self.post("/event/rsvp", {
            "auth": self.__class__.auth,
            "id": 1,
            "answers": ['cs', 'dvaz', '2012']
        })
        self.assertEqual(response.status_code, 200)

        response = self.post("/event/unrsvp", {
            "auth": self.__class__.auth,
            "id": 1
        })
        self.assertEqual(response.status_code, 200)

    def test_event_rsvp_invalid(self):
        response = self.post("/event/unrsvp", {})
        self.assertEqual(response.status_code, 401)

        response = self.post("/event/rsvp", {})
        self.assertEqual(response.status_code, 401)

        response = self.post("/event/rsvp", {
            "auth": self.__class__.auth,
        })
        self.assertEqual(response.status_code, 400)

        response = self.post("/event/rsvp", {
            "auth": self.__class__.auth,
            "id": 71
        })
        self.assertEqual(response.status_code, 400)

        response = self.post("/event/rsvp", {
            "auth": self.__class__.auth,
            "id": 1,
            "answers": ["no"]
        })
        self.assertEqual(response.status_code, 400)

        response = self.post("/event/unrsvp", {
            "auth": self.__class__.auth
        })
        self.assertEqual(response.status_code, 400)
    
    def test_event_table_close(self):
        response = self.post('event/close', {
            "auth": self.__class__.auth,
            "id": 1
        })
        self.assertEqual(response.status_code, 200)
    
    def test_event_table_close_invalid(self):
        response = self.post('event/close', {})
        self.assertEqual(response.status_code, 401)

        response = self.post('event/close', {
            "auth": self.fake_user()
        })
        self.assertEqual(response.status_code, 403)

        response = self.post('event/close', {
            "auth": self.__class__.auth
        })
        self.assertEqual(response.status_code, 400)

    def test_event_table_remove(self):
        response = self.post('/event/delete', {
            "auth": self.__class__.auth,
            "id": 1
        })
        self.assertEqual(response.status_code, 200)

        response = self.post('/event/details', {
            "auth": self.__class__.auth,
            "id": 1
        })
        self.assertEqual(response.status_code, 400)

    def test_event_table_remove_invalid(self):
        response = self.post('/event/delete', {})
        self.assertEqual(response.status_code, 401)

        response = self.post('/event/delete', {
            "auth": self.__class__.auth
        })
        self.assertEqual(response.status_code, 400)

        response = self.post('/event/delete', {
            "auth": self.fake_user()
        })
        self.assertEqual(response.status_code, 403)
