
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionExample(Action):
    def name(self):
        return "action_example"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="هذا مثال لأكشن مخصص.")
        return []
