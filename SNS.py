import boto3
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
    response = sns_client.unsubscribe(SubscriptionArn=subscriptionARN)
    db.add_phone_number(id, "", "")
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    return db.getResponse(status_code, db.get_user(id)['body'])






