# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from flask import Flask, request
app = Flask(__name__)
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = os.environ["CLIENT_SECRETS_FILE"]
tokenfile = os.environ["TOKEN_FILE"]

# Get credentials and create an API client

credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists(tokenfile):
    credentials = Credentials.from_authorized_user_file(tokenfile, scopes)
# If there are no (valid) credentials available, let the user log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(tokenfile, 'w') as token:
        token.write(credentials.to_json())
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

@app.route('/', methods=['POST','GET'])
def index():
    req_data = request.get_json()
    if "now_playing" in req_data:
        if "song" in req_data["now_playing"]:
            if "text" in req_data["now_playing"]["song"]:
                text = req_data["now_playing"]["song"]["text"]
                if "link" in req_data["now_playing"]["song"]:
                    link = req_data["now_playing"]["song"]["link"]
                else:
                    link = "discord.gg/coda"
                print(text, link)
                send_message(text, link)
    return '{"success":"true"}'

def send_message(text, link):
    liveChatId = youtube.liveBroadcasts().list(
        part="snippet",
        broadcastStatus="active",
    ).execute()
    if len(liveChatId["items"]) == 0:
        return
    liveChatId = liveChatId["items"][0]["snippet"]["liveChatId"]
    print(liveChatId)

    ytsend = youtube.liveChatMessages().insert(
        part="snippet",
        body={
          "snippet": {
            "type": "textMessageEvent",
            "liveChatId": "{lcid}",
            "textMessageDetails": {
              "messageText": "Now Playing: {now_playing} - {link}"
            }
          }.format(lcid=liveChatId, now_playing=text, link=link)
        }
    )

    response = ytsend.execute()
    print(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)