import json
import phonenumbers as pn
import dynamodb as db
import SNS as sns


def response(code, body):
    return {"statusCode": code, "body": body}

def validNumber(number):
    try:
        phoneNumber = pn.parse(number)
        return pn.is_valid_number(phoneNumber)
    except:
        return False

def handler(event, context):
    body = json.loads(event['body'])
    eventkeys = body.keys()
    userId = body['userId'] if 'userId' in eventkeys else ''
    phoneNumber = body['phoneNumber'] if 'phoneNumber' in eventkeys else ''
    request = body['request'] if 'request' in eventkeys else ''
    
    if userId and not phoneNumber and not request:
        return response(200, json.dumps(db.create_user(userId)))

    if userId and request == "unsub":
        return response(200, json.dumps(sns.unsubscribe(userId)))
    
    if userId and request == "delete":
        sns.unsubscribe(userId)
        return  response(200, json.dumps(db.delete_user(userId)))

    if userId and phoneNumber and not request:
        if validNumber(phoneNumber):
            result = sns.subscribe(userId, phoneNumber)
            sns.testNumber(phoneNumber)
            return response(200, json.dumps(result))
        else:
            return response(400, json.dumps({"status": "invalid phone number"}))    
    
    return response(200, "null/no input")
  
    
