# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import smtplib
from dotenv import load_dotenv, find_dotenv
import os
import re


from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ActionSendContactInfo(Action):

    def name(self) -> Text:
        return "action_send_contact_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get value from slots
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        phone = tracker.get_slot("phone")

        # create message
        body = f"Please contact {name} via {email} or {phone}!"

        # load env variables
        load_dotenv(find_dotenv())

        # send message
        
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_PASSWORD')

        sent_from = gmail_user
        to = [os.getenv('SEND_MAIL_TO')]
        subject = "Chatbot lead"

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(gmail_user, gmail_password)
            smtp_server.sendmail(sent_from, to, email_text)
            smtp_server.close()
            print ("Email sent successfully!")
        except Exception as ex:
            print ("Something went wrong….",ex)


        return []


class ValidateContactInfoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_get_contact_form"

    def clean_name(self, name):
        return "".join([c for c in name if c.isalpha()])

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        name = self.clean_name(slot_value)
        if len(name) == 0:
            dispatcher.utter_message(text="There must have been a typo.")
            return {"name": None}
        return {"name": name}


    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, slot_value)):
            return {"email": slot_value}
        dispatcher.utter_message(text="There must have been a typo. Email is not valid.")
        return {"email": None}


    def validate_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        regex = r'(\+\d{2,3} ?)?(\d{2,3}){1} ?(\d{3,4}) ?(\d{3,4})'
        if re.fullmatch(regex, slot_value):
            return {"phone": slot_value}
        dispatcher.utter_message(text="There must have been a typo. Phone is not valid.")
        return {"phone": None}
