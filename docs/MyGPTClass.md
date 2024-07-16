# MyGPTClass Documentation

`MyGPTClass` is a Python class designed to interact with the OpenAI API, providing a wide range of functionalities including image recognition, mathematical problem-solving, stock value queries, and general conversation capabilities. Below is the detailed documentation of the class and its methods.

## Class: `MyGPT`

### Constructor: `__init__`
Initializes a new instance of the `MyGPT` class.

#### Parameters:
- `assistant_name` (str, optional): The name of the assistant.
- `model` (str, optional): The model to be used, default is `'gpt-3.5-turbo-0125'`.
- `max_tokens` (int, optional): The maximum number of tokens, default is `1000`.
- `temperature` (int, optional): The temperature for the model, default is `0`.
- `printf` (callable, optional): The print function, default is `print`.

### Methods:

#### `call_assistant`
Sends a message to the assistant and initiates a new run.

##### Parameters:
- `message_content` (str): The content of the message to be sent to the assistant.
- `assistant_instructions` (str, optional): Instructions for the assistant.

#### `check_assistant_status`
Checks the status of the current assistant run.

##### Returns:
- `status` (str): The status of the assistant run.

#### `get_assistant_result`
Retrieves the result of the assistant's response.

##### Returns:
- `result` (str): The content of the assistant's response.

#### `add_tool`
Registers a new callable function (tool) to the assistant.

##### Parameters:
- `name` (str): The name of the tool.
- `registration_info` (dict): The registration information of the tool.

#### `set_attribute`
Sets the value of a specified attribute.

##### Parameters:
- `att` (str): The name of the attribute to set.
- `value` (any): The value to set for the attribute.

##### Raises:
- `Exception`: If an invalid attribute is provided.

#### `add_phrase`
Adds a new phrase to the conversation history.

##### Parameters:
- `content` (str, optional): The content of the phrase.
- `role` (str, optional): The role of the phrase, default is `'user'`.
- `phrase` (dict, optional): The full phrase dictionary.

##### Raises:
- `Exception`: If neither `content` nor `phrase` is provided.

#### `get_image_description`
Gets a description of an image.

##### Parameters:
- `content` (str): The content related to the image.
- `path` (str): The path or URL of the image.
- `max_tokens` (int, optional): The maximum number of tokens for the response.
- `temperature` (int, optional): The temperature for the response.
- `asynchronous` (bool, optional): If the response should be asynchronous.

##### Returns:
- `description` (str): The description of the image.

#### `talk_to_gpt`
Sends a conversation to GPT and handles the response, including tool calls if any.

##### Parameters:
- `model` (str, optional): The model to be used.
- `max_tokens` (int, optional): The maximum number of tokens for the response.
- `temperature` (int, optional): The temperature for the response.
- `asynchronous` (bool, optional): If the response should be asynchronous.

##### Returns:
- `response` (dict): The response from GPT.

#### `chat`
Runs a chat conversation with GPT.

##### Parameters:
- `model` (str, optional): The model to be used.
- `max_tokens` (int, optional): The maximum number of tokens for the response.
- `temperature` (int, optional): The temperature for the response.
- `asynchronous` (bool, optional): If the response should be asynchronous.

##### Returns:
- `response` (str): The content of the assistant's response.

#### `get_conversation`
Retrieves the entire conversation history.

##### Returns:
- `conversation` (list): The list of conversation phrases.

#### `get_responses`
Retrieves all responses from the conversation.

##### Returns:
- `responses` (list): The list of responses.

#### `get_usage`
Retrieves the usage statistics of the conversation.

##### Returns:
- `usages` (list): The list of usage statistics.

#### `reset_chat`
Resets the conversation history and responses.

#### `print_stream`
Prints the response stream content.

##### Raises:
- `Exception`: If an error occurs during the streaming process.

## Example Usage:

```python
from MyGPTClass import MyGPT

# Initialize the MyGPT instance
my_gpt = MyGPT(assistant_name='MyAssistant', model='gpt-4')

# Add a phrase to the conversation
my_gpt.add_phrase(content="Hello, how can you assist me today?")

# Chat with GPT
response = my_gpt.chat()
print(response)

# Get a description of an image
image_description = my_gpt.get_image_description(content="Describe this image", path="path/to/image.jpg")
print(image_description)

# Reset the chat history
my_gpt.reset_chat()
```