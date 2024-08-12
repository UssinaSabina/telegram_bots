from telebot import formatting

help_message = """
    Доступные команды:
    - <b>/start</b> (чтобы начать работу со мной)
    - <b>/help</b> (если понадобится помощь)
    - <b>/joke</b> (отправлю рандомную шутку)
    - <b>/rub_to_kzt 100</b> (конвертирую 100 RUB в KZT) 
    - <b>/cvt 100 JPY</b> (конвертирую 100 JPY в KZT) 
    """

start_message = """
        Привет! 
        Я первый бот <tg-spoiler>@UssinaSabina</tg-spoiler>. Не суди строго :)
    """

goodbye_message = "До новых встреч!"

me_caption = "Информация о пользователе"

markdown_formatting_style = """*bold \*text*
_italic \_text_
__underline__
~strikethrough~
||spoiler||
*bold _italic bold ~italic bold strikethrough ||italic bold strikethrough spoiler||~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=945368707)
![👍](tg://emoji?id=5368324170671202286)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
print("Hello world")
```
>Block quotation started
>Block quotation continued
>Block quotation continued
>Block quotation continued
>The last line of the block quotation
**>The expandable block quotation started right after the previous block quotation
>It is separated from the previous block quotation by an empty bold entity
>Expandable block quotation continued
>Hidden by default part of the expandable block quotation started
>Expandable block quotation continued
>The last line of the expandable block quotation with the expandability mark||
"""

html_formatting_style = """<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=945368707">inline mention of a user</a>
<tg-emoji emoji-id="5368324170671202286">👍</tg-emoji>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
<blockquote>Block quotation started\nBlock quotation continued\nThe last line of the block quotation</blockquote>
<blockquote expandable>Expandable block quotation started\nExpandable block quotation continued\nExpandable block quotation continued\nHidden by default part of the block quotation started\nExpandable block quotation continued\nThe last line of the block quotation</blockquote>
"""

rub_to_kzt_how_to = formatting.format_text(
    "Пожалуйста, укажите сумму для конвертации, как в примере ниже:",
    formatting.hcode("/rub_to_kzt 100"),
)

invalid_argument = "Вы ввели неверный аргумент:"

cvt_how_to = formatting.format_text(
    "Пожалуйста, укажите аргумент для конвертации, как в примере ниже (конвертация 100 JPY в KZT):",
    formatting.hcode("/cvt 100 JPY"),
)

error_fetching_value_message = "Что-то пошло не так при запросе, попробуйте позже."

error_currency_not_found_message = (
    "Неизвестная валюта: {currency}. Укажите существующую валюту."
)

cvt2_how_to = formatting.format_text(
    "Пожалуйста, укажите аргументы для конвертации.\n\nНапример, работа команд",
    formatting.hcode("/cvt2 100 JPY"),
    " и ",
    formatting.hcode("/cvt2 100 JPY KZT"),
    " приведет к одному результату (конвертирует 100 йен в тенге), а команда ",
    formatting.hcode("/cvt2 100 JPY IDR"),
    " превратит йены в рупии.",
    separator=""
)


def format_cvt2_answer(
        from_amount: int,
        to_amount: float,
        from_currency: str,
        to_currency: str
):
    text: object = formatting.format_text(
        formatting.hcode(f"{from_amount:,}"),
        f"{from_currency.upper()} это примерно",
        formatting.hcode(f"{to_amount:,.2f}"),
        f"{to_currency.upper()}",
        separator=" "
    )
    return text


def format_cvt_answer(
        from_amount: int,
        kzt_amount: float,
        from_currency: str
):
    return format_cvt2_answer(
        from_amount=from_amount,
        to_amount=kzt_amount,
        from_currency=from_currency,
        to_currency="KZT"
    )


def format_rub_to_kzt_answer(rub_amount: int, kzt_amount: float):
    return format_cvt_answer(
        from_amount=rub_amount,
        kzt_amount=kzt_amount,
        from_currency="rub"
    )