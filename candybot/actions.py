from typing import Dict, List

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet


class ActionListColor(Action):
    def name(self) -> str:
        return "action_list_colors"

    def run(self,
            dispatcher,  # type: CollectingDispatcher
            tracker,  # type: Tracker
            domain  # type:  Dict[Text, Any]
            ) -> List[Dict[str, any]]:
        result = ['red', 'green', 'blue']
        return [SlotSet("matches", result if result is not None else [])]
