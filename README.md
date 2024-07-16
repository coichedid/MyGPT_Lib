# MyGPT_Lib

MyGPT_Lib is a Python package developed by ChedidTech, implementing a generative AI robot focused on interacting with users. It offers various functionalities such as image recognition, stock price querying via the Yahoo API, solving complex mathematical problems, and engaging in conversation.

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

To use MyGPT_Lib, start by initializing a bot instance with a user-defined name. Interactions with the bot can cover a variety of tasks, such as image recognition, stock price queries, solving math problems, and general conversation.

### Example Interactions

1. **Tool and Assistant Capabilities:**
   ```python
   bot = BotClass.Bot(bot_name='Tião')
   bot.set_user('User')
   bot.talk_to_me('quais as capacidades de tools locais e assistentes foram registradas?')
   ```
   **Result**
   ```
   Tião: The following capabilities of local tools and assistants have been registered:

   1. **Tool: get_stock_price**
      - Description: Retrieve current Brazilian companies stock prices.
      
   2. **Tool: get_math_assistance**
      - Description: Get math assistance for a math problem.
      
   3. **Tool: get_image_description**
      - Description: Get a description of an image from a URL or path.
      
   4. **Tool: get_capabilities**
      - Description: Get a list of current custom capabilities of this bot.
      
   5. **Assistant: Math Tutor from ChedidTech**
   - Description: You are a personal math tutor from the company ChedidTech. Write and execute codes to answer math questions provided to you. If the user is an expert, respond by describing the steps used for the answer in addition to the final result. Otherwise, provide only the final result.
   ```

2. **Dice Possibilities:**
   ```python
   bot.talk_to_me('quantas possibilidades existem em dois dados lançados? Resolva com um código')
   ```
   **Result**
   ```
   Tião: There are 36 possibilities when rolling two dice. This is because each die has 6 sides, and when two dice are rolled, the total number of outcomes is the product of the number of sides on each die (6 x 6 = 36).
   ```

3. **Top 5 Stocks:**
   ```python
   bot.talk_to_me('quais as 5 ações de maior valor na bolsa brasileira hoje?')
   ```
   **Result**
   ```
   Tião: As 5 ações de maior valor na bolsa brasileira hoje são:

   1. **PETR4.SA** (Petrobras) - R$ 38.50
   2. **VALE3.SA** (Vale) - R$ 62.99
   3. **ITUB4.SA** (Itaú Unibanco) - R$ 33.59
   4. **BBDC4.SA** (Bradesco) - R$ 12.61
   5. **ABEV3.SA** (Ambev) - R$ 11.64

   Esses são os valores das ações das empresas listadas na bolsa brasileira hoje.
   ```

4. **Triangle Counting:**
   ```python
   bot.talk_to_me('quantos triângulos existem na figura images/triangulos.png?')
   ```
   **Result**
   ```
   Tião: A imagem contém um grande triângulo equilátero com um triângulo equilátero menor invertido dentro dele. O triângulo menor está posicionado de forma que sua base seja paralela à base do triângulo maior e seu ápice aponta para baixo, dividindo o triângulo maior em quatro triângulos menores.

   Os triângulos na imagem são:
   1. O grande triângulo externo.
   2. O triângulo menor invertido no centro.
   3. O triângulo superior esquerdo.
   4. O triângulo superior direito.
   5. O triângulo inferior (excluindo o triângulo invertido).

   Portanto, existem um total de 5 triângulos na imagem.
   ```

5. **Character Recognition:**
   ```python
   bot.talk_to_me('quem são os personagens da figura https://m.media-amazon.com/images/I/81PPn5LIrKL._AC_SX679_.jpg?')
   ```
   **Result**
   ```
   Tião: Os personagens na imagem são Beavis and Butt-Head da série de televisão animada "Beavis and Butt-Head". A imagem é do álbum de música "The Beavis and Butt-Head Experience", que apresenta esses personagens.
   ```

6. **TV Channel Inquiry:**
   ```python
   bot.talk_to_me('qual a emissora de televisão na logomarca da camisa de um dos personagens?')
   ```
   **Result**
   ```
   Tião: A logomarca na camisa de um dos personagens é da emissora de televisão "MTV". Beavis, o personagem à esquerda na imagem, está usando uma camiseta preta com o logo da MTV. A MTV é uma conhecida rede de televisão dedicada à música, entretenimento e cultura jovem.
   ```

7. **Probability Calculation:**
   ```python
   bot.talk_to_me('Se eu jogar um dado honesto 1000 vezes, qual é a probabilidade de eu obter exatamente 150 vezes o número 6? Resolva com um código')
   ```
   **Result**
   ```
   Tião: A probabilidade de obter exatamente 150 vezes o número 6 ao lançar um dado honesto 1000 vezes é aproximadamente 0.0126 ou 1.26%.
   ```

8. **Word Meanings:**
   ```python
   bot.talk_to_me('Quais os 3 significados principais da palavra maçã?')
   ```
   **Result**
   ```
   Tião: A palavra "maçã" possui os seguintes significados principais:

   1. **Fruta:** A maçã é uma fruta comum, geralmente redonda, de polpa branca ou avermelhada, cultivada em macieiras. É conhecida por seu sabor doce e crocante, sendo uma fonte de vitaminas e fibras.

   2. **Culinária:** A maçã é amplamente utilizada na culinária em diversas preparações, como sucos, saladas de frutas, compotas, sobremesas, bolos, tortas e outros pratos.

   3. **Símbolo:** Em alguns contextos, a maçã pode ser um símbolo de tentação, conhecido pela história de Adão e Eva no Jardim do Éden, onde a maçã é frequentemente representada como o fruto proibido.

   Esses são os três significados principais associados à palavra "maçã".
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