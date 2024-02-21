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
                original_content_url = "https://www.google.com/search?q=%E8%B2%93%E5%92%AA&tbm=isch&ved=2ahUKEwiUlPfH4byEAxXFXvUHHR_eCMMQ2-cCegQIABAA&oq=%E8%B2%93%E5%92%AA&gs_lp=EgNpbWciBuiyk-WSqjIFEAAYgAQyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARI4BxQrhNYuBpwAHgAkAEAmAE7oAGfAqoBATe4AQPIAQD4AQGKAgtnd3Mtd2l6LWltZ8ICBBAjGCfCAgcQABiABBgYiAYB&sclient=img&ei=mxjWZdTaKsW91e8Pn7yjmAw&bih=632&biw=1396&prmd=nivsbmtz&rlz=1C1VDKB_zh-TWTW954TW954#imgrc=UJOVbdwXLXE1mM",
                preview_image_url = "https://www.google.com/search?q=%E8%B2%93%E5%92%AA&tbm=isch&ved=2ahUKEwiUlPfH4byEAxXFXvUHHR_eCMMQ2-cCegQIABAA&oq=%E8%B2%93%E5%92%AA&gs_lp=EgNpbWciBuiyk-WSqjIFEAAYgAQyCBAAGIAEGLEDMggQABiABBixAzIIEAAYgAQYsQMyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgARI4BxQrhNYuBpwAHgAkAEAmAE7oAGfAqoBATe4AQPIAQD4AQGKAgtnd3Mtd2l6LWltZ8ICBBAjGCfCAgcQABiABBgYiAYB&sclient=img&ei=mxjWZdTaKsW91e8Pn7yjmAw&bih=632&biw=1396&prmd=nivsbmtz&rlz=1C1VDKB_zh-TWTW954TW954#imgrc=UJOVbdwXLXE1mM")
        line_bot_api.reply_message(event.reply_token, message)
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
