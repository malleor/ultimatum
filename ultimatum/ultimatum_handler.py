import json
import os
import uuid
import boto3
from data import Session, Participant

common_headers = {
    'Content-Type': 'text/json',
    'Access-Control-Allow-Origin': '*'
}

def create_session(event, context):
    print('request: {}'.format(json.dumps(event)))

    # connect to a database
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    table_name = os.environ.get('TABLE_NAME')
    table = db.Table(table_name)
    print('fetched table:', table_name)

    # prep new session
    new_session_id = str(uuid.uuid4().hex)
    new_session = Session(new_session_id)

    # write to database
    put_res = table.put_item(Item=new_session.to_dict())
    print('created a new session:', new_session_id)
    print(json.dumps(put_res, indent=2))

    # form response
    return {
        'statusCode': 200,
        'headers': common_headers,
        'body': json.dumps({'session_id': new_session.session_id})
    }

def join_session(event, context):
    print('request: {}'.format(json.dumps(event)))

    # parse request
    body = json.loads(event['body'])
    session_id = body['session_id']
    user_name = body['user_name']

    # connect to a database
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    table_name = os.environ.get('TABLE_NAME')
    table = db.Table(table_name)
    print('fetched table:', table_name)

    # get data
    get_res = table.get_item(Key={'session_id': session_id})
    print(json.dumps(get_res, indent=2))
    session_item = get_res['Item']

    # add a participant
    participant = Participant(user_name)
    upd_res = table.update_item(
        Key={'session_id': session_id},
        UpdateExpression='SET participants = list_append(participants, :p)',
        ExpressionAttributeValues={
            ':p': [participant.to_dict()]
        })
    print(json.dumps(upd_res, indent=2))

    # form response
    return {
        'statusCode': 200,
        'headers': common_headers,
        'body': json.dumps({})
    }
