from typing import Iterable

from telebot import types
from telebot import SimpleCustomFilter, AdvancedCustomFilter


class HasEntitiesFilter(SimpleCustomFilter):
    key = "has_entities"

    def check(self, message: types.Message):
        return bool(message.entities)


class ContainsAtLeastOneOfWordsFilter(AdvancedCustomFilter):
    key = "contains_at_least_one_of_words"

    def check(self, message: types.Message, words: Iterable[str]) -> bool:
        text = message.text or message.caption
        if not text:
            return False

        text_lower = text.lower()
        return any(word.lower() in text_lower for word in words)


