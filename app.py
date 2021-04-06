from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
# (
#     FollowEvent, MessageEvent, TextMessage,ButtonsTemplate,
#     TextSendMessage, StickerSendMessage, TemplateSendMessage
# )
import requests,pandas,os,random
from pyquery import PyQuery as pq

app = Flask(__name__)

line_bot_api = LineBotApi(
    'i76IuvwpBRgV3j2jkLcQ73fy0InOTA3fExe0u0hX4LSd74KWbV1Nt8Rik+vTIhkzIZuo8ksuhBSXMk3eiYzV418EcuRkYc0o+1jOsR79pTExl6VmbkfTOdUAn3DToeE+o7EUkicZsh2uOu4IZXSAxAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e96dc58fc1d8eeacb4d9c794eecf8e64')


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# @app.route("/",methods=['GET'])
# def main_test_page():
#     # line_bot_api.push_message(
#         # "U5387d7168fd38f08da16ec6c70871cca", TextSendMessage(text="校網已更新"))
#     file_path = str(os.path.dirname(__file__))
#     return '<a href="/result.csv" download="result.csv">result.csv</a>'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.push_message(
    #     "U5387d7168fd38f08da16ec6c70871cca", TextSendMessage(text=event.message.text))
    # profile = line_bot_api.get_profile(event.source.user_id)
    # print(profile.display_name)
    # global guestNumberGame

    user_id = event.source.user_id

    if event.message.text == "猜數字":
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="請輸入4個不重複的數字從0~9"))
        guestNumberGame.__init__()
        guestNumberGame.on = True
        print(guestNumberGame.answer)

    if guestNumberGame.on:
        if event.message.text == "答案":
            ans = "".join(guestNumberGame.answer)
            print(guestNumberGame.answer)
            line_bot_api.push_message(
                user_id, TextSendMessage(text=ans))
            print(ans)
            # guestNumberGame.on = False
        elif event.message.text.isdigit():
            num_a,num_b =  guestNumberGame.check(event.message.text)
            if num_a == 4:
                line_bot_api.reply_message(
                    event.reply_token,StickerSendMessage(1,13))
                Confirm_template = TemplateSendMessage(
                    alt_text='目錄 template',
                    template=ConfirmTemplate(
                        title='ConfirmTemplate',
                        text='繼續玩？',
                        actions=[
                            PostbackTemplateAction(
                                label='Y',
                                text='Y',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='N',
                                text='N'
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, Confirm_template)
                
                
            else:
                line_bot_api.push_message(
                    user_id, TextSendMessage(text="%dA%dB"%(num_a,num_b)))


    # print(event.source.user_id)

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

@handler.add(FollowEvent, message=TextMessage)
def someone_follow(event):
    line_bot_api.push_message(
        "U5387d7168fd38f08da16ec6c70871cca", TextSendMessage(text="有人將機器人加為好友"))


class GuestNumberGame():

    def __init__(self):
        print("\ninit \n\n")
        d = [str(i) for i in range(9)]
        self.answer = random.sample(d,4)
        self.record = []
        self.on = False

    def check(self, num):
        a = 0
        b = 0
        # print(self.answer)
        # print(num)
        for i in range(4):
            if num[i] == self.answer[i]:
                # print("A")
                a += 1
            elif num[i] in self.answer:
                # print("B")
                b += 1
        return a, b



guestNumberGame = GuestNumberGame()
if __name__ == "__main__":
    app.run()
    
