import boto3
import json
import dynamodb as db


region_name = "us-west-2"
sns_client = boto3.client('sns',region_name=region_name)
publishARN = sns_client.list_topics()['Topics'][1]['TopicArn']

def subscribe(id, phoneNumber):
    response = sns_client.subscribe(
        TopicArn=publishARN,
        Protocol="sms",
        Endpoint=phoneNumber,
        ReturnSubscriptionArn=True
    )
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    subscriptionARN = response['SubscriptionArn']
    if status_code == 200:
        db.add_phone_number(id, phoneNumber, subscriptionARN)
        return db.getResponse(status_code, db.get_user(id)['body'])

def unsubscribe(id):
    subscriptionARN = db.get_user(id)['body']['subscriptionARN']
    if not subscriptionARN: 
        return db.getResponse(200, db.get_user(id)['body'])
    response = sns_client.unsubscribe(SubscriptionArn=subscriptionARN)
    db.add_phone_number(id, "", "")
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    return db.getResponse(status_code, db.get_user(id)['body'])

def testNumber(number):
    response = sns_client.publish(PhoneNumber=number, Message="Thanks for signing up.")
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    return db.getResponse(status_code, json.dumps({"status": "request valid"}))
    









