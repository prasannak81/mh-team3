import os
import logging

import requests


log = logging.getLogger("quickpickup.order_ready")


def update(_id, obj):
    """
    Update hook for 'spots' objects.

    Args:
        _id: Object ID
        obj: Mutable object dictionary

    """
    if "_orderready" in obj:
        trigger = obj.pop("_orderready")
        webex_team_order_update(obj["orderNumber"], _id, trigger["customerName"])


def webex_team_order_update(order_number, spot_number, customer_name):
    """
    Make a request to the chatbot to post a message.

    Args:
        order_number: Number of the updated order
        spot_number: The parking spot the customer is in
        customer_name: The customer's name

    """
    team_url = os.environ.get("CHATBOT_URL", "http://chatbot:5030")
    url = team_url + "/webex-teams/update-order"
    try:
        response = requests.post(
            url,
            headers={"Content-type": "application/json"},
            json={
                "orderNumber": order_number,
                "spotNumber": spot_number,
                "customerName": customer_name,
            },
        )
        log.debug(response)
    except Exception as err:
        log.exception(err)
