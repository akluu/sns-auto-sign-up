import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userId')

def create_user(id):
    item = {"userId": id, "phoneNumber": "", "subscriptionARN": ""}
    result = table.put_item(Item = item)
    status_code = result['ResponseMetadata']['HTTPStatusCode']
    return getResponse(status_code, json.dumps(item))
    
def delete_user(id):
    key = {"userId": id}
    result = table.delete_item(Key = key)
    status_code = result['ResponseMetadata']['HTTPStatusCode']
    return getResponse(status_code, json.dumps({"status": id + " deleted"}))
    
def get_user(id):
    result = table.query(
        KeyConditionExpression='userId = :userId',
        ExpressionAttributeValues={
        ':userId': id
    })
    status_code = result['ResponseMetadata']['HTTPStatusCode']
    return getResponse(status_code, result["Items"])
    
def add_phone_number(id, number, subscriptionARN):
    key = {"userId": id}
    result = table.update_item(Key = key, 
    UpdateExpression = "Set phoneNumber=:p, subscriptionARN=:s ",
    ExpressionAttributeValues = {
        ':p' : number,
        ':s' : subscriptionARN
    },
    ReturnValues = "UPDATED_NEW")
    status_code = result['ResponseMetadata']['HTTPStatusCode']
    return getResponse(status_code, result['Attributes'])
    
def getResponse(status_code, body):
    if status_code == 200:
        response = {
            "statusCode": status_code,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": body
        }
        return response
    else:
        return {
            "statusCode": status_code,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"status": "request invalid"})
        }

