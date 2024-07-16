import time
from termcolor import colored

from MyGPT import auxiliar_functions as af
from MyGPT import MyGPTClass

class Bot:
    def __init__(self, bot_name='Tião') -> None:
        """
        Initializes an instance of the Bot class.

        Args:
            bot_name (str, optional): Name of the bot (default is 'Tião').
        """
        self.__bot_name = bot_name
        self.gpt = MyGPTClass.MyGPT(assistant_name=bot_name, printf=af.print_assistant)
        
        self.__available_tools = {
            'get_stock_price': {
                'func': af.get_stock_price,
                'registration_info': {
                    "type": "function",
                    "function": {
                        "name": "get_stock_price",
                        "description": "Retrieve current brazilian companies stock prices",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "stock_name": {
                                    "type": "string",
                                    "description": "Company name",
                                },
                                'period': {
                                    'type': 'string',
                                    'description': 'Historical period that will be returned with historical data \
                                                    as "1mo representing a month, "1d representing a day and \
                                                        "1y" representing a year',
                                    'enum': ["1d","5d","1mo","6mo","1y","5y","10y","ytd","max"]
                                }
                            },
                            "required": ["stock_name"],
                        },
                    },
                }
            },
            'get_math_assistance': {
                'func': self.call_math_assistent,
                'registration_info': {
                    "type": "function",
                    "function": {
                        "name": "get_math_assistance",
                        "description": "Get math assistance for a math problem",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "content": {
                                    "type": "string",
                                    "description": "Content informed by user to solve a math problem",
                                }
                            },
                            "required": ["content"],
                        },
                    },
                }
            },
            'get_image_description': {
                'func': self.get_image_description,
                'registration_info': {
                    "type": "function",
                    "function": {
                        "name": "get_image_description",
                        "description": "Get a description of an imagem from a url or path",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "content": {
                                    "type": "string",
                                    "description": "Content informed by user to be described from image",
                                },
                                "path": {
                                    "type": "string",
                                    "description": "Path or URL to get image content",
                                }
                            },
                            "required": ["content", "path"],
                        },
                    },
                }
            }
        }
        # Register all available tools with the GPT instance
        for available_tool_name in self.__available_tools:
            self.gpt.add_tool(available_tool_name, self.__available_tools[available_tool_name])
            
    def talk_to_me(self, content):
        """
        Initiates a conversation with the bot.

        Args:
            content (str): Content of the user's message.
        """
        af.print_assistant(f"{self.__bot_name}: Certo {self.__user}! Deixe-me pensar...")
        self.gpt.add_phrase(content=content)
        content = self.gpt.chat(asynchronous=False)
        af.print_assistant(f"{self.__bot_name}: {content}")
        # self.gpt.print_stream()
        
    def set_user(self, name):
        """
        Sets the name of the user interacting with the bot.

        Args:
            name (str): User's name.
        """
        self.__user = name
        
    def iterate_with_chat(self, message):
        """
        Handles iterative chat interactions with the user.

        Args:
            message (str): User's message.

        Returns:
            str: User input for further interaction.
        """
        if message.lower() == 'ajuda do assistente':
            self.assistant_demonstration(content='Se eu jogar um dado honesto 1000 vezes, qual é a probabilidade de eu obter exatamente 150 vezes o número 6? Resolva com um código',
                                         assistant_instructions=f"O nome do usuário é {self.__user} e ele é um usuário expert.")             
        else:
            self.talk_to_me(content=message)
        af.print_assistant(f"{self.__bot_name}: Te ajudo em algo mais {self.__user}?")
        return af.input_user("> ")
    
    def welcome_chat(self):
        """
        Welcomes the user and initializes the chat session.

        Returns:
            str: User's name.
        """
        af.print_assistant('Olá, seja bem vindo. A qualquer momento que desejar sair, digite "Finalizei"')
        af.print_assistant('')
        af.print_assistant('Para começar, me informe seu nome. ')
        name=af.input_user('> ')
        
        self.set_user(name=name)
        return name
    
    def chat(self):
        """
        Starts a chat session with the user.
        """
        af.print_assistant(f"{self.__bot_name}: Tudo bem, {self.__user}? Em que posso te ajudar?")
        message=af.input_user("> ")
        
        while message.lower() not in ['finalizei', 'não', 'fim', 'chega', 'nao']:
            message = self.iterate_with_chat(message=message)
        af.print_assistant(f"{self.__bot_name}: Ok, até uma próxima vez!")
    
    def run_chat(self):
        """
        Runs the chat session based on user input.
        """
        if self.welcome_chat() == 'Finalizei':
            af.print_assistant(f"{self.__bot_name}: Ok, quem sabe uma próxima vez...")
        else:
            self.chat()
            
    def get_assistant_help(self, content, assistant_instructions):
        """
        Calls the assistant for help with a specific content and instructions.

        Args:
            content (str): Content to be processed by the assistant.
            assistant_instructions (str): Instructions for the assistant.
        """
        self.gpt.call_assistant(message_content=content, assistant_instructions=assistant_instructions)
    
    def check_assistant_status(self):
        """
        Checks the status of the assistant's operation.
        """
        status = self.gpt.check_assistant_status()
        while status in ['queued', 'in_progress', 'cancelling']:
            af.print_assistant(f"{self.__bot_name}: {status}")
            time.sleep(1)
            status = self.gpt.check_assistant_status()
        
    def get_assistant_result(self, print_result=True):
        """
        Retrieves the result from the assistant.

        Args:
            print_result (bool, optional): Whether to print the result (default is True).

        Returns:
            str: Result from the assistant.
        """
        result = self.gpt.get_assistant_result()
        if print_result:
            af.print_assistant(f"{self.__bot_name}: {result}")
        return result
    
    def call_math_assistent(self, content, **args):
        """
        Calls the math assistant to help with a math problem.

        Args:
            content (str): Content of the math problem.
            **args: Additional arguments.
        
        Returns:
            str: Result from the math assistant.
        """
        af.print_warn(f"Redirecionando para o assistente")
        assistant_instructions=f"O nome do usuário é {self.__user} e ele é um usuário expert."
        self.get_assistant_help(content=content, assistant_instructions=assistant_instructions)
        self.check_assistant_status()
        return self.get_assistant_result(print_result=False)
    
    def get_image_description(self, content, path, **args):
        """
        Gets a description of an image from a URL or path.

        Args:
            content (str): Content related to the image.
            path (str): URL or path to the image.
            **args: Additional arguments.
        
        Returns:
            str: Description of the image.
        """
        af.print_warn(f"Redirecionando para o vision do GPT")
        if not path.startswith('http'):
            image_content = af.encode_image(image_path=path)
            image_file_extension = af.get_file_extension(file_path=path)
            path = f'data:image/{image_file_extension};base64,{image_content}'
        return self.gpt.get_image_description(content=content, path=path)
       
    def assistant_demonstration(self, content, assistant_instructions):
        """
        Demonstrates the use of the assistant with specific content and instructions.

        Args:
            content (str): Content to demonstrate.
            assistant_instructions (str): Instructions for the assistant.
        """
        af.print_assistant(f"{self.__bot_name}: Ok, vou demonstrar o uso do assistente...")
        self.get_assistant_help(content=content, assistant_instructions=assistant_instructions)
        self.check_assistant_status()
        self.get_assistant_result()
