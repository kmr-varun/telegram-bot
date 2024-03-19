import os
import telebot
import csv
import random
import string
from ffmpeg import FFmpeg

# from keep_alive import keep_alive
# keep_alive()

bot = telebot.TeleBot("6744089416:AAH_Mlsqkwtm16MpG-B-epnK8N_cWZKqaqE")

DOWNLOAD_DIR = 'data'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def generate_unique_id(existing_ids):
    while True:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if new_id not in existing_ids:
            return new_id

def get_existing_ids():
    existing_ids = set()
    with open('video_ids.csv', 'r', newline='') as csvfile:
        video_reader = csv.reader(csvfile)
        for row in video_reader:
            existing_ids.add(row[0])
    return existing_ids

def get_video_id_by_name(video_name):
    with open('video_ids.csv', 'r', newline='') as csvfile:
        video_reader = csv.reader(csvfile)
        for row in video_reader:
            if row[0] == video_name:
                return row[1]
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    id = message.text.replace("/start ", "")
    if(id == ''):
        bot.send_message(message.chat.id, 'Hello')
    else:
        records = get_video_id_by_name(id)
        bot.send_video(message.chat.id, records, protect_content=True)

@bot.message_handler(commands=['get_data'])
def send_data(message):
    if message.from_user.id == 1590174243:
        try:
            file_path = 'video_ids.csv'
            bot.send_document(message.chat.id, open(file_path, 'rb'))
        except Exception as e:
            bot.reply_to(message, "Error sending file: " + str(e))
    else:
        bot.reply_to(message, "Hello")

@bot.message_handler(commands=['add_data'])
def send_data(message):
    if message.from_user.id == 1590174243:
        try:
            id = message.text.replace("/add_data  ", "")
            nids = id.split(',')
            with open('video_ids.csv', 'a', newline='') as csvfile:
                video_writer = csv.writer(csvfile)
                video_writer.writerow([nids[0], nids[1]])
            bot.reply_to(message, "File Updated")
        except Exception as e:
            bot.reply_to(message, "Error sending file: " + str(e))
    else:
        bot.reply_to(message, "Hello")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    if message.from_user.id == 1590174243:
        video = message.video
        video_file = bot.get_file(video.file_id)
        existing_ids = get_existing_ids()
        unique_id = generate_unique_id(existing_ids)
        video_path = unique_id + '.mp4'
        thumb_path = unique_id + '.jpg'
        downloaded_file = bot.download_file(video_file.file_path)
        video_file_path = os.path.join(DOWNLOAD_DIR, video_path)
        with open(video_file_path, 'wb') as f:
            f.write(downloaded_file)
        
        ffmpeg = FFmpeg().input(os.path.join(DOWNLOAD_DIR, video_path), {"ss": "00:00:05"}).output(os.path.join(DOWNLOAD_DIR, thumb_path), {"vframes": "1"})
        ffmpeg.execute()
        with open('video_ids.csv', 'a', newline='') as csvfile:
            video_writer = csv.writer(csvfile)
            video_writer.writerow([unique_id, video.file_id])
        image_path = thumb_path
        bot.send_photo('-4135712186', open(os.path.join(DOWNLOAD_DIR, thumb_path), 'rb'), caption='Here is the Link \n Link: https://t.me/thundr_uploader_bot?start=' + unique_id)
        os.remove(os.path.join(DOWNLOAD_DIR, video_path))
        os.remove(os.path.join(DOWNLOAD_DIR, thumb_path))
        bot.reply_to(message, "Video Sent Successfully!")
    else:
        bot.send_message(message.chat.id, 'Hello')
    

bot.infinity_polling()