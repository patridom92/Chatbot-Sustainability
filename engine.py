import abc
import yaml

class IntentNotDeterminedException(Exception):
    """Raised when the input value is too small"""
    def __init__(self, message):
        self.message = message
        super().__init__(f"Error in: {message}")


class UtterancesNotEqualException(Exception):
    """Raised when saved and expected utterances are not equal"""
    def __init__(self, message):
        self.message = message
        super().__init__(f"Error in: {message}")


class TransitionException(Exception):
    """Raised when saved and expected utterances are not equal"""
    def __init__(self, message):
        self.message = message
        super().__init__(f"Looks like transition is broken in: {message}")


class MetricsNotEqualException(Exception):
    """Raised when saved and expected metrics are not equal"""
    pass

from Chatbot import *
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
    
class Conversation:
    def __init__(self):
        self.utterances = []
        self.metrics = []

    def add_turn(self, utterance):
        self.utterances.append(utterance)


if __name__ == '__main__':
    with open(r'conversations.yaml') as file:
        test_conversations = yaml.load(file, Loader=yaml.FullLoader)

    for name, test_conversation in test_conversations.items():
        chat = test_conversation['chat'].copy()
        dialogue_context = DialogueState()
        conversation = Conversation()

        while type(dialogue_context.current_node) != GoodbyeNode:
            node = dialogue_context.current_node

            try:
                utterance = node.say()
            except:
                raise TransitionException(name)

            chat.pop(0)
            conversation.add_turn(utterance)

            user_input = chat[0]
            chat.pop(0)

            conversation.add_turn(user_input)
            dialogue_context.process_user_input(user_input, name)

            dialogue_context.current_node = node.transition(dialogue_context)

        conversation.add_turn(dialogue_context.current_node.say())
        conversation.metrics = dialogue_context.metrics

        # check if conversations are the same
        for ind, expected_utterance in enumerate(test_conversation['chat']):
            saved_utterance = conversation.utterances[ind]
            if saved_utterance != expected_utterance:
                print(f"Utterances for conversation {name} are incorrect:\n"
                      f"{saved_utterance}!={expected_utterance}")
                raise UtterancesNotEqualException(name)

        # check if metrics are the same
        if 'metrics' in test_conversation:
            if len(conversation.metrics) != len(test_conversation['metrics']):
                print(conversation.metrics)
                print(f"Metrics for conversation {name} are incorrect")
                raise MetricsNotEqualException()
            for ind, expected_metric in enumerate(test_conversation['metrics']):
                saved_metric = conversation.metrics[ind]
                if saved_metric != expected_metric:
                    print(f"Metrics for conversation {name} are incorrect:\n"
                          f"{saved_metric}!={expected_metric}")
                    raise MetricsNotEqualException()
        print(f"Test for conversation {name} passed correctly.")
    print("All tests passed correctly")