from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, CallbackContext
import json
import os

# Вставьте здесь ваш токен бота
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Файл для хранения данных
DATA_FILE = "data.json"

# Минимальное и максимальное количество подписчиков
MIN_SUBSCRIBERS = 2
MAX_SUBSCRIBERS = 3

# Функция для загрузки данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"count": 0}

# Функция для сохранения данных
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id

    data = load_data()
    data["count"] += 1
    save_data(data)

    update.message.reply_text(f"Привет, {user.first_name}! Вы подписались на бота. Сейчас у нас {data['count']} подписчиков.")

    # Проверка на достижение минимального количества подписчиков
    if data["count"] == MIN_SUBSCRIBERS:
        context.bot.send_message(chat_id=chat_id, text="Ура! Мы достигли минимального количества подписчиков!")
        gif_file = InputFile("congratulations_min.gif")
        context.bot.send_animation(chat_id=chat_id, animation=gif_file)

    # Проверка на достижение максимального количества подписчиков
    if data["count"] == MAX_SUBSCRIBERS:
        context.bot.send_message(chat_id=chat_id, text="Поздравляем! Мы достигли максимального количества подписчиков!")
        gif_file = InputFile("congratulations_max.gif")
        context.bot.send_animation(chat_id=chat_id, animation=gif_file)

# Функция для обработки команды /count
def count(update: Update, context: CallbackContext) -> None:
    data = load_data()
    update.message.reply_text(f"Сейчас у нас {data['count']} подписчиков.")

# Функция для обработки команды /welcome
def welcome(update: Update, context: CallbackContext) -> None:
    if not context.bot.get_chat_member(update.message.chat_id, update.message.from_user.id).status in ['administrator', 'creator']:
        update.message.reply_text("Эта команда доступна только администраторам.")
        return

    welcome_message = "Добро пожаловать в нашу группу! Мы рады видеть вас здесь."
    update.message.reply_text(welcome_message)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("count", count))
    dispatcher.add_handler(CommandHandler("welcome", welcome))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
