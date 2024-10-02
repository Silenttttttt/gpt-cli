# GPT CLI

GPT CLI is a command-line interface tool designed to interact with OpenAI's GPT models. It allows users to manage conversations, edit system messages, and customize settings, providing a seamless experience for text autocompletion and AI-assisted tasks.

**Note**: This tool is made for Linux. Windows support is unknown.

## Features

- **Set API Key**: Easily configure your OpenAI API key for authentication.
- **Model Selection**: Choose from available GPT models to suit your needs.
- **System Message Editing**: Customize the system message using your preferred text editor.
- **Conversation Management**: Load, save, and delete conversations with ease.
- **Get AI Responses**: Generate responses for loaded conversations.
- **Conversation Status**: Check the status of your current conversation, including message count and file path.

## Installation

1. Clone the repository:
   git clone https://github.com/Silenttttttt/gpt_cli.git
   cd gpt_cli

2. Install the required dependency:
  `pip install openai`

## Usage

### Set Your OpenAI API Key
   python main.py -k YOUR_API_KEY

### Set the Model (Optional)
   python main.py -m YOUR_MODEL

### Set the Text Editor (Optional)
   python main.py -E YOUR_EDITOR

### Edit the System Message
   python main.py -e

### Load a Conversation
   python main.py -c CONVERSATION_NAME

### Get a Response for the Loaded Conversation
   python main.py -r "Your input message"

### Check the Status of the Current Conversation
   python main.py -s

### Reset the System Message to Default
   python main.py -R

### Delete a Conversation
   python main.py -d CONVERSATION_NAME

### Show the help text
   python main.py -h

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
