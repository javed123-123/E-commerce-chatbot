# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json

# Sample Tracking / Order ids to use - 20265, D1001, D1004, 20637, 20546, 21078, 21057, F1004, F1003
# Order Number / Tracking Number, extracted via Rasa
def extract_shipment_details(tr_no):
    # tr_no = ''
    url = "https://app.eshipz.com/track-widget/73d3c1bb-c1f7-4e3b-8baf-7243b9b31ac1"
    payload = {"q_num": "{}".format(tr_no)}
    print(url)
    headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers).json()
    return response

class ActionOrderNo(Action):

    def name(self):
        return "action_fetch_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:

        dispatcher.utter_message("Give me a second to fetch the details...")
        response=extract_shipment_details(tracker.latest_message['text'])
        details=str(response)
        dispatcher.utter_message(details+' (info: Empty curly brackets means no such orderNo exists)')
        return[SlotSet('orderNo',tracker.latest_message['text'])]