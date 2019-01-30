from typing import Dict, List, Text, Any

from rasa_core_sdk import Action, Tracker, ActionExecutionRejection
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from pprint import pprint


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


class ActionConfirm(Action):
    def name(self):
        return "action_confirm"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        color = next(tracker.get_latest_entity_values("COLOR"), None)
        qty = next(tracker.get_latest_entity_values("QTY"), None)
        print(color, qty)
        dispatcher.utter_template('utter_confirm', tracker)
        return [SlotSet("COLOR", color),
                SlotSet("QTY", qty)]


class ActionOrder(Action):
    def name(self):
        return "action_order"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ) -> List[Dict[str, any]]:
        qty = tracker.get_slot("QTY", 0)
        result = qty * 0.5
        return [SlotSet("PRICE_LIST", result)]


class ActionSubmit(Action):
    def name(self):
        return "action_submit"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ):
        # HTTP POST ...
        dispatcher.utter_template('utter_submit')
        return []


class CandyForm(FormAction):
    def name(self):
        return 'candy_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ['COLOR', 'QTY']

    def slot_mappings(self):
        return {
            'COLOR': self.from_entity(
                entity='COLOR',
                intent='inform',
            ),
            'QTY': self.from_entity(
                entity='QTY',
                intent='inform',
            )
        }

    @staticmethod
    def color_db():
        return ['red', 'green', 'blue',
                'สีแดง', 'สีเขียว', 'สีน้ำเงิน',
                'แดง', 'เขียว', 'น้ำเงิน']

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate(self,
                 dispatcher,  # : CollectingDispatcher
                 tracker,  # : Tracker
                 domain: Dict[Text, Any]) -> List[Dict]:
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)

        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))
        for slot, value in slot_values.items():
            if slot == 'COLOR':
                if value.lower() not in self.color_db():
                    pprint('>> utter_show_colors')
                    dispatcher.utter_template('utter_show_colors', tracker)

                    slot_values[slot] = None
            elif slot == 'QTY':
                if not self.is_int(value) or int(value) <= 0:
                    pprint('>> utter_wrong_qty')
                    dispatcher.utter_template('utter_wrong_qty',
                                              tracker)
                    slot_values[slot] = None
                # else:
                #     slot_values[slot] = int(value)

        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self, dispatcher, tracker, domain) -> List[Dict]:
        dispatcher.utter_template('utter_submit', tracker)
        return []
