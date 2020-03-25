import boto3
from botocore.exceptions import ClientError

sender = 'Polarapp <mail@polarapp.xyz>'
aws_region = 'us-east-1'
charset = 'utf-8'
email_client = boto3.client('ses', region_name=aws_region)


def sendEmail(email, subject, message):
    recipients = []
    recipients.append(email)

    body_text = message
    body_html = '''
    <html>
    <head></head>
    <body>
        <p>{}</p>
    </body>
    </html>
    '''.format(message)

    try:
        response = email_client.send_email(
            Destination={'ToAddresses': recipients, },
            Message={
                'Body': {
                    'Html': {'Charset': charset, 'Data': body_html, },
                    'Text': {'Charset': charset, 'Data': body_text, },
                },
                'Subject': {'Charset': charset, 'Data': subject, },
            },
            Source=sender
        )
    except ClientError as e:
        print(e.response['Error']['Message'])

