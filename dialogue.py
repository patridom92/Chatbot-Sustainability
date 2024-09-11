from intent import INTENT_LOOKUP
from Chatbot import *
import abc
class DialogueState:
    def __init__(self):
        self.intent = None
        self.current_node = StartNode()
        self.previous_node = None
        self.metrics = []

    def process_user_input(self, user_input, test_name):
        user_intent = None
        for intent, inputs in INTENT_LOOKUP.items():
            if user_input in inputs:
                user_intent = intent
        if not user_intent:
            raise IntentNotDeterminedException(test_name)
        self.intent = user_intent


class Node(abc.ABC):
    @abc.abstractmethod
    def say(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def transition(self, dialogue_state: DialogueState):
        raise NotImplementedError()