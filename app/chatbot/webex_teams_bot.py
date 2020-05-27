import json
import re
import requests
import os
import time
from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI


flask_app = Flask(__name__)

api = WebexTeamsAPI()

# Verify all of the environment variables are defined and available
ROOM_NAME = os.environ.get("ROOM_NAME")
WEBEX_BOT_USERNAME = os.environ.get("WEBEX_BOT_USERNAME")
WEBEX_TEAMS_ACCESS_TOKEN = os.environ.get("WEBEX_TEAMS_ACCESS_TOKEN")

if ROOM_NAME is None:
    raise ValueError(
        f"Please set environment variable for room name, 'export ROOM_NAME=<room_name>'"
    )

if WEBEX_BOT_USERNAME is None:
    raise ValueError(
        f"Please set environment variable for room name, 'export WEBEX_BOT_USERNAME=<webex_bot_username>'"
    )

if WEBEX_TEAMS_ACCESS_TOKEN is None:
    raise ValueError(
        f"Please set environment variable for room name, 'export WEBEX_TEAMS_ACCESS_TOKEN=<webex_teams_access_token>'"
    )

@flask_app.route("/", methods=["GET"])
def index():
    """ Simple healthcheck endpoint. """
    return jsonify({"ok": time.time()})


@flask_app.route("/webex-teams/camera", methods=["POST"])
def camera_listener():
    """
    Listening for camera messages to be sent from the Meraki dashboard, webhook listener

    Expects to receive JSON formatted data with the keys of:
      "type" (string): [arrival/departure] Represent the arrival/departing
      "parking_space" (integer): Parking space
      "time_elapsed" (float): Length of time that the car was parked
    """
    if request.method == "POST":
        # Check for the state of the vehicle
        if request.json["type"] == "arrival":
            content = f"Vehicle has arrived in Parking Space #{request.json['parking_space']}"
        elif request.json["type"] == "departure":
            content = f"Vehicle has departed from Parking Space #{request.json['parking_space']}"

        # Get the list of all rooms that the bot is joined to
        all_rooms = api.rooms.list()

        for room in all_rooms:
            if ROOM_NAME in room.title:
                # Send camera picture to the WebEx Teams chat as the bot
                api.messages.create(
                    roomId=room.id, markdown=f"## {content}"
                )

        return "OK"


@flask_app.route("/webex-teams/wireless-join", methods=["POST"])
def wifi_listener():
    """
    Listening for post messages for Wireless client join to guest SSID

    Expects to receive JSON formatted data with the keys of:
      "name" (string): Name of the person that has joined
      "email" (string): Email address of the person that has joined the network
      "order_num" (integer): Order number to process
      "dessert_pref" (string): Preference of a dessert
    """
    if request.method == "POST":
        # Set the name of the room from env variable
        room_name = os.environ.get("ROOM_NAME")

        if room_name is None:
            raise ValueError(
                "Please set environment variable for room name, 'export ROOM_NAME=<room_name>'"
            )

        # Get the list of all rooms that the bot is joined to
        all_rooms = api.rooms.list()
        rooms = [room.id for room in all_rooms if room_name in room.title]

        # Send the order information to the chat room
        content = (
            f"# Order {request.json['order_num']}\n"
            f"  Customer Name: {request.json['name']}<br>"
            f"  Preferred Dessert: {request.json['dessert_pref']}  "
        )
        api.messages.create(roomId=rooms[0], markdown=content)

        return "OK"


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5030)
