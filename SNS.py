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
        return response
    else: 
        return {
            "statusCode": status_code,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"status": "request invalid"})
        }

def unsubscribe(id):
    subscriptionARN = db.get_user(id)['body'][0]['subscriptionARN']
    response = sns_client.unsubscribe(SubscriptionArn=subscriptionARN)
    db.add_phone_number(id, "", "")
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    return 0 if status_code == 200 else -1






