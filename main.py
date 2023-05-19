import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import requests
from bs4 import BeautifulSoup
import random

def start(update, context):
    """Отправка сообщений при выполнении команды /start."""
    update.message.reply_text('Привет! Я могу прислать тебе картинку или мем небольшого размера, для быстрой пересылки твоим бро! Что бы ты хотел получить? Я уже готов!')
    update.message.reply_text('Правила запросов указаны в Меню')

def help(update, context):
    """Отправка сообщений при выполнении команды /help."""
    update.message.reply_text('🖼 Для получения картинки напиши: картинка "пробел" запрос, либо сразу запрос')
    update.message.reply_text('🤣 Для получения мема напиши: мем "пробел" запрос')
    update.message.reply_text('🖐 Можешь отправить Эмодзи, в ответ я пришлю на него реакцию в виде картинки')



def send_picture(update, context):
    """Отправка изображения, когда пользователь отправляет сообщение "картинка"."""
    text = update.message.text
    query = text.split('картинка ')[-1]
    url = f'https://www.google.com/search?q={query}&tbm=isch'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    images = soup.findAll('img')
    random_image = random.choice(images)
    pic_url = random_image['src']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic_url)

def send_meme(update, context):
    """Отправка изображения, когда пользователь отправляет сообщение "мем"."""
    text = update.message.text
    query = text.split('мем ')[-1]
    url = f'https://www.reddit.com/r/dankmemes/search?q={query}&restrict_sr=1'
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    memes = soup.findAll('div', {'class': '_2_tDEnGMLxpM6uOa2kaDB3'})
    random_meme = random.choice(memes)
    pic_url = random_meme.find('img')['src']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=pic_url)

def main():
    """Запуск бота."""
    # Создаем Updater и подключаем токем для бота.
    updater = Updater("6282254473:AAEW7jjogDI1vGf9Tt4wDdzb40clToL7d3k", use_context=True)

    # Регистрация обработчика
    dp = updater.dispatcher

    # Ответы на команды в Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # Повторить сообщение в Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, send_picture))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, send_meme))

    # Запустить бота
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()