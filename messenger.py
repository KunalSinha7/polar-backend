from datetime import datetime
from datetime import timedelta
from dateutil import tz

import MySQLdb as sql
from MySQLdb.cursors import DictCursor
import configparser
import message.email as mail
import message.text as text
import os

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')


def getEvents():
    get_events_cmd = '''select * from Event where reminder = 1;'''
    cursor.execute(get_events_cmd)

    return cursor.fetchall()


def make_conn():

    path = ''
    if os.path.isfile('/home/ubuntu/database.ini'):
        path = '/home/ubuntu/database.ini'
    else:
        path = '../database.ini'

    parser = configparser.ConfigParser()
    parser.read(path)

    return sql.connect(
        host=parser.get('database', 'host'),
        db=parser.get('database', 'name'),
        passwd=parser.get('database', 'pass'),
        user=parser.get('database', 'user'),)


def getUsersFromEvent(eventId):
    get_users_cmd = '''select e.userId, u.Email, u.Phone from event_{} as e join Users as u on e.userId = u.userId;'''.format(
        eventId)
    cursor.execute(get_users_cmd)

    return cursor.fetchall()


def changeReminder(eventId):
    change_reminder_cmd = '''UPDATE Event SET reminder = 0 where eventId = {};'''.format(
        eventId)
    cursor.execute(change_reminder_cmd)
    conn.commit()


def dayHourMinute(minutes):
    time_left = minutes
    day = 0
    hour = 0
    minute = 0

    if time_left/1440 >= 1:
        day = int(time_left/1440)
        time_left = time_left % 1440

    if time_left/60 >= 1:
        hour = int(time_left/60)
        time_left = time_left % 60

    minute = time_left

    return day, hour, minute


conn = make_conn()
cursor = conn.cursor()


events = getEvents()


for e in events:
    reminder_time = e[2] - timedelta(minutes=e[7])

    with open('/home/ubuntu/flaskapp/log.txt', 'a') as myFile:
        myFile.write("Found event " + str(e))
        myFile.write("\n")

    if reminder_time < datetime.utcnow():

        try:
            users = getUsersFromEvent(e[0])
            for u in users:
                with open('/home/ubuntu/flaskapp/log.txt', 'a') as myFile:
                    myFile.write("Sending to " + str(u))
                    myFile.write("\n")

                subject = 'You have {} starting soon!'.format(e[1])
                body = 'Hi there, <br> This message is to remind you that you have {} starting in '.format(
                    e[1])

                day, hour, minute = dayHourMinute(e[7])
                time_str = ''

                if day >= 1:
                    time_str = time_str + str(day) + ' day '

                if hour > 1:
                    time_str = time_str + str(hour) + ' hour\'s '
                elif hour == 1:
                    time_str = time_str + str(hour) + ' hour '

                time_str = time_str + str(minute) + ' minutes.'

                mail.sendEmail(u[1], subject, body + time_str)
                text.sendSMS(u[2], 'This message is to remind you about {} starting in {}'.format(
                    e[1], time_str))
        except Exception as e:
            with open('/home/ubuntu/flaskapp/log.txt', 'a') as myFile:
                myFile.write("ERROR " + str(e))
                myFile.write("\n")
    changeReminder(e[0])
