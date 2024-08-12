from telebot import TeleBot, types
from telebot import formatting
from telebot import util

from random import choice

from io import StringIO

import config
import messages
import my_filters
import currencies

from messages import start_message, help_message
from jokes import RANDOM_JOKES

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(my_filters.HasEntitiesFilter())
bot.add_custom_filter(my_filters.ContainsAtLeastOneOfWordsFilter())


@bot.message_handler(commands=["start"])
def start_handler(message: types.Message):
    bot.send_message(
        message.chat.id,
        start_message,
        parse_mode="HTML"
    )


@bot.message_handler(commands=["help"])
def help_handler(message: types.Message):
    bot.send_message(
        message.chat.id,
        help_message,
        parse_mode='HTML'
    )


@bot.message_handler(commands=["joke"])
def send_joke(message: types.Message):
    text = choice(RANDOM_JOKES)
    bot.send_message(
        message.chat.id,
        text
    )


@bot.message_handler(commands=["dogs"])
def send_dogs_photo(message: types.Message):
    bot.send_photo(
        message.chat.id,
        config.DOGS_PIC_URL,
        reply_to_message_id=message.id
    )


@bot.message_handler(commands=["dogs_file"])
def send_dogs_photo_as_file(message: types.Message):
    bot.send_document(
        message.chat.id,
        config.DOGS_PIC_URL,
        reply_to_message_id=message.id
    )


@bot.message_handler(commands=["me"])
def send_info_about_user_as_doc(message: types.Message):
    file = StringIO()
    file.write("Информация о пользователе:\n")
    file.write("User id: " + str(message.from_user.id) + "\n")
    file.write("First name: " + str(message.from_user.first_name) + "\n")
    file.write("Last name: " + str(message.from_user.last_name) + "\n")
    file.write("Username: " + str(message.from_user.username) + "\n")
    file.write("Is bot: " + str(message.from_user.is_bot))
    file.seek(0)
    file_text_doc = types.InputFile(file_name="your-info.txt", file=file)
    print(message.entities)
    bot.send_document(
        message.chat.id,
        file_text_doc,
        visible_file_name="your-info.txt",
        reply_to_message_id=message.id,
        caption=messages.me_caption
    )


@bot.message_handler(commands=["md"])
def send_markdown_formatting(message: types.Message):
    text = messages.markdown_formatting_style
    bot.send_message(
        message.chat.id,
        text,
        reply_to_message_id=message.id,
        parse_mode="MarkdownV2"
    )


@bot.message_handler(commands=["html"])
def send_html_formatting(message: types.Message):
    text = messages.html_formatting_style
    bot.send_message(
        message.chat.id,
        text,
        reply_to_message_id=message.id,
        parse_mode="HTML"
    )


@bot.message_handler(commands=["chat_id"])
def send_chat_id(message: types.Message):
    text = formatting.format_text(
        formatting.format_text(
            "id чата:",
            formatting.hcode(str(message.chat.id)),
            separator=" "
        ),
        formatting.format_text(
            "id отправителя:",
            formatting.hcode(str(message.from_user.id)),
            separator=" "
        ),
    )
    if message.reply_to_message:
        text = formatting.format_text(
            text,
            formatting.format_text(
                "Отвечено на сообщение от пользователя с id: ",
                formatting.hcode(str(message.reply_to_message.from_user.id)),
            )
        )

    bot.send_message(
        message.chat.id,
        text,
        reply_to_message_id=message.id,
        parse_mode="HTML"
    )


@bot.message_handler(commands=["rub_to_kzt"])
def convert_rub_to_kzt(message: types.Message):
    arguments = util.extract_arguments(message.text)

    # Ensure input is not blank
    if not arguments:
        bot.send_message(
            message.chat.id,
            messages.rub_to_kzt_how_to,
            parse_mode="HTML"
        )
        return

    # Ensure input is a number
    if not arguments.isdigit():
        text = formatting.format_text(
            formatting.format_text(
                messages.invalid_argument,
                arguments,
                separator=" "
            ),
            messages.rub_to_kzt_how_to
        )
        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML"
        )
        return

    rub_amount = int(arguments)
    kzt_amount = rub_amount * currencies.get_rub_to_kzt_ratio()

    bot.send_message(
        message.chat.id,
        messages.format_rub_to_kzt_answer(
            rub_amount=rub_amount,
            kzt_amount=kzt_amount
        ),
        parse_mode="HTML",
        reply_to_message_id=message.id,
    )


def has_no_command_arguments(message: types.Message):
    return not util.extract_arguments(message.text)


@bot.message_handler(commands=["cvt"], func=has_no_command_arguments)
def handle_cvt_has_no_arguments(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.cvt_how_to,
        parse_mode="HTML"
    )


@bot.message_handler(commands=["cvt"])
def convert_to_kzt(message: types.Message):
    arguments = util.extract_arguments(message.text)
    amount, _, currency = arguments.partition(" ")

    # Ensure amount is digits only
    if not amount.isdigit():
        text = formatting.format_text(
            formatting.format_text(
                messages.invalid_argument,
                arguments,
                separator=" "
            ),
            messages.cvt_how_to
        )
        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML"
        )
        return

    currency = currency.strip()

    ratio = currencies.get_currency_ratio(
        from_currency=currency,
        to_currency="kzt"
    )

    if ratio == currencies.ERROR_FETCHING_VALUE:
        bot.send_message(
            message.chat.id,
            messages.error_fetching_value_message,
        )
        return

    if ratio == currencies.ERROR_CURRENCY_FROM_NOT_FOUND:
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.error_currency_not_found_message.format(
                currency=formatting.hcode(currency)
            ),
            parse_mode="HTML",
        )
        return

    from_amount = int(amount)
    kzt_amount = from_amount * ratio

    bot.send_message(
        message.chat.id,
        messages.format_cvt_answer(
            from_amount=from_amount,
            kzt_amount=kzt_amount,
            from_currency=currency
        ),
        parse_mode="HTML"
    )


@bot.message_handler(commands=["cvt2"], func=has_no_command_arguments)
def handle_cvt_has_no_arguments(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.cvt2_how_to,
        parse_mode="HTML"
    )


def get_the_currencies_from_text(text: str):
    from_currency, _, to_currency = text.partition(" ")

    from_currency = from_currency.strip()
    to_currency = to_currency.strip()

    if not to_currency:
        to_currency = "KZT"

    return [from_currency, to_currency]


@bot.message_handler(commands=["cvt2"])
def convert_currencies(message: types.Message):
    arguments = util.extract_arguments(message.text)
    amount, _, text = arguments.partition(" ")
    from_currency, to_currency = get_the_currencies_from_text(text=text)

    # Ensure amount is digits only
    if not amount.isdigit():
        text = formatting.format_text(
            formatting.format_text(
                messages.invalid_argument,
                arguments,
                separator=" "
            ),
            messages.cvt2_how_to
        )
        bot.send_message(
            message.chat.id,
            text,
            parse_mode="HTML"
        )
        return

    ratio = currencies.get_currency_ratio(
        from_currency=from_currency,
        to_currency=to_currency
    )

    if ratio == currencies.ERROR_FETCHING_VALUE:
        bot.send_message(
            message.chat.id,
            messages.error_fetching_value_message,
        )
        return

    if ratio in [currencies.ERROR_CURRENCY_FROM_NOT_FOUND, currencies.ERROR_CURRENCY_TO_NOT_FOUND]:
        bad_currency = from_currency
        if ratio == currencies.ERROR_CURRENCY_TO_NOT_FOUND:
            bad_currency = to_currency
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.error_currency_not_found_message.format(
                currency=formatting.hcode(bad_currency)
            ),
            parse_mode="HTML",
        )
        return

    from_amount = int(amount)
    to_amount = from_amount * ratio

    bot.send_message(
        message.chat.id,
        messages.format_cvt2_answer(
            from_amount=from_amount,
            to_amount=to_amount,
            from_currency=from_currency,
            to_currency=to_currency
        ),
        parse_mode="HTML"
    )


@bot.message_handler(has_entities=True)
def echo_with_entities(message: types.Message):
    named_entities = {formatting.hcode(entity.type) for entity in message.entities}
    text = formatting.format_text(
        message.html_text,
        f"Entities: {', '.join(named_entities)}",
        separator='\n\n'
    )
    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML"
    )


@bot.message_handler(contains_at_least_one_of_words=["пока", "до свидания"])
def handle_goodbye(message: types.Message):
    text = messages.goodbye_message
    bot.send_message(
        message.chat.id,
        text,
        reply_to_message_id=message.id
    )


@bot.message_handler()
def echo_message(message: types.Message):
    text = message.text

    if 'привет' in text.lower():
        text = 'И тебе привет!'
    elif 'как дела' in text.lower():
        text = 'Хорошо! А у вас как?'

    bot.send_message(
        message.chat.id,
        text
    )


if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
