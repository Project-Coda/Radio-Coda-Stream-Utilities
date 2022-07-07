# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
# The following code was adapted from the YouTube API v3 documentation

import os
import random
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
token_file = os.environ["TOKEN_FILE"]
random_text = os.environ["RANDOM_TEXT"]
FNAME = os.environ["NP_SOURCE"]

# Initialize counter for number of messages sent
message_count = 0


# Get credentials and create an API client

credentials = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists(token_file):
    credentials = Credentials.from_authorized_user_file(token_file, scopes)
# If there are no (valid) credentials available, let the user log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes
        )
        credentials = flow.run_local_server(port=5410)
    # Save the credentials for the next run
    with open(token_file, "w") as token:
        token.write(credentials.to_json())
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials
)


@app.route("/", methods=["POST", "GET"])
def index():
    req_data = request.get_json()
    if "now_playing" in req_data:
        if "song" in req_data["now_playing"]:
            if "text" in req_data["now_playing"]["song"]:
                text = req_data["now_playing"]["song"]["text"]
                if "link" in req_data["now_playing"]["song"]["custom_fields"]:
                    link = req_data["now_playing"]["song"]["custom_fields"]["link"]
                update_now_playing(text)
                send_message(text, link)
                if message_count > 2:
                    send_message(random_message())
                    message_count = 0
                else:
                    message_count += 1

    return '{"success":"true"}'
def random_message():
    with open(random_text, "r") as f:
        text = f.read()
        message = text.split("\n")
        message = random.choice(message)
    return message

def update_now_playing(text):
    with open(FNAME, "w") as f:
        f.write(text)

def create_now_playing_text(text, link):
    if link == None:
        now_playing_text = "Now Playing: " + text
    else:
        now_playing_text = "Now Playing: " + text + " - " + link
    print(now_playing_text)
    return now_playing_text

def send_message(message):
    liveChatId = (
        youtube.liveBroadcasts()
        .list(
            part="snippet",
            broadcastStatus="active",
        )
        .execute()
    )
    if len(liveChatId["items"]) == 0:
        return
    liveChatId = liveChatId["items"][0]["snippet"]["liveChatId"]

    print(message)
    ytsend = youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "type": "textMessageEvent",
                "liveChatId": liveChatId,
                "textMessageDetails": {"messageText": message},
            }
        },
    )

    response = ytsend.execute()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
