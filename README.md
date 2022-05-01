# BlackBox Chatbot

BlackBox chatbot comes with a [website for a fictional company](https://github.com/bresha/blackbox).

## Installation

Clone this repository and clone [wbsite repository](https://github.com/bresha/blackbox) in a new folder. Create virtual environments, one for each project, and install requirements.txt for each project in its virtual environment. for chatbot you must use python 3.8.13  
in root folder of website project you must create .env file and add following:  
```
GMAIL_USER = '<YOUR GMAIL USER NAME>'
GMAIL_PASSWORD = '<YOUR GMAIL PASSWORD>'

SEND_MAIL_TO = '<EMAIL ADDRESS TO SEND EMAIL FORM APP>'
```

Also add .flaskenv file and add:
```
FLASK_APP=web
FLASK_ENV=development
```

## Usage

First start chatbot in its environment, in one terminal type:  
```rasa run actions```  
and in another terminal type:  
```rasa run --enable-api --cors "*"```  
then go to website folder and in its environment, in a terminal type:  
```flask run```  
Then open browser and go to 127.0.0.1:5000 and try chatbot in the bottom right corner.

## License
[MIT](https://choosealicense.com/licenses/mit/)