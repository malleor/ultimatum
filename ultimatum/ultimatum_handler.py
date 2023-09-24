import json
import os
import uuid
import boto3
from data import Session, Participant

common_headers = {
    'Content-Type': 'text/json',
    'Access-Control-Allow-Origin': '*'
}

def get_table():
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    table_name = os.environ.get('TABLE_NAME')
    table = db.Table(table_name)
    print('fetched table:', table.table_name)
    return table


def create_session(event, context):
    print('request: {}'.format(json.dumps(event)))

    # connect to a database
    table = get_table()

    # prep new session
    new_session_id = str(uuid.uuid4().hex)
    new_session = Session(new_session_id)

    # write to database
    put_res = table.put_item(Item=new_session.to_dict())
    print('created a new session:', new_session_id)
    print('put_res: {}'.format(json.dumps(put_res)))

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
    table = get_table()

    # get data
    get_res = table.get_item(Key={'session_id': session_id})
    print('get_res: {}'.format(json.dumps(get_res)))
    session_item = get_res['Item']

    # add a participant
    participant = Participant(user_name)
    upd_res = table.update_item(
        Key={'session_id': session_id},
        UpdateExpression='SET participants = list_append(participants, :p)',
        ExpressionAttributeValues={
            ':p': [participant.to_dict()]
        })
    print('upd_res: {}'.format(json.dumps(upd_res)))

    # form response
    return {
        'statusCode': 200,
        'headers': common_headers,
        'body': json.dumps({})
    }

def get_participants(event, context):
    print('request: {}'.format(json.dumps(event)))

    # parse request
    params = event['queryStringParameters']
    session_id = params['session_id']

    # connect to a database
    table = get_table()

    # get data
    get_res = table.get_item(
        Key={'session_id': session_id}
        )
    print('get_res: {}'.format(json.dumps(get_res)))
    participants = get_res['Item']['participants']

    # form response
    return {
        'statusCode': 200,
        'headers': common_headers,
        'body': json.dumps(participants)
    }
