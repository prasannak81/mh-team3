def update(_id, obj):
  if "_orderready" in obj
    trigger = obj.pop("_orderready")
    webex_team_order_update(obj["orderNumber"], _id, trigger["customerName"])


def webex_team_order_update(orderNumber, spotNumber, customerName):
    team_url = os.environ.get("CHATBOT_URL", "http://chatbot")
    url = team_url + "/webex-teams/update-order"
    try:
        response = requests.post(
            url,
            headers={"Content-type": "application/json"},
            data={orderNumber: orderNumber, spotNumber: spotNumber, customerName: customerName},
        )
        print(response)
    except Exception as e:
        print(e)