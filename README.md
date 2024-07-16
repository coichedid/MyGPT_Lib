# MyGPT_Lib

MyGPT_Lib is a Python package developed by ChedidTech, implementing a generative AI robot designed to interact with users. It offers functionalities for image recognition, stock price querying via the Yahoo API, solving complex mathematical problems, and engaging in conversation.

## Main Features

- **Image Recognition:** Recognizes images from local files or remote URLs.
- **Stock Price Querying:** Retrieves current stock prices of Brazilian companies using the Yahoo API.
- **Mathematical Problem Solving:** Provides assistance with solving complex mathematical problems.
- **Conversation:** Engages in interactive conversations with users.

## Installation

You can install MyGPT_Lib using pip:

```bash
pip install MyGPT_Lib
```

## Usage

### Example Usage

```python
from MyGPT_Lib import MyGPTClass, BotClass

# Initialize a bot
bot = BotClass.Bot(bot_name='Tião')

# Start a chat session
bot.run_chat()
```

### Classes

#### [MyGPTClass](docs/MyGPTClass.md)

The `MyGPTClass` class provides methods to interact with OpenAI's GPT models and manage conversations. Key methods include:

- `__init__(self, assistant_name=None, model='gpt-3.5-turbo-0125', max_tokens=1000, temperature=0, printf=print)`: Constructor to initialize the GPT assistant.
- `add_tool(self, name, registration_info)`: Adds a new tool for GPT to use.
- `get_image_description(self, content, path, max_tokens=None, temperature=None, asynchronous=False)`: Retrieves a description of an image from a URL or local path.
- `chat(self, model=None, max_tokens=None, temperature=None, asynchronous=False)`: Initiates a conversation with GPT.

#### [BotClass](docs/BotClass.md)

The `BotClass` class implements a conversational bot using `MyGPTClass` for AI capabilities. Public methods include:

- `__init__(self, bot_name='Tião')`: Constructor to initialize the bot with a specified name.
- `talk_to_me(self, content)`: Initiates a conversation with the bot based on user input.
- `run_chat(self)`: Starts a chat session with the user, handling interactions until the user decides to end.
- `call_math_assistent(self, content, **args)`: Calls the math assistant to help with a math problem.
- `get_image_description(self, content, path, **args)`: Retrieves a description of an image from a URL or local path.

## License

[MIT License](LICENSE)
