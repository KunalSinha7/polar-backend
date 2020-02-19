import boto3
from botocore.exceptions import ClientError



def send():
    sender = 'Polarapp <mail@polarapp.xyz>'
    recipients = []
    recipients.append('will@wborland.com')
    recipients.append('wborland@purdue.edu')
    aws_region = 'us-east-1'
    subject = 'AWS SES Test from polar'
    body_text = ('This is a test\nnew line\nThanks')
    body_html = '''
    <html>
    <head></head>
    <body>
        <h1>This is a test</h1>
        <h3>Thanks</h3>
    </body>
    </html>
    '''
    charset = 'utf-8'


    client = boto3.client('ses', region_name=aws_region)

    try:
        response = client.send_email(
            Destination={'BccAddresses': recipients,},
            Message={
                'Body': {
                    'Html': {'Charset':charset, 'Data': body_html,},
                    'Text': {'Charset': charset, 'Data': body_text,},
                },
                'Subject': {'Charset': charset, 'Data':subject,},
            },
            Source=sender
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('Email sent')
        print(response['MessageId'])