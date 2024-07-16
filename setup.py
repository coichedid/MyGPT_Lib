from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'ChatGPT Class'
LONG_DESCRIPTION = 'ChatGPT Conversation Class'
print(find_packages())
# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="mygpt", 
        version=VERSION,
        author="Clovis Chedid",
        author_email="clovis.s.chedid@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'openai==1.25.2',
            'python-dotenv==1.0.1',
            'yfinance==0.2.37',
            'pandas==2.2.1',
            'matplotlib==3.8.3',
            'pillow==10.2.0',
            'PyAudio==0.2.14',
            'SpeechRecognition==3.10.1',
            'sounddevice==0.4.6',
            'playsound==1.2.2'
            ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'chatgpt'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)