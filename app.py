from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import openai

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
import traceback
import random
import sys
#import json
#======python的函數庫==========

d=0
laugh=[
['有一天，有一群海底生物在考試\n考著考著，老師發現蝦子居然作弊！\n老師很生氣的問蝦子：「你抄誰的！」\n蝦子就很緊張的說：...「我...我超蚌der！」'],
['有一天，好帥氣、好美麗、好棒棒三個人去游泳\n好美麗跟好棒棒都溺水了\n好帥氣把好美麗救上岸後就打算離開⋯\n好美麗就說：「阿不救好棒棒」'],
['有一天 你好、安安、哈囉 三個人要出去玩\n你好開家裡的車載大家\n結果過了很久都還沒去接安安\n後來到了安安家後\n安安很生氣的質問你好：「你是載哈囉？」'],
['有一天🦀在沙灘上走著走著撞到了🐢 \n海龜說：你瞎子嗎😡 \n螃蟹回：不 我是螃蟹'],
['有一天海底動物舉辦跑步比賽，蝦子當裁判，並大喊 預備～起！\n結果魚就哭了\n牠哭著說：蝦子罵我北七ヾ(;ﾟ;Д;ﾟ;)ﾉﾞ'],
['有一天蝦子、魚、螃蟹相約出去玩，結果魚遲到了\n他們只好 = ='],
['有一天迷路在森林裡走丟了，於是他打電話給長頸鹿\n鹿：為我迷路啦\n長頸鹿：我長頸鹿啦。'],
['有一天小智去車行看車\n經理問：請問預算、廠牌？\n小智說：十萬、福特\n經理就被電死了。'],
['有一個人去餐廳點了一個漢堡，取餐時卻多了一杯可樂\n於是問店員說：這是附的嗎？\n店員說：這是drink。'],
['小明到醫院看病\n醫生：張開嘴巴，啊\n小明：啊\n醫生：喉嚨發炎\n喉嚨：嗨'],
['A:先生你好這是我們招待的小菜\nB:不用了謝謝\nA:確定嗎，這是你的筍絲喔'],
['一個0號走進一個滿是1號的gay bar\n0號說:hello everyone'],
['有一天小明打電話給電話客服\n客服：很高興為您服務\n小明：你高興的太早了\n於是小明就把電話掛掉了'],
['我出門前對桌上的隱形眼鏡說：\n\n我根本沒把妳放在眼裡'],
['我：醫生，我手術後要多久才能拉小提琴？\n醫生：一個月。\n我：謝謝你，我本來不會拉的！'],
['有兩隻螞蟻在沙灘上，為什麼看不到他們的足跡？','因為他們騎腳踏車','那為什麼小明不用開冰箱就知道冰箱長螞蟻？','A:因為冰箱旁邊停著兩輛腳踏車']
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
['為什櫻花鉤吻鮭敢跟熊打架？','因為他特有種'],
['為什麼去科學園區容易摔倒？','因為很多半導體'],
['為什麼暖暖包到現在還一堆人在用？','因為他有鐵粉'],
['為什麼很冷的時候要靠牆站？','因為有90度'],
['為什麼超人要穿緊身衣？','因為救人要緊'],
['為什麼吃完鮭魚肚子會痛？','因為他在胃食道逆流'],
['你知道台灣第一個實況主是誰嗎？','鄭成功，因為他是開台始祖'],
['蛤蜊確診會變什麼？','居家隔離'],
['做車坐到哪一站會心臟不舒服？','星際大戰'],
['為什麼肩膀是熱的？','因為他是shoulder（熱的台語）'],
['飛機上有蛇第二集要叫什麼？','飛機尚有蛇'],
['為什麼sin跟cos不能一起唱歌？','因為它們慢半拍'],
['西班牙跟葡萄牙之間是什麼？','牙縫'],
['有一天，小明拿著帳單進去超商，但出來卻坐著輪椅，為什麼？','因為他繳費了(腳廢了)'],
['間諜家家酒的主角叫做安尼亞，那間諜八加九呢？','安尼亞雞掰啦'],
['工讀生被毒蛇咬了，傳line跟你求救，你要怎麼辦？','已讀他，以毒攻毒'],
['為什麼冷氣不會煮飯？','因為他沒有打開除濕功能'],
['鴨子發不出聲音會變什麼蔬菜？','南瓜(難呱)'],
['大陸打過來怎麼辦？','不要接就好'],
['老鼠死了會去哪裡？','澳洲，因為有很多袋鼠(die鼠)'],
['呂布看到什麼鳥要叫爸爸？','啄木鳥，因為他董卓'],
['為什麼吐司和起司出門，吐司的動作都很慢？','因為起司蛋吐司(台語)'],
['海裡有什麼東西好笑？','海鰻，海鰻好笑的'],
['牛奶最好喝幾次？','九次，因為高鈣牛乳(台語)'],
['小姐放假變什麼？','休假(台語)'],
['加菲貓為什麼流浪？','因為他家飛了'],
['哪對字母湊在一起會爆炸？','ok，ok蹦'],
['衣服皺皺的要怎麼辦？','拿進房吹變頻冷氣'],
['為什麼大象躲在樹上不會被發現？','因為他真的對躲得很好'],
['地震是公的還是母的？','公的，因為地震有幾級'],
['曹操字孟德\n劉備字玄德\n伍佰呢？','五百字心得']
]

hell=[
['唐寶寶天天刷牙會變什麼？','口香糖'],
['原住名腳斷掉猜一種蔬菜？','番茄（番瘸）'],
['把菲傭關起來猜一個國家？','索馬利亞'],
['你知道為什麼男生勃起不能往上嗎？','因為他們無法反駁'],
['獵人打完手槍，會變什麼？','以色列人'],
]


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
openai.api_key = os.getenv('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')
CHATGPT_API_URL = 'https://api.openai.com/v1/chat/completions'
CHATGPT_API_KEY = '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'

# OPENAI API Key初始化設定
#openai.api_key = 'OPENAI_API_KEY'

line_bot_api.push_message('U14064b6b005dcd289f44ef6a2c106a36',TextSendMessage('部屬完成') )


def GPT_response(text):
    # 接收回應
    response = OpenAI().Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer
    
def chat_with_gpt(user_input):
    try:
        # 設定提示語句，將使用者輸入的訊息與回覆模板結合
        prompt = f"{user_input}\n\nResponse:"
        # 使用OpenAI API，傳遞模型名稱、訊息角色和內容，以生成機器人回覆
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
        )
        # 從回覆中提取機器人的回覆訊息，並去除前後空白
        result = response['choices'][0]['message']['content'].strip()
        return result # 返回處理過的回覆給LINE使用者
    except openai.Error as e:
        return "Error: OpenAI API"
    except Exception as e:
        return "Error: An unexpected error occurred"

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
        id = event.source.user_id

        if(msg[0:1]=='AI'):
            res=chat_with_gpt(msg[3:])
            line_bot_api.reply_message(event.reply_token, TextSendMessage(res))
            line_bot_api.push_message('U14064b6b005dcd289f44ef6a2c106a36',TextSendMessage('in'))


        
        if(msg=='有什麼功能'):
            line_bot_api.reply_message(event.reply_token, TextSendMessage('輸入 笑話 聽一則笑話\n輸入 冷笑話 獲取一個冷笑話\n輸入 加笑話(你要加入的笑話) 讓我加入你的笑話\n目前功能沒有很多\n如果有想要加入什麼功能，輸入：!(你想說的話)，來通知作者'))
        
        if(msg=='貓貓'):
            message=ImageSendMessage(
            original_content_url = "https://hips.hearstapps.com/hmg-prod/images/domestic-gray-tabby-cat-with-an-orange-nose-is-royalty-free-image-1686039395.jpg?crop=0.668xw:1.00xh;0.264xw,0&resize=980:*",
            preview_image_url = "https://hips.hearstapps.com/hmg-prod/images/domestic-gray-tabby-cat-with-an-orange-nose-is-royalty-free-image-1686039395.jpg?crop=0.668xw:1.00xh;0.264xw,0&resize=980:*")
            line_bot_api.reply_message(event.reply_token, message)
        if(msg[0]=='!'):
            message=msg[1:]
            line_bot_api.push_message('U14064b6b005dcd289f44ef6a2c106a36',TextSendMessage(message))
        if(msg[0:2]=='加笑話'):
            message=msg[3:]
            line_bot_api.push_message('U14064b6b005dcd289f44ef6a2c106a36',TextSendMessage(message))
        if(msg=='余爾佑'):
            message=ImageSendMessage(
            original_content_url = "https://upload.cc/i1/2024/02/22/S4RsOU.png",
            preview_image_url = "https://upload.cc/i1/2024/02/22/S4RsOU.png")
            line_bot_api.reply_message(event.reply_token, message)
        if(msg=='許書絃'):
            message=ImageSendMessage(
            original_content_url = "https://i.ibb.co/Jkkw0yp/IMG-4604.jpg",
            preview_image_url = "https://i.ibb.co/Jkkw0yp/IMG-4604.jpg")
            line_bot_api.reply_message(event.reply_token, message)
            

        if(msg=='冷笑話'):
            lengh=len(joke)
            haa=random.randint(1,lengh)
            message=joke[haa-1][0]
            line_bot_api.reply_message(event.reply_token,TextSendMessage(message))
            time.sleep(7.5)
            message=joke[haa-1][1]
            line_bot_api.push_message(id,TextSendMessage(message))

        if(msg=='地獄笑話'):
            lengh=len(hell)
            hel=random.randint(1,lengh)
            message=hell[hel-1][0]
            line_bot_api.reply_message(event.reply_token,TextSendMessage(message))
            time.sleep(7.5)
            message=hell[hel-1][1]
            line_bot_api.push_message(id,TextSendMessage(message))

        if(msg=='笑話'):
            lengh=len(laugh)
            lau=random.randint(1,lengh)
            laulen=len(laugh[lau-1])
            if(laulen==1):
                message=laugh[lau-1][0]
                line_bot_api.reply_message(event.reply_token,TextSendMessage(message))
            else:
                for i in range(laulen):
                    message=laugh[lau-1][i]
                    line_bot_api.push_message(id,TextSendMessage(message))
                    time.sleep(5)
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))

       
            
    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(errMsg)) # 設定要回傳的訊息
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
