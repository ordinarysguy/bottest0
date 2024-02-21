from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
openai.api_key = os.getenv('OPENAI_API_KEY')


def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(進入chatgpt))
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer


# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        msg = event.message.text
        massage=ImageSendMessage(
                original_content_url = "https://lh3.googleusercontent.com/pw/ABLVV84uV8h6k1tHJgssMxpM2GSylRNCUwSgj-D7nnF7ov3H6J2y_rV_oBQp1-wKWH15l8v7OwQ5ojW1okaU0jSeagv0A1wM7YzCWg9m1GuN2dHkHCFTQ65ckVHWRHRfLFFO-BsqTxxWjt9OIKELsyx3tu7SQubaUOS1TWCp-Zd6gYQdihHraxqE7k6GgWTKHKcCvNBY93rY5Xy6uvYHw8mLwluuJC5Vf3Ue9jWNdqZXG2Tj3hPdqAO_Qkz9jPBUN-aw12k0QCV9v0sLX6cSEPckdHg916HFGNwsc_3P2cIGt3vmZmnIsx3MMsXOnW9XPgaiADKExnZSBYl9_CnP5NiiexHpTbnClqJ-w1l8rfjXrTv_EVXRRZ3OkQMl2b9GuZ99A9h7Kq7F2KrfPCUqphUyC-8uQyogUQhGqGrzyOpSd9Jv53zhU17zU99l9605PmaOMmUvb-yaPGrfS9EHTooPjLyNtZZuLkdDIUyMZsIMB-1r_JvlG0LLkyw7oVg5C0HZ3mBtI-K1XPUIzo2jUrkbqk1jV5tonkkx7Tnts8wog_UQlMjqpBu11e4ib3LWL3yxV1BqZRAo26Kw99FngAsgaWLdy-bI3pYUftnNUreaqFkFHUQ-T4h0BqoLnRV4Wlg-74LqBtIPzLHTw2kMhdARmem-Q36QmeuKh37X5AdJ33rLQMN9uSxr5DON5rdMavscs3a6H84reFySe1bjz-OvJjOcTEF0VA_-K60lVxdFHV4bGnspMVGD9gSEY8MO8WxUNNl_KMps8KmwumPxqi4aKZ8gco0GcNA939wxKDppPB3DGArFJQQzTTKs0Om91yCZzc9sDAxWeIX8EV5X_WnWdT-Vd5Fc9NBVhHWsDxJWnc5fohl46CVNkncFyl7zw1BZZxJqPzTytfXEC6nII_jib2rl5Q9tHnXGU_u4zGwt5HEiD11R0g6O-qC5BtC0=w401-h869-s-no-gm?authuser=0",
            preview_image_url = "https://hips.hearstapps.com/hmg-prod/images/domestic-gray-tabby-cat-with-an-orange-nose-is-royalty-free-image-1686039395.jpg?crop=0.668xw:1.00xh;0.264xw,0&resize=980:*")
        line_bot_api.reply_message(event.reply_token, massage)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage("Gg"))
    '''
    try:
        GPT_answer = GPT_response(msg)
        print(GPT_answer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except:
        print(traceback.format_exc())
        line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息2'))
    '''
        

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
