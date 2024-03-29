from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ORatwK0+RL6H6NU13zfg+8tgoRmC7dtnufB46iU5zJ5FyPGC3sTfKOe0avdijOK85rgdukRna7w1+h2OwuwScfLSsjnvqMtN0QtMshY+dHkS2xhOIIAQv/b6ecejZjsaDp66gxgcblqA6+4zFfL08QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('66fe8f641f703556898581fd0c97e6bd')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
