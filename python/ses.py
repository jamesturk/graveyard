import os
import email
import boto3

"""
Environment Variables

AWS_DEFAULT_PROFILE
S3_BUCKET
"""

S3_BUCKET = os.environ['S3_BUCKET']


def incoming(event, context):
    mail = event['Records'][0]['ses']['mail']
    # from_email = mail['source']
    # desination = mail['destination']
    message_id = mail['messageId']

    return get_message(message_id)


def get_message(message_id):
    s3 = boto3.client('s3')
    body = s3.get_object(Bucket=S3_BUCKET, Key=message_id)['Body']

    msg = email.message_from_bytes(body.read())
    resp = {
        'date': msg['date'],
        'from': msg['from'],
        'to': msg['to'],
        'subject': msg['subject'],
    }
    for part in msg.get_payload():
        if part.get_content_type() == 'text/plain':
            resp['body_text'] = part.get_payload()
        elif part.get_content_type() == 'text/html':
            resp['body_html'] = part.get_payload()

    return resp
