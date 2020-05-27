from . import routes
import os
from flask import Blueprint
from webexteamssdk import WebexTeamsAPI

# Define the Flask blue print
webex_teams_blueprint = Blueprint("webex_teams_blueprint", __name__)

# Set the API ACCESS TOKEN
WEBEX_TEAMS_ACCESS_TOKEN = os.environ["WEBEX_TEAMS_ACCESS_TOKEN"]

# Create an API object
webex_teams_api = WebexTeamsAPI()

# Routes need to be loaded after Blueprint
from . import routes
