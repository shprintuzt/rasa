# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import copy
import time

from rasa.core.actions import action
from rasa.core.actions.action import ActionDefaultAskAffirmation
from rasa.core.actions.two_stage_fallback import TwoStageFallbackAction
#from rasa.core.actions.two_stage_fallback import (
#    _last_intent_name,
#    _user_should_affirm
#)
from rasa.core.actions.loops import LoopAction
from rasa.core.channels import OutputChannel
from rasa.shared.core.domain import Domain
from rasa.shared.core.events import (
    Event,
    UserUtteranceReverted,
    ActionExecuted,
    UserUttered,
    ActiveLoop,
)
from rasa.core.nlg import NaturalLanguageGenerator
from rasa.shared.core.trackers import DialogueStateTracker, EventVerbosity
from rasa.shared.constants import DEFAULT_NLU_FALLBACK_INTENT_NAME
from rasa.shared.core.constants import (
    USER_INTENT_OUT_OF_SCOPE,
    ACTION_LISTEN_NAME,
    ACTION_DEFAULT_FALLBACK_NAME,
    ACTION_DEFAULT_ASK_AFFIRMATION_NAME,
    ACTION_DEFAULT_ASK_REPHRASE_NAME,
    ACTION_TWO_STAGE_FALLBACK_NAME,
    DEFAULT_ACTION_NAMES
)
from rasa.utils.endpoints import EndpointConfig

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
            try:
                howLong = int(entityList[0]["value"])
            except:
                return []

        response = "utter_vision_invalid" # default string
        if howLong >= 2 and howLong <= 7:
            response = "utter_vision_in_5_years"
        elif howLong <= 15:
            response = "utter_vision_in_10_years"
        elif howLong <= 30:
            response = "utter_vision_in_20_years"
        dispatcher.utter_message(template=response)
                     
        return []
        
class ActionIntroHobby(Action):

    def name(self) -> Text:
        return "action_intro_hobby"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # responses
        responses = ["utter_introduction",
                     "utter_hobby",
                     "utter_greeting"]
        for response in responses:
            dispatcher.utter_message(template=response)

        return []
