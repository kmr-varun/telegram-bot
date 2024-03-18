import telebot
from pyairtable import Api

from keep_alive import keep_alive
keep_alive()

bot = telebot.TeleBot("6744089416:AAH_Mlsqkwtm16MpG-B-epnK8N_cWZKqaqE")
token = 'patThcgATHQGPJC7g.a6c6f1407e17d116c5160333d0c19901677e2ed2cbbd7f431f313ea06dd5a5f3'
api = Api(token)
table = api.table(base_id='appNhV3tkj9e5xXy8',table_name='vid_data')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    id = message.text.replace("/start ", "")

    if(id == ''):
        bot.send_message(message.chat.id, 'Hello')
    else:
        records = table.get(id)
        bot.send_video(message.chat.id, records['fields']['vlink'], protect_content=True)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    if message.from_user.id == 1590174243:
        video = message.video
        file_info = bot.get_file(video.file_id)
        records = table.create({'vlink': video.file_id})
        image_path = 'thumb.png'
        bot.send_photo('-4135712186', open(image_path, 'rb'), caption='Here is the Link \n Link: https://t.me/thundr_uploader_bot?start=' + records['id'])
        
        bot.reply_to(message, "Video Sent Successfully!")
    else:
        bot.send_message(message.chat.id, 'Hello')
    

bot.infinity_polling()