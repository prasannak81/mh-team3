import time
import re
import json
import yaml
from random import randint

# from urllib import quote_plus
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestsMethod(object):
    @staticmethod
    def method(method, url, verify_ssl=False, headers=None, params=None):
        methods = {"get": requests.get, "post": requests.post}

        if not params:
            params = dict()

        # print url
        requests_method = methods.get(method)
        try:
            response = requests_method(
                url, headers=headers, params=params, verify=verify_ssl
            )
            # print response
            if response.status_code:
                # print(response.status_code)
                if response.status_code != 200:
                    raise ValueError("Error: mvsense not accessible.")
                elif len(response.json()) <= 0:
                    raise ValueError("Error: Wrong api-key.")
                else:
                    return response.json()
            else:
                return response.text
        # except PswNotFoundException as error:
        except ValueError as error:
            # print error
            return error
        except Exception as excp:
            # print excp
            return excp


class MerakiClientApp:
    def __init__(self):
        # super(MerakiClientApp, self).__init__()
        self._api_ext = "api/v0"
        self.url = "https://api.meraki.com"
        self.verify_ssl = False

        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _get(self, endpoint, headers, params=None, *args, **kwargs):
        api_url = "/".join((self.url, self._api_ext, endpoint))
        return RequestsMethod.method("get", api_url, self.verify_ssl, headers, params)

    def _post(self, endpoint, headers, params=None, *args, **kwargs):
        api_url = "/".join((self.url, self._api_ext, endpoint))
        return RequestsMethod.method("post", api_url, self.verify_ssl, headers, params)

    def get(self, *args, **kwargs):
        return self._get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self._post(*args, **kwargs)


class MVSenseAPI(MerakiClientApp):
    def __init__(self, api_key, serial, interval=30, zone_count=4):
        self._api_endpoint = "devices"
        self.api_key = api_key
        self.serial = serial
        self.zone_count = zone_count
        self.interval = interval
        self.rest_client = MerakiClientApp()

    # def query_mvsense(self, serial, query_url, **kwargs):
    def query_mvsense(self, query_url, **kwargs):
        real_endpoint = "{0}/{1}/{2}".format(self._api_endpoint, self.serial, query_url)
        params = {}

        self._headers = {
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        return self.rest_client._get(
            real_endpoint, headers=self._headers, params=params, **kwargs
        )

    def simulate_api_return_feed(self):
        result = []
        if self.zone_count == None:
            self.zone_count = randint(0, 5)
        simulated_data = {"zoneId": 0, "entrances": 0, "startTs": "", "endTs": ""}
        tsnow = time.time()
        ts_start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(tsnow - 60))
        ts_end = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(tsnow))
        for zone in range(self.zone_count):
            entrances = randint(0, 1)
            result.append(
                {
                    "zoneId": zone,
                    "entrances": entrances,
                    "startTs": ts_start,
                    "endTs": ts_end,
                }
            )
        return result


def webex_team_post(url, camera_feed):
    # url="http://10.0.1.4:5030/webex-teams/camera"
    url = url + "/webex-teams/camera"
    try:
        response = requests.post(
            url,
            headers={"Content-type": "application/json"},
            data=json.dumps(camera_feed),
        )
        print(response)
    except Exception as e:
        print(e)


def main():
    api_key = os.environ.get("MVSENSOR_API_KEY")
    serial = os.environ.get("MVSENSOR_SERIAL")
    team_url = os.environ.get("MV_SENSOR_WEBHOOK_URL")
    zone_count = os.environ.get("MV_SENSOR_ZONE_COUNT", 4)
    interval = os.environ.get("MV_SENSOR_INTERVAL", 30)
    search_obj = MVSenseAPI(api_key, serial, zone_count, interval)
    ## Analytics zoners recent
    error_str = "Error:(.*)"
    pattern = re.compile(error_str)
    posted = {}
    zoneIdMap = {"566327653141839970": 2, "566327653141839971": 3}
    while True:
        result = search_obj.query_mvsense("camera/analytics/recent")
        if pattern.match(str(result)):
            result = search_obj.simulate_api_return_feed()
            # print result
            # break
        if len(result) > 0:
            tsnow = time.time()
            if search_obj.zone_count == None:
                search_obj.zone_count = len(result)
            for zone in result:
                # print(zone['zoneId'],zone['entrances'], zone['startTs'], zone['endTs'])
                if str(zone["zoneId"]) in zoneIdMap:
                    zoneId = zoneIdMap[str(zone["zoneId"])]
                else:
                    zoneId = zone["zoneId"] + 1
                print(zoneId, zone["entrances"], zone["startTs"], zone["endTs"])
                # if zone['entrances'] > 0:
                if zone["entrances"] == 1 or zone["entrances"] > 10:
                    if zoneId in posted:
                        print("A vehicle detection has already been posted for", zoneId)
                    else:
                        print("A new vehical has arrived in zoneId = ", zoneId)
                        ## post this json to webhook
                        posted[zoneId] = {
                            "type": "arrival",
                            "parking_space": zoneId,
                            "count": zone["entrances"],
                            "startTs": zone["startTs"],
                            "endTs": zone["endTs"],
                            "enteredTs": tsnow,
                        }
                        print(posted)
                        webex_team_post(team_url, posted[zoneId])
                        # post_to_webhook()
                else:
                    if zoneId in posted:
                        enteredTime = posted[zoneId]["enteredTs"]
                        timespent = tsnow - enteredTime
                        if timespent > 90:
                            print("A vehical has left the zoneId = ", zoneId)
                            ## post this message to webhook
                            departure = {
                                "type": "departure",
                                "parking_space": zoneId,
                                "count": zone["entrances"],
                                "startTs": posted[zoneId]["startTs"],
                                "endTs": zone["endTs"],
                                "time_elaspsed": timespent,
                            }
                            print(departure)
                            webex_team_post(team_url, departure)
                            posted.pop(zoneId)
            print(
                "-----------------------------------------------------------------------------------------------------------\n"
            )
        time.sleep(search_obj.interval)
    ## Analytics zoners live
    # result = search_obj.query_mvsense('Q2GV-7HEL-HC6C','camera/analytics/live')
    # print result


if __name__ == "__main__":
    main()
