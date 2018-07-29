from flask import Flask, request, abort
from random import randint
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from commands.exchange import exchange
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
    if text.startswith("/"):
        parsed = text[1:].split(" ", 1)
        command = parsed[0]
        if len(parsed) > 1:
            args = parsed[1]
        else:
            args = ""
        if command == "yn":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=yesorno(args)))
        elif command == "pick":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=pick(args)))
        elif command == "convert":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=convert(args)))
        elif command == "help":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=help(args)))


def yesorno(str):
    if len(str) > 0:
        return str + '\n' + answer[randint(0, 2)]
    else:
        return help("yn")

def pick(str):
    list = str.split('/')
    if len(list) > 0:
        return list[randint(0, len(list))-1]
    else:
        return help("pick")


def convert(str):
    args = str.split(" ")
    if len(args) == 3:
        return exchange.convertecurrencyrates(args[0], args[1], args[2])
    elif len(args) == 2:
        return exchange.convertecurrencyrates(args[0], args[1])
    else:
        return help("convert")


def help(str):
    if str == "convert":
        return "Convert currency rate from one currency to another. Will return calculated value if amount is given.\n" + \
               "Usage:\n" + \
               "/convert <base_currency> <destination_currency> [<amount>]\n\n" + \
               "Example:\n" + \
               "/convert USD IDR\n" + \
               "/convert USD IDR 10"
    elif str == "yn":
        return "Ask this bot to approve, disapprove, or doubt anything you tell her!\n" + \
               "Usage:\n" + \
               "/yn <insert question here>\n\n" + \
               "Example\n" + \
               "/yn Do you like cookies?"
    elif str == "pick":
        return "Can't pick anything from a set of choice? Use this command to let the bot choose for you!\n" + \
               "Usage:\n" + \
               "/pick <a choice>/<another choice>/<unlimited choice works>\n\n" + \
               "Example:\n" + \
               "/pick indomie/mie seda/pop mie\n"
    else:
        return "List of commands: convert, yn, pick.\n" + \
               "Use /help <commands> for more info."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)