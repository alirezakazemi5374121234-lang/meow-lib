"""
تست‌های اولیه کتابخانه meow-lib
"""

import asyncio
from meow_lib import MeowBot, Message, InlineKeyboard, load_json, save_json


def test_import():
    """تست اینکه همه چیز درست import میشه"""
    try:
        from meow_lib import (
            MeowBot, Message, CallbackQuery, Update,
            InlineButton, InlineKeyboard,
            load_json, save_json, format_time,
            get_user_level, is_meow_word, is_bad_word
        )
        print("✅ همه import‌ها موفقیت‌آمیز بود!")
        return True
    except Exception as e:
        print(f"❌ خطا در import: {e}")
        return False


def test_json():
    """تست ذخیره و بارگذاری JSON"""
    try:
        test_data = {"test": "hello", "number": 123}
        save_json("test.json", test_data)
        loaded = load_json("test.json")
        if loaded == test_data:
            print("✅ JSON درست کار میکنه!")
            return True
        else:
            print("❌ JSON مشکل داره!")
            return False
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False


def test_level():
    """تست سیستم سطح‌بندی"""
    try:
        level = get_user_level(20)
        if level["level"] == 3 and level["name"] == "سطح 3":
            print("✅ سطح‌بندی درست کار میکنه!")
            return True
        else:
            print("❌ سطح‌بندی مشکل داره!")
            return False
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False


def test_keyboard():
    """تست دکمه‌های شیشه‌ای"""
    try:
        from meow_lib import InlineButton, InlineKeyboard
        kb = InlineKeyboard()
        kb.add_row(
            InlineButton("دکمه ۱", "btn1"),
            InlineButton("دکمه ۲", "btn2")
        )
        result = kb.to_dict()
        if "inline_keyboard" in result:
            print("✅ دکمه‌های شیشه‌ای درست کار میکنن!")
            return True
        else:
            print("❌ دکمه‌های شیشه‌ای مشکل دارن!")
            return False
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False


def run_all_tests():
    """اجرای همه تست‌ها"""
    print("🧪 شروع تست‌های کتابخانه meow-lib...")
    print("-" * 40)
    
    results = []
    results.append(test_import())
    results.append(test_json())
    results.append(test_level())
    results.append(test_keyboard())
    
    print("-" * 40)
    passed = sum(results)
    total = len(results)
    print(f"✅ {passed}/{total} تست قبول شد!")
    
    if passed == total:
        print("🎉 همه تست‌ها قبول شدن! کتابخانه آماده‌ست!")
    else:
        print("⚠️ بعضی تست‌ها قبول نشدن!")


if __name__ == "__main__":
    run_all_tests()
