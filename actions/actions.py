from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector

class ActionCheckAdmissionType(Action):
    def name(self) -> Text:
        return "action_check_admission_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        admission_type = tracker.get_slot("admission_type")
        
        if admission_type:
            # إذا كان نوع القبول موجودًا، لا تفعل شيئًا
            return []
        else:
            # إذا لم يكن نوع القبول موجودًا، اطلب من المستخدم تحديده
            dispatcher.utter_message(text="من فضلك، حدد نوع القبول (عام أو خاص).")
            return []

class ActionGetAdmissionFees(Action):
    def name(self) -> Text:
        return "action_get_admission_fees"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # استخراج نوع القبول من الفتحة (Slot)
        admission_type = tracker.get_slot("admission_type")

        if admission_type:
            # إذا تم تحديد نوع القبول، قم بالرد برسوم القبول
            fees = self.get_fees_from_db(admission_type)
            if fees:
                dispatcher.utter_message(text=f"رسوم التسجيل للنوع {admission_type} هي: {fees} ريال.")
            else:
                dispatcher.utter_message(text=f"عذرًا، لا توجد بيانات متاحة للنوع {admission_type}.")
        else:
            # إذا لم يتم تحديد نوع القبول، اطلب من المستخدم تحديده
            dispatcher.utter_message(text="من فضلك، حدد نوع القبول (عام أو خاص).")

        return []

    def get_fees_from_db(self, admission_type: Text) -> float:
        """
        استرداد رسوم التسجيل من قاعدة البيانات.
        """
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123",
                database="admission_db"
            )
            cursor = connection.cursor()

            # استعلام SQL
            query = "SELECT fees_amount FROM admission_fees WHERE admission_type=%s"
            cursor.execute(query, (admission_type,))
            result = cursor.fetchone()

            return result[0] if result else None

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()