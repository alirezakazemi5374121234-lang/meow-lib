from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class Message:
    """مدل پیام"""
    message_id: str
    chat_id: str
    sender_id: str
    text: Optional[str] = None
    reply_to_message: Optional['Message'] = None
    raw_data: Optional[Dict[str, Any]] = None
    new_chat_members: Optional[List[Dict]] = None
    
    def is_group(self) -> bool:
        """بررسی اینکه پیام در گروه ارسال شده"""
        return self.chat_id != self.sender_id


@dataclass
class CallbackQuery:
    """مدل دکمه شیشه‌ای"""
    id: str
    from_id: str
    chat_id: str
    data: str
    message: Optional[Message] = None


@dataclass
class Update:
    """مدل بروزرسانی"""
    update_id: int
    message: Optional[Message] = None
    callback_query: Optional[CallbackQuery] = None
