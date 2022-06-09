import json
import dynamodb as db
import SNS as sns

def response(body):
    return {"statusCode": 200, "body": body}

def handler(event, context):
    body = json.loads(event['body'])
    eventkeys = body.keys()
    userId = body['userId'] if 'userId' in eventkeys else ''
    phoneNumber = body['phoneNumber'] if 'phoneNumber' in eventkeys else ''
    request = body['request'] if 'requestType' in eventkeys else ''
    
    if userId and not phoneNumber and not request:
        return response(db.create_user(userId))
    if userId and phoneNumber:
        return response(sns.subscribe(userId, phoneNumber))
    if userId and request == 'delete':
        return response(db.delete_user(userId))
    
    return response("null input")
    
