"""
MeowLib - کتابخانه اختصاصی ربات میویی برای روبیکا
"""

from .client import MeowBot
from .types import Message, CallbackQuery, Update
from .keyboard import InlineButton, InlineKeyboard
from .utils import (
    load_json,
    save_json,
    format_time,
    get_user_level,
    is_meow_word,
    is_bad_word
)

__version__ = "1.0.0"
__author__ = "Meow Team"

__all__ = [
    "MeowBot",
    "Message",
    "CallbackQuery",
    "Update",
    "InlineButton",
    "InlineKeyboard",
    "load_json",
    "save_json",
    "format_time",
    "get_user_level",
    "is_meow_word",
    "is_bad_word"
]