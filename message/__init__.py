import boto3
from botocore.exceptions import ClientError

sender = 'Polarapp <mail@polarapp.xyz>'
aws_region = 'us-east-1'
charset = 'utf-8'
email_client = boto3.client('ses', region_name=aws_region)


def sendForgotPassword(email, link):
    recipients = []
    recipients.append(email)


    subject = 'Forgot your password?'

    body_text = ('Did you forget your password?\nIf you did go to this link:{}').format(link)
    body_html = '''
    <html>
    <head></head>
    <body>
        <h2>Did you forget your password?</h2>
        <p>If you did you can click <a href='{}'>here</a> or go to this link: {}</p>
    </body>
    </html>
    '''.format(link, link)



    try:
        response = email_client.send_email(
            Destination={'ToAddresses': recipients,},
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