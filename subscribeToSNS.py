import boto3
import json
from updateTable import add_phone_number

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
    print(response)
    subscriptionARN = response['SubscriptionArn']
    add_phone_number(id, phoneNumber, subscriptionARN)

    


