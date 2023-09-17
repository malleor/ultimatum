import json
import os
import uuid
import boto3

common_headers = {
    'Content-Type': 'text/json',
    'Access-Control-Allow-Origin': '*'
}

def create_session(event, context):
    print('request: {}'.format(json.dumps(event)))

    db = boto3.resource('dynamodb', region_name='eu-central-1')

    table_name = os.environ.get('TABLE_NAME')
    print('table name:', table_name)

    new_session_id = str(uuid.uuid4().hex)
    table = db.Table(table_name)
    put_res = table.put_item(
        Item={
            'id': new_session_id
        }
    )
    print('created a new session:', new_session_id)
    print(json.dumps(put_res, indent=2))

    return {
        'statusCode': 200,
        'headers': common_headers,
        'body': json.dumps({'session_id': new_session_id})
    }

def join_session(event, context):
    print('request: {}'.format(json.dumps(event)))
    body = json.loads(event['body'])
    session_id = body['session_id']
    return {
        'statusCode': 200,
        'headers': common_headers,
        'body': json.dumps({
            'session_id': session_id,
            'websocket_topic': 'XXXX'
            })
    }
