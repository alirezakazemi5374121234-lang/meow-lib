from typing import Dict, List


class InlineButton:
    """یک دکمه شیشه‌ای"""
    def __init__(self, text: str, callback_data: str):
        self.text = text
        self.callback_data = callback_data
    
    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "callback_data": self.callback_data
        }


class InlineKeyboard:
    """صفحه‌کلید شیشه‌ای"""
    def __init__(self):
        self.rows = []
    
    def add_row(self, *buttons: InlineButton):
        """افزودن یک ردیف دکمه"""
        self.rows.append([btn.to_dict() for btn in buttons])
        return self
    
    def to_dict(self) -> Dict:
        return {"inline_keyboard": self.rows}