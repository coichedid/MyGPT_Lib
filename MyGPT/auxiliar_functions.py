import base64
import yfinance as yf
import os
from termcolor import colored

def print_assistant(text, end='\n'):
    print(colored(text, 'blue'), end=end)

def print_warn(text, end='\n'):
    print(colored(text, 'red'), end=end)

def input_user(text):
    return input(colored(text, 'green'))

def encode_image(image_path):
    print(colored(os.getcwd(), 'red'))
    with open(image_path, 'rb' ) as img:
        return base64.b64encode(img.read()).decode('utf-8')
    
def get_file_extension(file_path):
    filename, file_extension = os.path.splitext(file_path)
    return file_extension[1:].lower()
    
def get_stock_price(stock_name, period='1mo', **args):
    print_warn(f"Redirecionando para a api de stock exchange do Yahoo")
    ticker_obj = yf.Ticker(f'{stock_name}')
    hist = ticker_obj.history(period=period)['Close']
    hist.index = hist.index.strftime('%Y-%m-%d')
    hist = round(hist, 2)
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    return hist.to_json()