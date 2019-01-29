from typing import Dict, List, Text

from rasa_core_sdk import Action, Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import FormAction


class ActionListColor(Action):
    """
    Retrieve the values from the external
    """
    def name(self) -> str:
        return "action_list_colors"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ) -> List[Dict[str, any]]:
        result = ['white', 'red', 'black']
        return [SlotSet("COLOR_LIST", result)]


class ActionListPricing(Action):
    def name(self) -> str:
        return "action_list_pricing"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ) -> List[Dict[str, any]]:
        result = ['0.5', '0.6', '0.7']
        return [SlotSet("PRICE_LIST", result)]


class CandyForm(FormAction):
    def name(self):
        return 'candy_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ['color']

    def slot_mappings(self):
        return {
            'color': [self.from_entity(entity='color',
                                       not_intent=['chitchat', 'bargain']),
                      self.from_entity(entity='color',
                                       intent='inform',
                                       not_intent=['chitchat', 'bargain'])]
        }

    def submit(self, dispatcher, tracker, domain) -> List[Dict]:
        dispatcher.utter_template('utter_submit', tracker)
