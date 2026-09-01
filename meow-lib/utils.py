import json
import os
from typing import Dict, Any


def load_json(file_path: str, default: Dict = None) -> Dict:
    """بارگذاری فایل JSON"""
    if default is None:
        default = {}
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def save_json(file_path: str, data: Dict):
    """ذخیره فایل JSON"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def format_time(seconds: int) -> str:
    """تبدیل ثانیه به فرمت خوانا"""
    if seconds < 60:
        return f"{int(seconds)} ثانیه"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def get_user_level(meows: int) -> Dict:
    """محاسبه سطح کاربر بر اساس تعداد میوها"""
    if meows >= 50:
        return {"level": 5, "name": "سطح 5", "emoji": "😻", "min_reward": 25, "max_reward": 40}
    elif meows >= 30:
        return {"level": 4, "name": "سطح 4", "emoji": "😺", "min_reward": 20, "max_reward": 35}
    elif meows >= 15:
        return {"level": 3, "name": "سطح 3", "emoji": "🐱", "min_reward": 15, "max_reward": 25}
    elif meows >= 5:
        return {"level": 2, "name": "سطح 2", "emoji": "🐣", "min_reward": 10, "max_reward": 20}
    else:
        return {"level": 1, "name": "سطح 1", "emoji": "🥚", "min_reward": 5, "max_reward": 15}


def is_meow_word(text: str) -> bool:
    """بررسی اینکه متن یکی از کلمات میو است"""
    if not text:
        return False
    text = text.strip().lower()
    meow_words = ["میو", "میو میو", "/meow", "مع", "معو", "میویی"]
    return text in meow_words


def is_bad_word(text: str) -> bool:
    """بررسی وجود کلمات نامناسب در متن"""
    if not text:
        return False
    bad_words = ["کیر", "کص", "کس", "کون", "جنده", "کسکش", "کصکش", "کونی", "گاییدم", "خارکصه"]
    text = text.lower()
    for word in bad_words:
        if word in text:
            return True
    return False