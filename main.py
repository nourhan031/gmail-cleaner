import time
from datetime import datetime, timedelta
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow # handles the OAuth authorization flow for installed applications
from google.auth.transport.requests import Request # provides a request object for making HTTP requests
from googleapiclient.discovery import build # constructs a resource object for interacting with the API
from googleapiclient.errors import HttpError # handles errors that occur during API requests


CLIENT_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
# ACCESS LEVEL: Read, write and send emails in Gmail, and delete them all permanently
SCOPES = ['https://mail.google.com/']

# create and return a service object for interacting with the gmail API
def create_service(client_file, api_name, api_version, scopes):
    creds = None
    # check if this token exists
    if os.path.exists('token.json'):
        # if yes, load the credentials from it
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # else, start the OAuth flow to get new creds
    if not creds or not creds.valid:
        # if the creds are expired and a refresh token is available
        if creds and creds.expired and creds.refresh_token:
            # refresh the credentials
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_file, scopes)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # build and return the service object using the obtained creds
    service = build(api_name, api_version, credentials=creds)
    return service


gmail_service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)


# return the date one year ago from the current date 
def one_year_ago():
    return (datetime.now() - timedelta(days=365)).strftime('%Y/%m/%d')


# search for emails matching the given query
def search(user_id, query, labels=None):
    # init an empty list for storing email msgs and a var for the next page token
    email_messages = []
    next_page_token = None

    try:
        # make an init req to the API to search for emails based on the query and the date from the 'one year ago' func
        message_response = gmail_service.users().messages().list(
            userId=user_id,
            labelIds=labels,
            includeSpamTrash=False,
            q=f"{query} before:{one_year_ago()}",
            maxResults=500
        ).execute()
        # add the results to the email messages list
        email_messages.extend(message_response.get('messages', []))
        # get the next page token if it exists
        next_page_token = message_response.get('nextPageToken')

        # while there is a next page token
        while next_page_token:
            # cont to request and add more emails to the list
            message_response = gmail_service.users().messages().list(
                userId=user_id,
                labelIds=labels,
                q=f"{query} before:{one_year_ago()}",
                maxResults=500,
                includeSpamTrash=False,
                pageToken=next_page_token
            ).execute()
            email_messages.extend(message_response.get('messages', []))
            next_page_token = message_response.get('nextPageToken')
            print('Page Token: {0}'.format(next_page_token))
            time.sleep(0.5)

    except HttpError as error:
        print(f'An error occurred: {error}')

    return email_messages


# move emails to the trash
def delete(user_id, email_ids):
    # iterate over the list of email IDs
    for email_id in email_ids:
        # for each, it sends a req to the API to trash the email
        try:
            gmail_service.users().messages().trash(
                userId=user_id,
                id=email_id['id']
            ).execute()
            # print(f"Email with ID {email_id['id']} deleted successfully.")
            print(f"Successfully deleted email with ID: {email_id['id']} YIPPEE")
        except HttpError as error:
            print(f'An error occurred: {error} :(')


def get_user_confirmation():
    return input("Are you sure you want to delete old emails? (yes/no): ").strip().lower() == 'yes'


target_user_email = 'target@gmail.com'
query_string = "in:inbox"
# get a list of email results matching the query
emails_to_delete = search(target_user_email, query_string)

# prompt user for confirmation if email results exist
if emails_to_delete:
    if get_user_confirmation():
        delete(target_user_email, emails_to_delete)
    else:
        print("Deletion canceled.")
else:
    print("No matching emails found.")
