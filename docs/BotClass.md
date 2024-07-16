# Bot Class

The `Bot` class represents a chatbot interface that interacts with users using OpenAI's GPT models and auxiliary functions.

## Constructor

### `__init__(self, bot_name='Tião') -> None`

Initializes an instance of the `Bot` class.

- **Parameters:**
  - `bot_name` (str, optional): Name of the bot (default: 'Tião').

## Public Methods

### `talk_to_me(self, content)`

Initiates a conversation with the bot.

- **Parameters:**
  - `content` (str): Content of the user's message.

### `set_user(self, name)`

Sets the name of the user interacting with the bot.

- **Parameters:**
  - `name` (str): User's name.

### `iterate_with_chat(self, message)`

Handles iterative chat interactions with the user.

- **Parameters:**
  - `message` (str): User's message.

### `welcome_chat(self)`

Welcomes the user and initializes the chat session.

- **Returns:**
  - `str`: User's name.

### `chat(self)`

Starts a chat session with the user.

### `run_chat(self)`

Runs the chat session based on user input.

### `get_assistant_help(self, content, assistant_instructions)`

Calls the assistant for help with a specific content and instructions.

- **Parameters:**
  - `content` (str): Content to be processed by the assistant.
  - `assistant_instructions` (str): Instructions for the assistant.

### `check_assistant_status(self)`

Checks the status of the assistant's operation.

### `get_assistant_result(self, print_result=True)`

Retrieves the result from the assistant.

- **Parameters:**
  - `print_result` (bool, optional): Whether to print the result (default: True).

### `call_math_assistent(self, content, **args)`

Calls the math assistant to help with a math problem.

- **Parameters:**
  - `content` (str): Content of the math problem.
  - `args` (dict): Additional arguments.

### `get_image_description(self, content, path, **args)`

Gets a description of an image from a URL or path.

- **Parameters:**
  - `content` (str): Content related to the image.
  - `path` (str): URL or path to the image.
  - `args` (dict): Additional arguments.

### `assistant_demonstration(self, content, assistant_instructions)`

Demonstrates the use of the assistant with specific content and instructions.

- **Parameters:**
  - `content` (str): Content to demonstrate.
  - `assistant_instructions` (str): Instructions for the assistant.
