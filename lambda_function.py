import sys
import os
import requests
import json

def get_access_token(client_id, client_secret, tenant_id):
    auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body_user = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    # response = requests.post(auth_url, headers=headers, data=body_user)
    response_token = requests.post(url, headers=headers, data=body)
    response_token.raise_for_status()
    # return response
    return response_token.json().get('access_token')

def list_users(access_token):
    url = "https://graph.microsoft.com/v1.0/users"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# token  = get_access_token(CLIENT_ID, CLIENT_SECRET, TENANT_ID)
# print("Successfully obtained access token.")
# print(token)


import boto3
import json

def get_parameter():
    parameter_name = "/my/azure/credentials"
    region_name = "ap-southeast-2"

    # Create an SSM client
    client = boto3.client('ssm', region_name=region_name)

    # Retrieve the parameter value
    response = client.get_parameter(Name=parameter_name, WithDecryption=True)
    
    # Parse the parameter value as JSON
    parameter = json.loads(response['Parameter']['Value'])
    
    return parameter


    # Use these credentials as needed



# def handler(event, context):
# return 'Hello from AWS Lambda using Python' + sys.version + '!'
try:
    # # azure_credentials = os.getenv('AZURE_CREDENTIALS')
    # # print(azure_credentials)

    # # credentials = json.loads(azure_credentials)
    # # print(credentials)
    # with open('azure_credentials.json') as f:
    #     credentials = json.load(f)
    # credentials = get_parameter()
    azure_credentials = os.getenv('AZURE_CREDENTIALS')
    azure_credentials = json.loads(azure_credentials)



    TENANT_ID = azure_credentials['tenantId']
    CLIENT_ID = azure_credentials['clientId']
    CLIENT_SECRET = azure_credentials['clientSecret']
        

    print("tenant id ",TENANT_ID)

    # # Extract individual fields from the JSON
    # CLIENT_ID = credentials.get('clientId')
    # CLIENT_SECRET = credentials.get('clientSecret')
    # TENANT_ID = credentials.get('tenantId')
    token = get_access_token(CLIENT_ID, CLIENT_SECRET, TENANT_ID)
    # print("Successfully obtained access token.")
    # print(token)
    users = list_users(token)
    print("Successfully connected to Microsoft Graph API. Here are the first 10 users:")
    for user in users['value'][:10]:
        print(f"User: {user['displayName']}, Email: {user['mail']}")
except Exception as e:
    print(f"An error occurred: {e}")
