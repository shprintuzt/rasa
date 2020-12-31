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

### new default actions ###

#old_default_actions = action.default_actions
#def new_default_actions(action_endpoint: Optional[EndpointConfig] = None) -> List["Action"]:
#    default_action_list = old_default_actions(action_endpoint)
#    new_default_list = [
#        ActionCustomDefaultAskAffirmation(),
#        ActionCustomTwoStageFallback()
#    ]
#    default_action_list += new_default_list
#
#    return default_action_list
#action.default_actions = new_default_actions
#
#class ActionCustomDefaultAskAffirmation(Action):
#    """Default implementation which asks the user to affirm his intent.
#
#    It is suggested to overwrite this default action with a custom action
#    to have more meaningful prompts for the affirmations. E.g. have a
#    description of the intent instead of its identifier name.
#    """
#
#    def name(self) -> Text:
#        return "action_custom_default_ask_affirmation"
#
#    async def run(
#        self,
#        output_channel: "OutputChannel",
#        nlg: "NaturalLanguageGenerator",
#        tracker: "DialogueStateTracker",
#        domain: "Domain",
#    ) -> List[Event]:
#        intent_to_affirm = tracker.latest_message.intent.get(INTENT_NAME_KEY)
#
#        intent_ranking = tracker.events[-1].parse_data.get(INTENT_RANKING_KEY, [])
#
#        # nlu_fallback intent is replaced with the other intent
#        if (
#            intent_to_affirm == DEFAULT_NLU_FALLBACK_INTENT_NAME
#            and len(intent_ranking) > 1
#        ):
#            intent_to_affirm = intent_ranking[1][INTENT_NAME_KEY]
#        elif (
#            intent_to_affirm == DEFAULT_NLU_FALLBACK_INTENT_NAME
#            and len(intent_ranking) <= 1
#        ):
#            intent_to_affirm = "ask_study"
#
#        affirmation_message = f"質問の意図は「'{intent_to_affirm}'」、とでよろしいでしょうか？"
#        message = {
#            "text": affirmation_message,
#            "buttons": [
#                {"title": "Yes", "payload": f"/{intent_to_affirm}"},
#                {"title": "No", "payload": f"/{USER_INTENT_OUT_OF_SCOPE}"},
#            ],
#            "template_name": self.name(),
#        }
#
#        dispatcher.utter_message(json_message = message)
#
#
#        return []
#

#DEFAULT_ACTION_NAMES.append("action_custom_two_stage_fallback")
#

#class ActionCustomTwoStageFallback(Action):
#    def name(self) -> Text:
#        return "action_custom_two_stage_fallback"
#
#    async def _ask_affirm(
#        self,
#        output_channel: OutputChannel,
#        nlg: NaturalLanguageGenerator,
#        tracker: DialogueStateTracker,
#        domain: Domain,
#    ) -> List[Event]:
#        affirm_action = action.action_from_name(
#            "action_custom_default_ask_affirmation",
#            self._action_endpoint,
#            domain.user_actions,
#        )
#
#        return await affirm_action.run(output_channel, nlg, tracker, domain)

#class ActionCustomTwoStageFallback(LoopAction):
#    def __init__(self, action_endpoint: Optional[EndpointConfig] = None) -> None:
#        self._action_endpoint = action_endpoint
#
#    def name(self) -> Text:
#        return "action_custom_two_stage_fallback"
#
#    async def do(
#        self,
#        output_channel: "OutputChannel",
#        nlg: "NaturalLanguageGenerator",
#        tracker: "DialogueStateTracker",
#        domain: "Domain",
#        events_so_far: List[Event],
#    ) -> List[Event]:
#        if _user_should_affirm(tracker, events_so_far):
#            return await self._ask_affirm(output_channel, nlg, tracker, domain)
#
#        return await self._ask_rephrase(output_channel, nlg, tracker, domain)
#
#    async def _ask_affirm(
#        self,
#        output_channel: OutputChannel,
#        nlg: NaturalLanguageGenerator,
#        tracker: DialogueStateTracker,
#        domain: Domain,
#    ) -> List[Event]:
#        affirm_action = action.action_from_name(
#            "action_custom_default_ask_affirmation",
#            self._action_endpoint,
#            domain.user_actions,
#        )
#
#        return await affirm_action.run(output_channel, nlg, tracker, domain)
#
#    async def _ask_rephrase(
#        self,
#        output_channel: OutputChannel,
#        nlg: NaturalLanguageGenerator,
#        tracker: DialogueStateTracker,
#        domain: Domain,
#    ) -> List[Event]:
#        rephrase = action.action_from_name(
#            ACTION_DEFAULT_ASK_REPHRASE_NAME, self._action_endpoint, domain.user_actions
#        )
#
#        return await rephrase.run(output_channel, nlg, tracker, domain)
#
#    async def is_done(
#        self,
#        output_channel: "OutputChannel",
#        nlg: "NaturalLanguageGenerator",
#        tracker: "DialogueStateTracker",
#        domain: "Domain",
#        events_so_far: List[Event],
#    ) -> bool:
#        _user_clarified = _last_intent_name(tracker) not in [
#            DEFAULT_NLU_FALLBACK_INTENT_NAME,
#            USER_INTENT_OUT_OF_SCOPE,
#        ]
#        return (
#            _user_clarified
#            or _two_fallbacks_in_a_row(tracker)
#            or _second_affirmation_failed(tracker)
#        )
#
#    async def deactivate(
#        self,
#        output_channel: "OutputChannel",
#        nlg: "NaturalLanguageGenerator",
#        tracker: "DialogueStateTracker",
#        domain: "Domain",
#        events_so_far: List[Event],
#    ) -> List[Event]:
#        if _two_fallbacks_in_a_row(tracker) or _second_affirmation_failed(tracker):
#            return await self._give_up(output_channel, nlg, tracker, domain)
#
#        return await self._revert_fallback_events(
#            output_channel, nlg, tracker, domain, events_so_far
#        ) + _message_clarification(tracker)
#
#    async def _revert_fallback_events(
#        self,
#        output_channel: OutputChannel,
#        nlg: NaturalLanguageGenerator,
#        tracker: DialogueStateTracker,
#        domain: Domain,
#        events_so_far: List[Event],
#    ) -> List[Event]:
#        revert_events = [UserUtteranceReverted(), UserUtteranceReverted()]
#
#        temp_tracker = DialogueStateTracker.from_events(
#            tracker.sender_id, tracker.applied_events() + events_so_far + revert_events
#        )
#
#        while temp_tracker.latest_message and not await self.is_done(
#            output_channel, nlg, temp_tracker, domain, []
#        ):
#            temp_tracker.update(revert_events[-1])
#            revert_events.append(UserUtteranceReverted())
#
#        return revert_events
#
#    async def _give_up(
#        self,
#        output_channel: OutputChannel,
#        nlg: NaturalLanguageGenerator,
#        tracker: DialogueStateTracker,
#        domain: Domain,
#    ) -> List[Event]:
#        fallback = action.action_from_name(
#            ACTION_DEFAULT_FALLBACK_NAME, self._action_endpoint, domain.user_actions
#        )
#
#        return await fallback.run(output_channel, nlg, tracker, domain)
#
#
#def _last_intent_name(tracker: DialogueStateTracker) -> Optional[Text]:
#    last_message = tracker.latest_message
#    if not last_message:
#        return None
#
#    return last_message.intent.get("name")
#
#
#def _two_fallbacks_in_a_row(tracker: DialogueStateTracker) -> bool:
#    return _last_n_intent_names(tracker, 2) == [
#        DEFAULT_NLU_FALLBACK_INTENT_NAME,
#        DEFAULT_NLU_FALLBACK_INTENT_NAME,
#    ]
#
#
#def _last_n_intent_names(
#    tracker: DialogueStateTracker, number_of_last_intent_names: int
#) -> List[Text]:
#    intent_names = []
#    for i in range(number_of_last_intent_names):
#        message = tracker.get_last_event_for(
#            UserUttered, skip=i, event_verbosity=EventVerbosity.AFTER_RESTART
#        )
#        if isinstance(message, UserUttered):
#            intent_names.append(message.intent.get("name"))
#
#    return intent_names
#
#
#############################################
#def _user_should_affirm(
#    tracker: DialogueStateTracker, events_so_far: List[Event]
#) -> bool:
##    fallback_was_just_activated = any(
##        isinstance(event, ActiveLoop) for event in events_so_far
##    )
##    if fallback_was_just_activated:
##        return True
#
#    intent_ranking = tracker.latest_message.intent.get(INTENT_RANKING_KEY, [])
#    if (
#        _last_intent_name(tracker) == DEFAULT_NLU_FALLBACK_INTENT_NAME
#        and len(intent_ranking) <= 1
#    ):
#        return False
#    if (
#        _last_intent_name(tracker) == DEFAULT_NLU_FALLBACK_INTENT_NAME
#        and intent_ranking[1] in [
#            DEFAULT_NLU_FALLBACK_INTENT_NAME,
#            USER_INTENT_OUT_OF_SCOPE
#        ]
#    ):
#        return False
#
#    return True
#
#
#def _second_affirmation_failed(tracker: DialogueStateTracker) -> bool:
#    return _last_n_intent_names(tracker, 3) == [
#        USER_INTENT_OUT_OF_SCOPE,
#        DEFAULT_NLU_FALLBACK_INTENT_NAME,
#        USER_INTENT_OUT_OF_SCOPE,
#    ]
#
#
#def _message_clarification(tracker: DialogueStateTracker) -> List[Event]:
#    clarification = copy.deepcopy(tracker.latest_message)
#    clarification.parse_data["intent"]["confidence"] = 1.0
#    clarification.timestamp = time.time()
#    return [ActionExecuted(ACTION_LISTEN_NAME), clarification]
