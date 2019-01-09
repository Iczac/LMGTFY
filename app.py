from flask import Flask
from flask import request
import re
import requests
import json

app = Flask(__name__)

def setLMGTFY(string, index):
    substring = string[index:]

    match = re.search('[!,.?]', substring)

    if match is not None:
        new_string = substring[:substring.find(match.group())]
    else:
        new_string = substring

    LMGTFY = 'http://lmgtfy.com/?q=' + ('+').join(new_string.split(' '))

    return LMGTFY;


@app.route('/', methods=['POST'])
def vis_webhook():
    incoming_json = request.get_json()

    TELEGRAM_URL = 'https://api.telegram.org/bot647751837:AAFjJTwsxEmsEJyJFDsUFEA3fjGJ0Cknvwc/sendMessage'

    payload = {
        "chat_id": "407352782",
        "text": "None",
        "parse_mode": "HTML"
    }

    chat_id = incoming_json["message"]["chat"]["id"]
    chat_message = incoming_json["message"]["text"]

    isHowQuestion = chat_message.find('how')

    if isHowQuestion >= 0:
        payload["text"] = setLMGTFY(chat_message, isHowQuestion)
        payload["chat_id"] = chat_id
        requests.post(TELEGRAM_URL, payload)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run()