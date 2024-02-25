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
import random
#import json
#======python的函數庫==========

laugh=[
'有一天，有一群海底生物在考試 考著考著，老師發現蝦子居然作弊！ 老師很生氣的問蝦子：「你抄誰的！」 蝦子就很緊張的說： . . . . . . . . . . . . . 「我...我超蚌der！」',
'有一天，好帥氣、好美麗、好棒棒三個人去游泳，好美麗跟好棒棒都溺水了，好帥氣把好美麗救上岸後就打算離開⋯，好美麗就說：「阿不救好棒棒」',
'有一天 你好、安安、哈囉 三個人要出去玩 你好開家裡的車載大家 結果過了很久都還沒去接安安 後來到了安安家後 安安很生氣的質問你好 「你是載哈囉？」',
'有一天🦀在沙灘上走著走著撞到了🐢 \n海龜說：你瞎子嗎😡 \n螃蟹回：不 我是螃蟹',
'有一天海底動物舉辦跑步比賽，蝦子當裁判，並大喊 預備～起！\n結果魚就哭了\n牠哭著說：蝦子罵我北七ヾ(;ﾟ;Д;ﾟ;)ﾉﾞ',
'有一天蝦子、魚、螃蟹相約出去玩，結果魚遲到了\n他們只好 = =',
'有一天迷路在森林裡走丟了，於是他打電話給長頸鹿\n鹿：為我迷路啦\n長頸鹿：我長頸鹿啦。',
'有一天小智去車行看車\n經理問：請問預算、廠牌？\n小智說：十萬、福特\n經理就被電死了。',
'有一個人去餐廳點了一個漢堡，取餐時卻多了一杯可樂，於是問店員說：這是附的嗎？\n店員說：這是drink。',
'小明到醫院看病\n醫生：張開嘴巴，啊\n小明：啊\n醫生：喉嚨發炎\n喉嚨：嗨',
'A:先生你好這是我們招待的小菜\nB:不用了謝謝\nA:確定嗎，這是你的筍絲喔'
]

joke=[
['為什麼不能把橄欖樹種在一起？','因為會群聚感染'],
['有一隻深海魚遊著遊著就哭了，為什麼？','因為他壓力很大。'],
['L 以前叫什麼？','Led'],
['那個職業最不會受傷？','零售商'],
['哈利波特那個角色最有主見？','佛地魔\n因為他不會被牽著鼻子走'],
['運氣不好要去哪裡？','轉運站'],
['一群公司主管出去吃飯，猜三個字？','幹部揪'],
['福原愛失憶會說什麼？','who am I?(一個酷酷的諧音耿'],
['香蕉一直加熱會變甚麼？','熱融膠'],
['有一本經書中描述著一個現象，上帝喜歡數人間路過的車輛，這種現象稱之為什麼？','天竺鼠車車(天主數車車)'],
['小明的師父想要傳授秘笈給小明，但小明卻一直不敢接受，為什麼？','因為他有密集恐懼症'],
['為什麼螃蟹會一直咳嗽？','因為他是甲殼類'],
['你知道警衛在笑什麼嗎？','在校門口'],
['做愛最慢的國家是哪？','斯洛伐克'],
['去七股鹽山不能幹嘛？','尿尿，因為會尿道鹽'],
['北部的奶茶叫什麼？','bubble milk tea'],
['你知道什麼島最熱嗎？','套中島'],
['為什麼去買麵的時候老闆都不會笑？','因為他是面攤老闆(麵攤老闆)'],
['一隻老鷹叫eagle，那兩隻老鷹叫什麼？','兩狗'],
['一隻老鷹叫eagle，那老鷹出國叫什麼？','trivago'],
['DNA想養狗，但一直被旁人阻止，為什麼？','因為大家都叫他去養核糖核酸(去氧核糖核酸)'],
['濁水溪和曾文溪為什麼是分開的？','因為它們不適合(不是河)'],
['佛陀開的店叫什麼？','photoshop(佛陀shop)'],
['哪個藝人頭最圓？','陶晶瑩(頭真圓的台語)'],
['哪個藝人會走路的時候走走停停？','趙又廷(台語)'],
['孤兒院最愛養什麼動物？','企鵝'],
['什麼車不容易被刮壞？','南瓜馬車'],
['自然捲為什麼不能當警察？','因為警察是執法人員(直髮人員)'],
['什麼東西會卡在肺裡？','city，因為city 卡肺(city coffee)'],
['柯南如果跳樓哪個角色會最難過？','灰原哀，因為：新一跳，哀就開始煎熬(「煎熬」歌詞)'],
['愛喝酒的是酒鬼\n好色的是色鬼\n那擋路的是？','舊鬼(借過台語)'],
['妳知道刮刮樂買多少比較容易中嗎？','500，因為500五保必'],
['8+9打全場籃球叫什麼？','10隻89'],
['茶最害怕什麼醬料？','沙茶醬'],
['一顆星星多種？','8公克，因為星巴克'],
['一個餐廳裡誰最厲害？','客人，因為他有點東西'],
['為什櫻花鉤吻鮭敢跟熊打架？','因為他特有種。'],
'''
['','']
['','']
['','']
['','']
['','']
['','']
['','']
['','']
['','']
['','']
['','']
['','']

為什麼去科學園區容易摔倒？因為很多半導體。
為什麼暖暖包到現在還一堆人在用？因為他有鐵粉。
為什麼很冷的時候要靠牆站？因為有90度。
為什麼超人要穿緊身衣？因為救人要緊。
為什麼吃完鮭魚肚子會痛？因為他在胃食道逆流。
你知道台灣第一個實況主是誰嗎？鄭成功，因為他是開台始祖。
蛤蜊確診會變什麼？居家隔離。
做車坐到哪一站會心臟不舒服？星際大戰。
如果你覺得冷就摸摸自己的肩膀，因為他是shoulder（台）。
飛機上有蛇第二集要叫什麼？飛機尚有蛇
為什麼sin跟cos不能一起唱歌？因為它們慢半拍
西班牙跟葡萄牙之間是什麼？牙縫
有一天，小明拿著帳單進去超商，但出來卻坐著輪椅，為什麼？因為他繳費了。
原住名腳斷掉猜一種蔬菜？番茄（番瘸）
把菲傭關起來猜一個國家？索馬利亞
間諜家家酒的主角叫做安尼亞，那間諜八加九呢？安尼亞雞掰啦。
你知道為什麼男生勃起不能往上嗎？因為他們無法反駁
工讀生被毒蛇咬了，傳line跟你求救，要怎麼辦？已讀他，以毒攻毒
一個0號走進一個滿是1號的gay bar，0號說:hello everyone
為什麼冷氣不會煮飯？因為他沒有打開除濕功能。
獵人打完手槍，會變什麼？以色列人
鴨子發不出聲音會變什麼蔬菜？南瓜
大陸打過來怎麼辦？不要接就好
老鼠死了會去哪裡？澳洲，袋鼠
唐寶寶天天刷牙會變什麼？口香糖
呂布看到什麼鳥要叫爸爸？啄木鳥，因為他董卓
為什麼吐司和起司出門，吐司的動作都很慢？因為起司蛋吐司
海裡有什麼東西好笑？海鰻，海鰻好笑的
牛奶最好喝幾次？九次，高鈣牛乳
小姐放假變什麼？休假
加菲貓為什麼流浪？因為他家飛了，
哪對字母湊在一起會爆炸？ok，ok蹦
衣服皺皺的要怎麼辦？拿進房吹變頻冷氣
為什麼大象躲在樹上不會被發現？因為他真的對躲得很好
地震是公的還是母的？公的，因為地震有幾級
'''
]

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
openai.api_key = os.getenv('OPENAI_API_KEY')

line_bot_api.push_message('U14064b6b005dcd289f44ef6a2c106a36',TextSendMessage('部屬完成') )


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
        '''
        json_data=json.loads(msg)
        type=json_data['events'][0]['message']['type']
        if(type=='image'):
            msgID = json_data['events'][0]['message']['id']
            message_content = line_bot_api.get_message_content(msgID)  # 根據訊息 ID 取得訊息內容
            # 在同樣的資料夾中建立以訊息 ID 為檔名的 .jpg 檔案
            with open(f'{msgID}.jpg', 'wb') as fd:
                fd.write(message_content.content)             # 以二進位的方式寫入檔案
            line_bot_api.reply_message(event.reply_token, TextSendMessage('圖片儲存完成！')) # 設定要回傳的訊息
            '''
        
        if(msg=='貓貓'):
            massage=ImageSendMessage(
            original_content_url = "https://hips.hearstapps.com/hmg-prod/images/domestic-gray-tabby-cat-with-an-orange-nose-is-royalty-free-image-1686039395.jpg?crop=0.668xw:1.00xh;0.264xw,0&resize=980:*",
            preview_image_url = "https://hips.hearstapps.com/hmg-prod/images/domestic-gray-tabby-cat-with-an-orange-nose-is-royalty-free-image-1686039395.jpg?crop=0.668xw:1.00xh;0.264xw,0&resize=980:*")
            line_bot_api.reply_message(event.reply_token, massage)
        #elif(msg=='笑話'):
            
        if(msg=='余爾佑出來'):
            massage=ImageSendMessage(
            original_content_url = "https://upload.cc/i1/2024/02/22/S4RsOU.png",
            preview_image_url = "https://upload.cc/i1/2024/02/22/S4RsOU.png")
        line_bot_api.reply_message(event.reply_token, massage)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))

        if(msg=='謎題'):
            d=1
            haa=random.randint(0,len(joke))
            message=joke[haa][0]
            line_bot_api.reply_message(event.reply_token,message)

        if(msg=='為什麼' and d==1):
            d=0
            message=joke[haa][1]
            line_bot_api.reply_message(event.reply_token,message)
            
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('gg')) # 設定要回傳的訊息
    '''
    try:
        GPT_answer = GPT_response(msg)
        print(GPT_answer)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
    except:
        print(traceback.format_exc())
        line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息3'))
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
