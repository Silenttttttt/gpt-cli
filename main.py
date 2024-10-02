from openai import OpenAI
import json
import os
import argparse
import subprocess

CONFIG_FILE = "gpt_config.json"
CONVERSATIONS_FOLDER = "conversations"
SYSTEM_MESSAGE_FILE = "system_message.txt"

DEFAULT_SYSTEM_MESSAGE = """
You are an AI designed to assist users by continuing their sentences based on the context provided. 
Your goal is to continue the text without repeating any letters or words already present in the input. 
Ensure that your completions are coherent and contextually relevant. Pay special attention to whether the starting character should be a space or not, as it is very important and depends on the context. If the context requires a space, make sure it is present; if not, avoid starting with a space. Specifically, if you are continuing a word, do not start with a space. If the last character is the end of a word, then start with a space.
Do not start or end your response with quotes (' or " or `) unless it makes sense in the context.

The user is seeking autocompletion for the currently focused application.
"""

# Load or create the config file
def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as file:
            json.dump({"api_key": "", "model": "gpt-4o-mini", "editor": "nano", "current_conversation": ""}, file, indent=4)
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)

def load_system_message():
    if not os.path.exists(SYSTEM_MESSAGE_FILE):
        with open(SYSTEM_MESSAGE_FILE, 'w') as file:
            file.write(DEFAULT_SYSTEM_MESSAGE)
    with open(SYSTEM_MESSAGE_FILE, 'r') as file:
        return file.read()

def reset_system_message():
    with open(SYSTEM_MESSAGE_FILE, 'w') as file:
        file.write(DEFAULT_SYSTEM_MESSAGE)
    print("System message reset to default.")

config = load_config()
api_key = config.get("api_key", "")
model = config.get("model", "gpt-4o-mini")
editor = config.get("editor", "nano")
current_conversation = config.get("current_conversation", "")
system_message = load_system_message()

class Chatbot:
    def __init__(self, api_key, model):
        """Initialize with API key and model."""
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat_completion(self, messages):
        """Centralized chat completion logic with streaming."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True  # Enable streaming
            )

            # Collect the streamed responses
            full_response = ""
            for chunk in response:
                choices = chunk.choices
                if choices and len(choices) > 0:
                    delta = choices[0].delta
                    content = getattr(delta, 'content', None)
                    if content:
                        full_response += content
                        print(content, end='', flush=True)  # Stream to CLI
            print()
            return full_response

        except Exception as e:
            print(f"Error interacting with OpenAI API: {str(e)}")
            return None

class Conversation:
    def __init__(self, name):
        self.name = name
        self.file_path = os.path.join(CONVERSATIONS_FOLDER, f"{name}.json")
        self.messages = self.load_from_file() if os.path.exists(self.file_path) else []
        # Add system message only if the conversation is new
        if not self.messages:
            self.add_message("system", system_message)

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_conversation_format(self):
        return [{"role": message["role"], "content": message["content"]} for message in self.messages]

    def save_to_file(self):
        """Save the conversation to a JSON file."""
        if not os.path.exists(CONVERSATIONS_FOLDER):
            os.makedirs(CONVERSATIONS_FOLDER)
        with open(self.file_path, 'w') as file:
            json.dump(self.messages, file, indent=4)

    def load_from_file(self):
        """Load the conversation from a JSON file."""
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def get_status(self):
        """Get the status of the conversation."""
        num_messages = len(self.messages)
        num_tokens = sum(len(message["content"].split()) for message in self.messages)
        num_chars = sum(len(message["content"]) for message in self.messages)
        return {
            "num_messages": num_messages,
            "num_tokens": num_tokens,
            "num_chars": num_chars,
            "file_path": os.path.abspath(self.file_path)
        }

    def delete(self):
        """Delete the conversation file."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print(f"Conversation '{self.name}' deleted successfully.")
        else:
            print(f"Conversation '{self.name}' does not exist.")

def get_gpt_response(conversation_name, user_input):
    """
    Function to get GPT response for a given user input.
    """
    if not api_key:
        print("API key is not set. Use the -k argument to set it.")
        return

    conversation = Conversation(conversation_name)
    chatbot = Chatbot(api_key=api_key, model=model)
    conversation.add_message("user", user_input)
    messages = conversation.get_conversation_format()
    response = chatbot.chat_completion(messages)
    

    if response is None:
        return
    # Ensure that if the two starting characters are space, we make it only 1
    if response.startswith("  "):
        response = response[1:]
    
    conversation.add_message("assistant", response)
    conversation.save_to_file()
    
    return response

def list_conversations():
    """List all conversation names."""
    if not os.path.exists(CONVERSATIONS_FOLDER):
        print("No conversations found.")
        return
    conversations = [f.replace('.json', '') for f in os.listdir(CONVERSATIONS_FOLDER) if f.endswith('.json')]
    if conversations:
        print("Conversations:")
        for convo in conversations:
            print(f" - {convo}")


def show_guide():
    guide = """
    Welcome to the GPT CLI Tool!

    Here are the steps to get started:

    1. Set your OpenAI API key:
       python main.py -k YOUR_API_KEY
       python main.py --set-api-key YOUR_API_KEY

    2. Set the model (optional, default is gpt-4o-mini):
       python main.py -m gpt-4o
       python main.py --set-model gpt-4o-mini

    3. Set the text editor for editing the system message (default is nano) (optional):
       python main.py -E nano
       python main.py --set-editor vim

    4. Edit the system message, opens the above mentioned text editor (default is nano) (optional):
       python main.py -e
       python main.py --edit-system-message

    5. Load a conversation, specify the conversation name to use:
       python main.py -c CONVERSATION_NAME
       python main.py --conversation CONVERSATION_NAME

    6. Get a response for the loaded conversation:
       python main.py -r Your input message
       python main.py --response Your input message

    7. Check the status of the currently loaded conversation:
       python main.py -s
       python main.py --status

    8. Reset the system message to default:
       python main.py -R
       python main.py --reset-system-message

    9. Delete a conversation:
       python main.py -d CONVERSATION_NAME
       python main.py --delete-conversation CONVERSATION_NAME

    10. List all conversations:
        python main.py -l
        python main.py --list-conversations

    11. Show this guide:
        python main.py -h
        python main.py --help

    Enjoy using the tool!
    """
    print(guide)

def main():
    parser = argparse.ArgumentParser(description="GPT Autocomplete CLI Tool")
    parser = argparse.ArgumentParser(description="GPT Autocomplete CLI Tool")
    parser.add_argument("-k", "--set-api-key", type=str, help="Set the OpenAI API key")
    parser.add_argument("-m", "--set-model", type=str, help="Set the model to be used")
    parser.add_argument("-E", "--set-editor", type=str, help="Set the text editor to be used for editing the system message")
    parser.add_argument("-e", "--edit-system-message", action="store_true", help="Edit the system message using the configured editor")
    parser.add_argument("-R", "--reset-system-message", action="store_true", help="Reset the system message to default")
    parser.add_argument("-s", "--status", action="store_true", help="Show the status of the current conversation")
    parser.add_argument("-r", "--response", nargs='+', help="Get response for the given conversation")
    parser.add_argument("-c", "--conversation", type=str, help="Specify the conversation name")
    parser.add_argument("-d", "--delete-conversation", type=str, help="Delete the specified conversation")
    parser.add_argument("-l", "--list-conversations", action="store_true", help="List all conversations")
    parser.add_argument("-H", "--custom-help", action="store_true", help="Show the custom guide")



    args = parser.parse_args()

    if args.set_api_key:
        config["api_key"] = args.set_api_key
        save_config(config)
        print("API key set successfully.")
        return

    if args.set_model:
        config["model"] = args.set_model
        save_config(config)
        print(f"Model set to {args.set_model} successfully.")
        return

    if args.set_editor:
        config["editor"] = args.set_editor
        save_config(config)
        print(f"Editor set to {args.set_editor} successfully.")
        return

    if args.edit_system_message:
        subprocess.call([editor, SYSTEM_MESSAGE_FILE])
        print("System message updated successfully.")
        return

    if args.reset_system_message:
        reset_system_message()
        return

    if args.status:
        if not current_conversation:
            print("No conversation is currently loaded. Please load a conversation using -c.")
            return
        conversation = Conversation(current_conversation)
        status = conversation.get_status()
        print(f"Conversation '{current_conversation}' Status:")
        print(f"Number of messages: {status['num_messages']}")
        print(f"Number of tokens: {status['num_tokens']}")
        print(f"Number of characters: {status['num_chars']}")
        print(f"File path: {status['file_path']}")
        return

    if args.conversation:
        config["current_conversation"] = args.conversation
        save_config(config)
        print(f"Conversation '{args.conversation}' loaded.")
        return

    if args.delete_conversation:
        conversation = Conversation(args.delete_conversation)
        conversation.delete()
        if current_conversation == args.delete_conversation:
            config["current_conversation"] = ""
            save_config(config)
        return

    if args.response:
        if not api_key:
            print("API key is not set. Use the -k argument to set it.")
            return
        if not current_conversation:
            print("No conversation is currently loaded. Please load a conversation using -c.")
            return
        user_input = ' '.join(args.response)
        get_gpt_response(current_conversation, user_input)
        return

    if args.list_conversations:
        list_conversations()
        return

    if args.custom_help:
        show_guide()
        return

    show_guide()

if __name__ == "__main__":
    main()