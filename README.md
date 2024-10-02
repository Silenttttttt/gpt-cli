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
- **List Conversations**: List all saved conversations.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Silenttttttt/gpt_cli.git
   cd gpt_cli
   ```

2. Install the required dependency:
   ```bash
   pip install openai
   ```

## Quick Start Tutorial

1. **Set Your OpenAI API Key**:
   ```bash
   python main.py -k YOUR_API_KEY
   ```

2. **Load a Conversation** (you can choose any name; if the conversation doesn't exist, a new one gets created):
   ```bash
   python main.py -c CONVERSATION_NAME
   ```

3. **Get a Response for the Loaded Conversation**:
   ```bash
   python main.py -r "Your input message"
   ```

## Usage

1. **Set Your OpenAI API Key**:
   ```bash
   python main.py -k YOUR_API_KEY
   python main.py --set-api-key YOUR_API_KEY
   ```

2. **Set the Model (Optional, default is gpt-4o-mini)**:
   ```bash
   python main.py -m gpt-4o
   python main.py --set-model gpt-4o-mini
   ```

3. **Set the Text Editor for Editing the System Message (Default is nano) (Optional)**:
   ```bash
   python main.py -E nano
   python main.py --set-editor vim
   ```

4. **Edit the System Message**:
   ```bash
   python main.py -e
   python main.py --edit-system-message
   ```

5. **Load a Conversation (you can choose any name; if the conversation doesn't exist, a new one gets created)**:
   ```bash
   python main.py -c CONVERSATION_NAME
   python main.py --conversation CONVERSATION_NAME
   ```

6. **Get a Response for the Loaded Conversation**:
   ```bash
   python main.py -r "Your input message"
   python main.py --response "Your input message"
   ```

7. **Check the Status of the Currently Loaded Conversation**:
   ```bash
   python main.py -s
   python main.py --status
   ```

8. **Reset the System Message to Default**:
   ```bash
   python main.py -R
   python main.py --reset-system-message
   ```

9. **Delete a Conversation**:
   ```bash
   python main.py -d CONVERSATION_NAME
   python main.py --delete-conversation CONVERSATION_NAME
   ```

10. **List All Conversations**:
    ```bash
    python main.py -l
    python main.py --list-conversations
    ```

11. **Show the Custom Help Text**:
    ```bash
    python main.py -H
    python main.py --custom-help
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
