# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import json
from pathlib import Path
from typing import Any, Text, Dict, List ,Optional
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher ,Action
from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
from rasa_sdk import Tracker
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import AllSlotsReset, SlotSet
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.types import DomainDict

import requests

import pandas as pd
from fuzzywuzzy import fuzz # visit https://github.com/seatgeek/fuzzywuzzy for more details
from fuzzywuzzy import process

class GetAnswer(Action):
	def __init__(self):
		self.faq_data = pd.read_csv('/home/sagar24/rasa_csv/faq_data.csv')

	def name(self):
		return 'actions.GetAnswer'
		
	def run(self, dispatcher, tracker, domain):
		query =  tracker.latest_message['text']
		questions = self.faq_data['question'].values.tolist()

		mathed_question, score = process.extractOne(query, questions, scorer=fuzz.token_set_ratio) # use process.extract(.. limits = 3) to get multiple close matches

		if score > 50: # arbitrarily chosen 50 to exclude matches not relevant to the query
		    matched_row = self.faq_data.loc[self.faq_data['question'] == mathed_question,]
		    
		    document = matched_row['link'].values[0]
		    page = matched_row['page'].values[0]
		    match = matched_row['question'].values[0]
		    answer = matched_row['answers'].values[0]
		    response = "Here's something I found, \n\n Document: {} \n Page number: {} \n Question: {} \n Answer: {} \n".format(document, page, match, answer)

		else:
			response = "Sorry I couldn't find anything relevant to your query!"
						
		dispatcher.utter_message(response)

class ApiAnswer(Action):
	def name(self):
		return 'actions.ApiAnswer'
		
	def run(self, dispatcher, tracker, domain):
		response="Hello"
		response = requests.get(f"https://jsonplaceholder.typicode.com/todos/1")
		if response.status_code == 200:
			print("sucessfully fetched the data")
			print(str(response.json()))
		else:
			print(f"Hello person, there's a {response.status_code} error with your request")				
		response1=(str(response.json()))
		dispatcher.utter_message(response1)
