from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_mailing_type():
    kb = ReplyKeyboardBuilder()
    kb.button(text="За некоторое время")
    kb.button(text="В конкретное время")
    kb.button(text="Я не хочу получать")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)