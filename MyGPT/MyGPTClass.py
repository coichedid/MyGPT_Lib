import openai
import json
from dotenv import load_dotenv, find_dotenv

from MyGPT import gpt_constants as c

_ = load_dotenv(find_dotenv())

class MyGPT:
    """
    A class to interact with OpenAI's GPT models through threaded communication.

    Attributes:
        model (str): Model ID to use for GPT.
        max_tokens (int): Maximum number of tokens per request.
        temperature (float): Sampling temperature for text generation.
        __conversation (list): List to store conversation history.
        __responses (list): List to store GPT responses.
        __usages (list): List to store internal usage statistics.
        __stream_content: Content from streamed asynchronous sessions.
        __client: OpenAI Client instance.
        __assistant_name (str): Name of the assistant.
        __printf: Print function to use.
        __available_tools (list): List of registered tools.
        __available_tools_pointers (dict): Mapping of tool names to their functions.
        __code_interpreter_assistent: ID of the code interpreter assistant.
        __assistant_thread: ID of the current thread with the assistant.
        __assistant_thread_run: ID of the current assistant run.
    """

    def __init__(self, assistant_name=None, model='gpt-3.5-turbo-0125', max_tokens=1000, temperature=0, printf=print):
        """
        Initializes an instance of the MyGPT class.

        Args:
            assistant_name (str, optional): Name of the assistant.
            model (str, optional): Model ID to use for GPT (default: 'gpt-3.5-turbo-0125').
            max_tokens (int, optional): Maximum number of tokens per request (default: 1000).
            temperature (float, optional): Sampling temperature for text generation (default: 0).
            printf (function, optional): Function to use for printing (default: print).
        """
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.__conversation = []
        self.__responses = []
        self.__usages = []
        self.__stream_content = None
        self.__client = openai.Client()
        self.__assistant_name = assistant_name
        self.__printf=printf
        self.__available_tools = []
        self.__available_tools_pointers = {}
        self.__recover_assistants()
        self.__add_code_interpreter_assistant(name=c.CODE_ASSISTANT_NAME, instructions=c.CODE_ASSISTANT_INSTRUCTIONS)
        self.__add_thread()

    def __recover_assistants(self):
        """
        Retrieves and stores the list of available assistants from OpenAI.
        """
        assistant_list = self.__client.beta.assistants.list()
        self.__recovered_assistants = {a.name: a.id for a in assistant_list}

    def __add_code_interpreter_assistant(self, name, instructions):
        """
        Adds a code interpreter assistant if not already recovered.

        Args:
            name (str): Name of the assistant.
            instructions (str): Instructions for the assistant.
        """
        if name in self.__recovered_assistants.keys():
            self.__code_interpreter_assistent = self.__recovered_assistants[name]
        else:
            assistant = self.__client.beta.assistants.create(
                name=name,
                instructions=instructions,
                tools=[{'type': 'code_interpreter'}],
                model='gpt-3.5-turbo-0125'
            )
            self.__code_interpreter_assistent = assistant.id

    def __add_thread(self):
        """
        Creates a new thread for communication with the assistant.
        """
        thread = self.__client.beta.threads.create()
        self.__assistant_thread = thread.id

    def call_assistant(self, message_content, assistant_instructions=''):
        """
        Calls the assistant with a user message and optional instructions.

        Args:
            message_content (str): Content of the user's message.
            assistant_instructions (str, optional): Instructions for the assistant.
        """
        message = self.__client.beta.threads.messages.create(
            thread_id=self.__assistant_thread,
            role='user',
            content=message_content
        )
        run = self.__client.beta.threads.runs.create(
            thread_id=self.__assistant_thread,
            assistant_id=self.__code_interpreter_assistent,
            instructions=assistant_instructions
        )
        self.__assistant_thread_run = run.id

    def check_assistant_status(self):
        """
        Checks the status of the current assistant run.

        Returns:
            str: Status of the assistant run.
        """
        run = self.__client.beta.threads.runs.retrieve(
            thread_id=self.__assistant_thread,
            run_id=self.__assistant_thread_run
        )
        return run.status

    def get_assistant_result(self):
        """
        Retrieves the result from the assistant after a call.

        Returns:
            str: Content of the assistant's response.
        """
        message = self.__client.beta.threads.messages.list(
            thread_id=self.__assistant_thread
        )
        return message.data[0].content[0].text.value

    def add_tool(self, name, registration_info):
        """
        Adds a new callable tool to the assistant.

        Args:
            name (str): Name of the tool.
            registration_info (dict): Registration information for the tool.
        """
        self.__available_tools.append(registration_info['registration_info'])
        self.__available_tools_pointers[name] = registration_info['func']

    def set_attribute(self, att, value):
        """
        Sets instance attributes for `max_tokens`, `temperature`, or `model`.

        Args:
            att (str): Attribute name ('max_tokens', 'temperature', 'model').
            value: Value to set.
        """
        if att not in ['max_tokens', 'temperature', 'model']:
            Exception('Invalid attribute')
        self[att] = value

    def add_phrase(self, content=None, role='user', phrase=None):
        """
        Adds a phrase or content to the conversation.

        Args:
            content (str, optional): Content to add.
            role (str, optional): Role of the speaker ('user' or 'assistant').
            phrase (dict, optional): Complete phrase object.
        """
        if not content and not phrase:
            Exception('Need a content or full phrase')
        new_conversation = phrase or {
            'role': role,
            'content': content
        }
        self.__conversation.append(new_conversation)

    def get_image_description(self, content, path, max_tokens=None, temperature=None, asynchronous=False):
        """
        Generates a description of an image using GPT.

        Args:
            content (str): Text prompt for the image description.
            path (str): URL of the image.
            max_tokens (int, optional): Maximum tokens for completion.
            temperature (float, optional): Sampling temperature.
            asynchronous (bool, optional): Whether to stream the response.

        Returns:
            str: Description of the image.
        """
        if not path.startswith('data:image') and not path.startswith('http'):
            return ''
        params = {
            'messages': [{
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': content},
                        {'type': 'image_url', 'image_url':
                        {'url': path}}
                    ]
                }],
            'model': 'gpt-4o',
            'max_tokens': max_tokens or self.max_tokens,
            'temperature': temperature or self.temperature,
            'stream': asynchronous
        }
        response = self.__client.chat.completions.create(**params)
        return response.choices[0].message.content

    def talk_to_gpt(self, model=None, max_tokens=None, temperature=None, asynchronous=False):
        """
        Initiates a conversation with the GPT model.

        Args:
            model (str, optional): Model ID to use.
            max_tokens (int, optional): Maximum tokens for completion.
            temperature (float, optional): Sampling temperature.
            asynchronous (bool, optional): Whether to stream the response.

        Returns:
            str: Content of the GPT response.
        """
        params = {
            'messages': self.__conversation,
            'model': model or self.model,
            'max_tokens': max_tokens or self.max_tokens,
            'temperature': temperature or self.temperature,
            'stream': asynchronous
        }
        if len(self.__available_tools) > 0:
            params['tools'] = self.__available_tools
            params['tool_choice'] = "auto"
        response = self.__client.chat.completions.create(**params)
        self.add_phrase(phrase=response.choices[0].message.model_dump(exclude_none=True))
        tool_calls = None
        try:
            tool_calls = response.choices[0].message.tool_calls
        except:
            pass

        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.__available_tools_pointers[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                phrase = {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
                self.add_phrase(phrase=phrase)
            response = self.talk_to_gpt(model=model, max_tokens=max_tokens, temperature=temperature, asynchronous=asynchronous)
        return response

    def chat(self, model=None, max_tokens=None, temperature=None, asynchronous=False):
        """
        Runs a chat session using GPT.

        Args:
            model (str, optional): Model ID to use.
            max_tokens (int, optional): Maximum tokens for completion.
            temperature (float, optional): Sampling temperature.
            asynchronous (bool, optional): Whether to stream the response.

        Returns:
            str: Content of the GPT response.
        """
        response = self.talk_to_gpt(model=model, max_tokens=max_tokens, temperature=temperature, asynchronous=asynchronous)
        if not asynchronous:
            response_content = response.choices[0].message.content
            usage = {
                'completion_tokens': response.usage.completion_tokens,
                'prompt_tokens': response.usage.prompt_tokens,
                'total_tokens': response.usage.total_tokens
            }
            self.__usages.append(usage)
            self.__responses.append(response_content)
            # self.__printf(f"{self.__assistant_name or self.__conversation[-1]['role']}: {self.__conversation[-1]['content']}")
        else:
            self.__stream_content = response
            self.print_stream()
        return response.choices[0].message.content

    def get_conversation(self):
        """
        Returns the entire conversation history.

        Returns:
            list: List of conversation objects.
        """
        return self.__conversation

    def get_responses(self):
        """
        Returns all responses received from GPT.

        Returns:
            list: List of GPT responses.
        """
        return self.__responses

    def get_usage(self):
        """
        Returns internal usage statistics.

        Returns:
            list: List of usage statistics.
        """
        return self.__usages

    def reset_chat(self):
        """
        Resets the conversation history.
        """
        self.__conversation = []
        self.__responses = []

    def print_stream(self):
        """
        Prints the streamed content from an asynchronous chat session.
        """
        full_text = ''
        print('')
        for chunk in self.__stream_content:
            text = chunk.choices[0].delta.content or ""
            full_text += text
            self.__printf(text, end='')
        self.add_phrase(role='assistant', content=full_text)
        self.__printf('')
