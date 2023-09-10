import json

common_headers = {
    'Content-Type': 'text/json',
    'Access-Control-Allow-Origin': '*'
}

def create_session(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': common_headers,
        'body': json.dumps({'session_id': 'XXXX'})
    }

def join_session(event, context):
    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': common_headers,
        'body': json.dumps({'websocket_topic': 'XXXX'})
    }
