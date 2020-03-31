import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

sender = 'Polarapp <mail@polarapp.xyz>'
aws_region = 'us-east-1'
charset = 'utf-8'
email_client = boto3.client('ses', region_name=aws_region)


def sendEmailAttachment(email, subject, message, file, basename):

    body_text = message
    body_html = '''
    <html>
    <head></head>
    <body>
        <p>{}</p>
    </body>
    </html>
    '''.format(message)

    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = email

    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(body_text.encode(charset), 'plain', charset)
    htmlpart = MIMEText(body_html.encode(charset), 'html', charset)
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    att = MIMEApplication(open(file, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename=basename)
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    msg.attach(att)
    # print(msg)
    try:
        # Provide the contents of the email.
        response = email_client.send_raw_email(
            Source=sender,
            Destinations=[
                email
            ],
            RawMessage={
                'Data': msg.as_string(),
            }
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


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
