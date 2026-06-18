import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = '8533255433:AAGHOhhGY2GMAjCAnSWq8TYaLTigXxs2cTU'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Я помогу тебе скачать видео из TikTok или Instagram Reels.\n"
                          "Просто отправь мне ссылку на видео!")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    
    if not url.startswith("http"):
        bot.reply_to(message, "❌ Пожалуйста, отправь корректную ссылку, начинающуюся с http...")
        return

    status_msg = bot.reply_to(message, "⏳ Начинаю скачивание видео... Подождите немного.")

    # Облегченные настройки скачивания (ищем уже готовый mp4/ext файл)
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',
        'format': 'b[ext=mp4]/b',  # скачиваем сразу готовый mp4, чтобы не требовать склейки
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if not os.path.exists(filename):
                filename = filename.rsplit('.', 1)[0] + '.mp4'

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="🎬 Вот твое video!\nСкачано через @MyDownloaderSuper_bot")

        bot.delete_message(message.chat.id, status_msg.message_id)
        os.remove(filename)

    except Exception as e:
        print(f"Ошибка в консоли: {e}")
        bot.edit_message_text(f"❌ Не удалось скачать видео. Попробуй другую ссылку.\n(Ошибка: {str(e)[:50]})", 
                              message.chat.id, status_msg.message_id)
        
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

print("Бот-скачиватель успешно запущен...")
bot.polling(none_stop=True)
