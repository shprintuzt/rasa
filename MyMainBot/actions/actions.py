# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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

class ActionVision(Action):

    def name(self) -> Text:
        return "action_vision"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entityList = tracker.latest_message["entities"]
        howLong = 0 # default value
        if len(entityList) != 0:
            howLong = int(entityList[0]["value"])

        response = "utter_vision_invalid" # default string
        if howLong >= 2 and howLong <= 7:
            response = "utter_vision_in_5_years"
        elif howLong <= 15:
            response = "utter_vision_in_10_years"
        elif howLong <= 30:
            response = "utter_vision_in_20_years"
        dispatcher.utter_message(template=response)
                     
        return []
