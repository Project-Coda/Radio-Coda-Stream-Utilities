# -*- coding: utf-8 -*-


"""
    This code manages the now playing text and YouTube Live chatbot for the Radio Coda Stream
    Author: Matheson Steplock
    Adapted from: https://developers.google.com/explorer-help/code-samples#python
"""

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
random_text = os.environ["RANDOM_TEXT_FILE"]
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
    with open(token_file, "w", encoding="utf-8") as token:
        token.write(credentials.to_json())
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials
)


@app.route("/", methods=["POST", "GET"])
def index():
    """
    Main function which handles the request from the webhook sent by AzuraCast
    """
    req_data = request.get_json()
    if "now_playing" in req_data:
        if "song" in req_data["now_playing"]:
            if "text" in req_data["now_playing"]["song"]:
                text = req_data["now_playing"]["song"]["text"]
                if "link" in req_data["now_playing"]["song"]["custom_fields"]:
                    link = req_data["now_playing"]["song"]["custom_fields"]["link"]
                update_now_playing(text)
                now_playing_text = create_now_playing_text(text, link)
                send_message(now_playing_text)
                global message_count
                print("Message count:" + str(message_count))
                if message_count > 2:
                    send_message(random_message())
                    message_count = 0
                else:
                    message_count += 1

    return "OK Updated " + str(now_playing_text)


def random_message():
    """
    Returns a random message from the list of messages in
    the random_text file defined in the environment variable
    """
    with open(random_text, "r", encoding="utf-8") as f:
        text = f.read()
        message = text.split("\n")
        message = random.choice(message)
        f.close()
    return message


def update_now_playing(text):
    """
    Updates the now playing text in the source file which is read by ffmpeg
    """
    with open(FNAME, "w", encoding="utf-8") as f:
        f.write(text)
    return f.close()


def create_now_playing_text(text, link):
    """
    Creates the now playing text to be sent to the chat
    """
    if link is None:
        now_playing_text = "Now Playing: " + text
    else:
        now_playing_text = "Now Playing: " + text + " - " + link
    print(now_playing_text)
    return now_playing_text


def send_message(message):
    """
    Sends a message to the YouTube Live Chat
    """
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

    return ytsend.execute()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
