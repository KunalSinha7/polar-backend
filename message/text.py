import boto3
from botocore.exceptions import ClientError


aws_region = 'us-east-1'
sms_client = boto3.client('sns', region_name=aws_region)


def sendSMS(number, message):
    number = '+1' + number
    print(number)
    message = 'POLAR APP: ' + message
    sms_client.publish(PhoneNumber=number, Message=message)