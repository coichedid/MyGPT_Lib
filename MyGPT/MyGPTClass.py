import openai
import json
from dotenv import load_dotenv, find_dotenv

from MyGPT import gpt_constants as c

_ = load_dotenv(find_dotenv())

class MyGPT:

    # instance attributes
    def __init__(self, assistant_name=None, model='gpt-3.5-turbo-0125', max_tokens=1000, temperature=0, printf=print):
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
        assistant_list = self.__client.beta.assistants.list()
        self.__recovered_assistants = {a.name: a.id for a in assistant_list}
        
        
    def __add_code_interpreter_assistant(self, name, instructions):
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
        thread = self.__client.beta.threads.create()
        self.__assistant_thread = thread.id
    
    def call_assistant(self, message_content, assistant_instructions=''):
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
        run = self.__client.beta.threads.runs.retrieve(
            thread_id=self.__assistant_thread,
            run_id=self.__assistant_thread_run
        )
        return run.status
    
    def get_assistant_result(self):
        message = self.__client.beta.threads.messages.list(
            thread_id=self.__assistant_thread
        )
        return message.data[0].content[0].text.value
        
    # add new callable function
    def add_tool(self, name, registration_info):
        self.__available_tools.append(registration_info['registration_info'])
        self.__available_tools_pointers[name] = registration_info['func']

    # set instance attributes
    def set_attribute(self, att, value):
        if att not in ['max_tokens', 'temperature', 'model']:
            Exception('Invalid attribute')
        self[att] = value
    
    # add a phrase
    def add_phrase(self, content=None, role='user', phrase=None):
        if not content and not phrase:
            Exception('Need a content or full phrase')
        new_conversation = phrase or {
            'role': role,
            'content': content
        }
        self.__conversation.append(new_conversation)
        
    # get a description of an image
    def get_image_description(self, content, path, max_tokens=None, temperature=None, asynchronous=False):
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
        
    # talk to gpt    
    def talk_to_gpt(self, model=None, max_tokens=None, temperature=None, asynchronous=False):
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
        
    # run a chat
    def chat(self, model=None, max_tokens=None, temperature=None, asynchronous=False):
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
    
    # get all conversation
    def get_conversation(self):
        return self.__conversation
    
    # get all responses
    def get_responses(self):
        return self.__responses   
    
    # get internal usage
    def get_usage(self):
        return self.__usages 
    
    # reset all history
    def reset_chat(self):
        self.__conversation = []
        self.__responses = []

    # iterate over stream
    def print_stream(self):
        full_text = ''
        # if self.__assistant_name:
        #     self.__printf(f"{self.__assistant_name}: ", end='')
        print('')
        for chunk in self.__stream_content:
            text = chunk.choices[0].delta.content or ""
            full_text += text
            self.__printf(text, end='')
        self.add_phrase(role='assistant', content=full_text)
        
        self.__printf('')
        
    
