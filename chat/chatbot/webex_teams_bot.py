import json
import re
import requests
import os
import logging
import time
from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
import requests_mock


flask_app = Flask(__name__)

api = WebexTeamsAPI()
LOGGER = logging.getLogger("ChatBotApp")

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

# Get the list of all rooms that the bot is joined to
ALL_ROOMS = api.rooms.list()

API_CALLS = [
    {
        "fixture_path": f"{os.getcwd()}/mocks/fixtures/api_client1.json",
        "url": "https://sandbox.purpleportal.net/api/company/v1/venue/821/visitor/127",
        "method": "get",
    },
    {
        "fixture_path": f"{os.getcwd()}/mocks/fixtures/api_client2.json",
        "url": "https://sandbox.purpleportal.net/api/company/v1/venue/821/visitor/135",
        "method": "get",
    },
    {
        "fixture_path": f"{os.getcwd()}/mocks/fixtures/api_client3.json",
        "url": "https://sandbox.purpleportal.net/api/company/v1/venue/821/visitor/122",
        "method": "get",
    },
    {
        "fixture_path": f"{os.getcwd()}/mocks/fixtures/api_client4.json",
        "url": "https://sandbox.purpleportal.net/api/company/v1/venue/821/visitor/2161",
        "method": "get",
    },
    {
        "fixture_path": f"{os.getcwd()}/mocks/fixtures/api_client5.json",
        "url": "https://sandbox.purpleportal.net/api/company/v1/venue/821/visitor/123162",
        "method": "get",
    },
    {
        "fixture_path": f"{os.getcwd()}/mocks/fixtures/api_client6.json",
        "url": "https://sandbox.purpleportal.net/api/company/v1/venue/821/visitor/32623",
        "method": "get",
    },
    {
        "fixture_path": f"{os.getcwd()}/mocks/fixtures/api_client7.json",
        "url": "https://sandbox.purpleportal.net/api/company/v1/venue/821/visitor/203633",
        "method": "get",
    },
    {
        "fixture_path": f"{os.getcwd()}/mocks/fixtures/api_client8.json",
        "url": "https://sandbox.purpleportal.net/api/company/v1/venue/821/visitor/43236",
        "method": "get",
    },
]


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
            content = (
                f"Vehicle has arrived in Parking Space #{request.json['parking_space']}"
            )
        elif request.json["type"] == "departure":
            content = f"Vehicle has departed from Parking Space #{request.json['parking_space']} seconds"

        for room in ALL_ROOMS:
            if ROOM_NAME in room.title:
                # Send camera picture to the WebEx Teams chat as the bot
                response = api.messages.create(roomId=room.id, markdown=f"## {content}")
                LOGGER.info(response)

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
        # Get the UserID for Purple
        user_id = request.json["user"]["id"]

        # Set the Location ID from the JSON data
        site_id = request.json["user"]["venue"]["id"]

        # Get the Visit Count
        visit_count = request.json["user"]["visitCountsForVenue"]

        # Get name
        customer_name = (
            f"{request.json['user']['firstName']} {request.json['user']['lastName']}"
        )

        # Setup Mock
        with requests_mock.Mocker() as m:
            for api_call in API_CALLS:
                with open(api_call["fixture_path"], "r") as f:
                    data = f.read()

                if api_call["method"] == "get":
                    m.get(api_call["url"], text=data)
                    continue

            # Get order number from API

            # Get car color ID from the Purple API
            resp = requests.get(
                url=f"https://sandbox.purpleportal.net/api/company/v1/venue/{site_id}/visitor/{user_id}"
            )

            data = resp.json()

            print(data["data"]["user"][0]["form_data"][0]["response"])

            # Send the order information to the chat room
            content = (
                f"# New Arrival to WiFi\n"
                f"  Customer Name: {customer_name}<br>"
                f"  Car Color: {data['data']['user'][0]['form_data'][0]['response']}"
            )

        for room in ALL_ROOMS:
            if ROOM_NAME in room.title:
                response = api.messages.create(roomId=room.id, markdown=content)
                LOGGER.info(response)

        return "OK"


@flask_app.route("/webex-teams/update-order", methods=["POST"])
def update_order():
    """
    Customer Name, Order ID, Spot Number

    Client has <order number> in car spot
    """
    if request.method == "POST":
        content = (
            f" # Order Update - {customerName}\n"
            f"    Order Number: {orderNumber}\n"
            f"    Parking Spot: {spotNumber}"
        )

        for room in ALL_ROOMS:
            if ROOM_NAME in room.title:
                # Send camera picture to the WebEx Teams chat as the bot
                response = api.messages.create(roomId=room.id, markdown=content)
                LOGGER.info(response)

        return "OK"


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5030)
