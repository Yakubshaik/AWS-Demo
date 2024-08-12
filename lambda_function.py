import sys
import os
import requests

# Replace these with your Azure AD application details
CLIENT_ID = os.getenv('Client_Id')
CLIENT_SECRET = os.getenv('Client_Secret')
TENANT_ID = os.getenv('Tenant_Id')

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


def handler(event, context):
    # return 'Hello from AWS Lambda using Python' + sys.version + '!'
    try:
        token = get_access_token(CLIENT_ID, CLIENT_SECRET, TENANT_ID)
        print("Successfully obtained access token.")
        print(token)
        users = list_users(token)
        print("Successfully connected to Microsoft Graph API. Here are the first 10 users:")
        for user in users['value'][:10]:
            print(f"User: {user['displayName']}, Email: {user['mail']}")
    except Exception as e:
        print(f"An error occurred: {e}")
