import json

def create_session(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/json'
        },
        'body': json.dumps({'session_id': 'XXXX'})
    }

def join_session(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/json'
        },
        'body': json.dumps({'websocket_topic': 'XXXX'})
    }
