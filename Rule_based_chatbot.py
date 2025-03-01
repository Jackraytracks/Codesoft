import re

def chatbot_response(user_input):
    user_input = user_input.strip().lower()
    
    responses = {
        r"^hello$": "Hello! How can I help you today?",
        r"^.*your name.*$": "I'm a simple chatbot created to assist you.",
        r"^how are you\?$": "I'm just a bot, but I'm here to help!",
        r"^bye$": "Goodbye! Have a great day!"
    }
    
    for pattern, response in responses.items():
        if re.search(pattern, user_input):  # Changed from re.match() to re.search() for partial matches
            return response
    
    return "I'm not sure how to respond to that. Can you ask something else?"

# Running the chatbot in a simple loop
print("Chatbot: Hello! Type 'bye', 'Bye', or 'BYE' to exit.")
while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["bye", "Bye", "BYE"]:
        print("Chatbot: Goodbye!")
        break
    print("Chatbot:", chatbot_response(user_input))
