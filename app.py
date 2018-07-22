from flask import Flask, request, abort
from random import randint

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os


app = Flask(__name__)


line_bot_api = LineBotApi('aOlL2EKMOiD6aA+K5w9/F1knxQ762If9+bX6bWs2Ve7DIs66KOw06W4FPlfO2QSbROJ47y4MEMVytwyJ4UVFNbnmUtlmH24sdbe4n2bgfBXZvyO/ZyPQOGAAzW46wsurGzIRGFfABFCd5JF0QupwuwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8c3378230678cf4ea511e84af24aefc9')

# variables for answer from yes or not
answer = ['Yes', 'No', 'Perhaps']


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text.startswith("/yn") and len(text) > 5:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=yesOrNo(text[4:])))
    elif text.startswith("/pick") and len(text) > 7:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pick(text[6:])))


def yesOrNo(str):
    return str + '\n' + answer[randint(0,2)]


def pick(str):
    list = str.split('/')
    if len(list) > 0:
        return list[randint(0, len(list))-1]
    else:
        return 'Please specify your question!'


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)