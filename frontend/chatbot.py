class ChatBot:
    def __init__(self):
        self.responses = {
            "hello": "Hi there! How can I assist you?",
            "how are you": "I'm just a bot, but I'm doing fine. How about you?",
            "bye": "Goodbye! Have a great day!",
        }
        self.default_response = "I'm sorry, I don't understand that."

    def get_response(self, user_input):
        user_input = user_input.lower()
        # TO EDIT here
        # should change to AI response here ----
        return self.responses.get(user_input, self.default_response)
