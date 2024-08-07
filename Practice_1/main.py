from telebot import TeleBot, types
from random import choice
from config import BOT_TOKEN
from messages import start_message, help_message
from jokes import RANDOM_JOKES

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start_handler(message: types.Message):
    bot.send_message(
        message.chat.id,
        start_message
    )


@bot.message_handler(commands=["help"])
def help_handler(message: types.Message):
    bot.send_message(
        message.chat.id,
        help_message
    )


@bot.message_handler(commands=["joke"])
def send_joke(message: types.Message):
    text = choice(RANDOM_JOKES)
    bot.send_message(
        message.chat.id,
        text
    )


@bot.message_handler()
def echo_message(message: types.Message):
    text = message.text

    if 'привет' in text.lower():
        text = 'И тебе привет!'
    elif 'как дела' in text.lower():
        text = 'Хорошо! А у вас как?'
    elif ('пока' in text.lower()) or ('до свидания' in text.lower()):
        text = 'До новых встреч!'

    bot.send_message(
        message.chat.id,
        text
    )


bot.infinity_polling(skip_pending=True)
