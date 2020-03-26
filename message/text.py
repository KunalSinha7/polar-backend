import boto3
from botocore.exceptions import ClientError


aws_region = 'us-east-1'
sms_client = boto3.client('sns', region_name=aws_region)


def sendSMS(number, message):
    message = 'POLAR APP: ' + message
    sms_client.publish(PhoneNumber= '+1' + number, Message=message)