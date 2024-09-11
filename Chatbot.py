import difflib
from intent import INTENT_LOOKUP
from engine import DialogueState, Node

class DialogueState:
    def __init__(self, intent=None, location=None):
        self.intent = intent
        self.location = location
        self.metrics = []
        self.topic = None

def set_intent(self, user_input):
        closest_match = None
        highest_similarity = 0
        
        # Loop through intents and utterances to find the closest match
        for intent, utterances in INTENT_LOOKUP.items():
            for utterance in utterances:
                similarity = difflib.SequenceMatcher(None, user_input, utterance).ratio()
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    closest_match = intent
        
        # If similarity is above a threshold (e.g., 0.6), consider it a match
        if highest_similarity > 0.6:
            self.intent = closest_match
        else:
            self.intent = None  # No close match found

class Node:
    """Base class for all chatbot nodes."""
    def say(self):
        pass

    def transition(self, dialogue_state: DialogueState):
        pass
    

class StartNode(Node):
    """Starting point of the conversation."""
    def say(self):
        return "Hiya. Welcome to 'Say aye to Sustainability'. My name is Fergus, and I am here to help you become more sustainable. I can show you sustainability events and shops where you can buy local products in your area, sustainable businesses from our beautiful Scotland, and give you some sustainability tips. What can I do for you today?"

    def transition(self, dialogue_state: DialogueState):
        if dialogue_state.intent == "EVENTS":
            return EventRecommendationNode()
        elif dialogue_state.intent == "FAQ":
            return FAQNode()
        elif dialogue_state.intent == "LOCAL_BUSINESSES":
            return LocalRecommendationNode()
        elif dialogue_state.intent == "TOPIC_ENERGY":
            dialogue_state.topic = "energy"
            return FAQNode()
        elif dialogue_state.intent == "TOPIC_PLASTICS":
            dialogue_state.topic = "plastics"
            return FAQNode()
        elif dialogue_state.intent == "TOPIC_RECYCLING":
            dialogue_state.topic = "recycling"
            return FAQNode()
        elif dialogue_state.intent == "BUSINESS_HOTEL":
            return HotelNode()
        elif dialogue_state.intent == "TOPIC_LOCHRANZA":
            dialogue_state.topic = "Lochranza"
            return RestaurantNode()
        elif dialogue_state.intent == "TOPIC_BURMIESTON":
            dialogue_state.topic = "Burmieston"
            return RestaurantNode()
        elif dialogue_state.intent == "BUSINESS_RESTAURANT":
            return RestaurantNode()
        elif dialogue_state.intent == "TOPIC_MHARSANTA":
            dialogue_state.topic = "Mharsanta"
            return RestaurantNode()
        elif dialogue_state.intent == "TOPIC_LOCH":
            dialogue_state.topic = "Loch Arthur Farm Shop and Café"
            return RestaurantNode()
        elif dialogue_state == "DENY":
            return DenyNode()
        elif dialogue_state.intent == "GOODBYE":
            return GoodbyeNode()
        else:
            return ClarificationNode()  #If the input is not part of the intent_lookup, a message will come up asking for clarification.

#To do: 
# 1. Create the remaining nodes (Events and local businesses - See about the APIS).
# 2. Add more utterances to the topics' intents.
# 3.Test the chatbot.
# 4. See about the deployment.



class FAQNode(Node):
    """Answers frequently asked questions about sustainability."""
    FAQ_RESPONSES = {
        "energy": "To conserve energy, try using LED bulbs, unplugging devices when not in use, and utilizing natural light",
        "plastics": "Reducing single-use plastics can be done by carrying reusable bags, bottles, and containers",
        "recycling": "Proper recycling involves cleaning recyclables, separating materials, and avoiding contaminants like plastic bags"
    }

    def say(self):
        # Check if a specific topic is asked
        if dialogue_state.topic in self.FAQ_RESPONSES:
            return self.FAQ_RESPONSES[dialogue_state.topic]
        # Default response for general sustainability questions
        return "To be more eco-friendly, try reducing single-use plastics, conserving energy, recycling properly, and buying from local businesses near you. Choosing a local company over a chain can have a very positive impact on the environment. It decreases carbon emissions, pollution, and waste. Is there anything else I can do for you?"

    def transition(self, dialogue_state: DialogueState):
        return StartNode()  #transition back to the StartNode
    

class ClarificationNode(Node):
    """Asks the user for clarification if input is not recognized."""
    def say(self):
        return "Sorry. I need more time to understand everything you say. Could you clarify or rephrase?"

    def transition(self, dialogue_state: DialogueState):
        return StartNode()  # After asking for clarification, transition back to the StartNode

class GoodbyeNode(Node):
    """Says goodbye to the user before the conversation finishes"""
    def say(self):
        return "I hope I helped you with the journey of becoming more sustainable. And remember, it is the wee steps that count! Do not hesitate to come back for more sustainable tips. Mòran taing!"
    def transition(self, dialogue_state: DialogueState):
        """Will not be called, finishes the conversation"""

class DenyNode(Node):
    """Says goodbye to the user before the conversation finishes"""
    def say(self):
        return "Awright. Do not hesitate to come back for more sustainable tips. And remember, it is the wee steps that count! Mòran taing!"
    def transition(self, dialogue_state: DialogueState):
        """Will not be called, finishes the conversation"""    

class RestaurantNode(Node):
    """Answers frequently asked questions about sustainability."""
    RESTAURANT_RESPONSES = {
        "Mharsanta": "This restaurant works closely with local food and drink suppliers including Macsween Haggis, Graham's Dairy and The Fish People. They have also switched their takeaway orders to smarter packaging, made from extractions of juice and sugarcane",
        "Loch Arthur Farm Shop and Café": "'Loch Arthur' is part of a working community that looks after people with learning disabilities, many of whom work in the bustling café and shop. Everything served and on display is made using the finest organic ingredients, grown and reared on the farm, or sourced locally"
    }

    def say(self):
        # Check if a specific topic is asked
        if dialogue_state.topic in self.RESTAURANT_RESPONSES:
            return self.RESTAURANT_RESPONSES[dialogue_state.topic]
        # Default response for general questions
        return "I have a couple of sustainable restaurants that you may like, 'Mharsanta', located in Glasgow, and 'Loch Arthur Farm Shop and Café', located in Dumfries. Would you like to know more about one of them?"

    def transition(self, dialogue_state: DialogueState):
        return StartNode()  #transition back to the StartNode
    
class HotelNode(Node):
    """Answers questions about specific sustainable accomodation."""
    HOTEL_RESPONSES = {
        "Burmieston": "The Burmieston Farm's passion for sustainability goes beyond its buildings. It uses recycled plastic and sheep's wool for insulation and biomass and solar energy systems. The rooms are beautifully furnished with antiques and 'upcycled' furniture, while outside boxes for bats, owls and hedgehogs help support the wildlife",
        "Lochranza": "Set in a spacious clearing surrounded by dramatic glens, Lochranza is one of the most picturesque spots in Scotland to pitch a tent. You can also stay in one of the insulated pods. It has a 100% green energy tariff, and has taken steps to boost the biodiversity of the area so that it's teeming with red deer, birds, wildflowers, bees and red squirrels"
    }

    def say(self):
        # Check if a specific topic is asked
        if dialogue_state.topic in self.HOTEL_RESPONSES:
            return self.HOTEL_RESPONSES[dialogue_state.topic]
        # Default response for general questions
        return "I have two places that offer sustainable accomodation that you may find interesting, 'Lochranza Campsite', located in Arran, and 'Burmieston Steading', located in Perthshire. Which one would you like to know more about?"

    def transition(self, dialogue_state: DialogueState):
        return StartNode()  #transition back to the StartNode