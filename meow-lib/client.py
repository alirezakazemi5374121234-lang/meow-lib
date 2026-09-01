import asyncio
import ssl
from typing import Dict, Any, Optional, Callable, List

import aiohttp

from .types import Message, Update, CallbackQuery
from .keyboard import InlineKeyboard


class MeowBot:
    """کلاس اصلی ربات میویی"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.rubika.ir/v1"
        self.handlers: List[Callable] = []
        self.callback_handlers: Dict[str, Callable] = {}
        self.offset = 0
        self.running = False
        self._bot_info = None
    
    # ---------- درخواست‌های پایه ----------
    
    async def _request(self, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """ارسال درخواست به API روبیکا"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # ایجاد SSL context برای اتصال امن
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        
        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    f"{self.base_url}/{method}",
                    json=data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    return await response.json()
        except aiohttp.ClientConnectorDNSError:
            print("❌ خطا: اتصال به سرور روبیکا ممکن نیست.")
            return {"ok": False, "error": "connection_error"}
        except Exception as e:
            print(f"❌ خطا در درخواست: {e}")
            return {"ok": False, "error": str(e)}
    
    async def get_me(self) -> Dict:
        """دریافت اطلاعات ربات"""
        if not self._bot_info:
            result = await self._request("getMe", {})
            if result.get("ok"):
                self._bot_info = result.get("result", {})
        return self._bot_info or {}
    
    # ---------- ارسال پیام ----------
    
    async def send_message(
        self,
        chat_id: str,
        text: str,
        reply_to_message_id: Optional[str] = None,
        inline_keyboard: Optional[InlineKeyboard] = None
    ) -> bool:
        """ارسال پیام با پشتیبانی از دکمه شیشه‌ای"""
        data = {"chat_id": chat_id, "text": text}
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
        if inline_keyboard:
            data["reply_markup"] = inline_keyboard.to_dict()
        result = await self._request("sendMessage", data)
        return result.get("ok", False)
    
    async def reply_message(
        self,
        message: Message,
        text: str,
        inline_keyboard: Optional[InlineKeyboard] = None
    ) -> bool:
        """پاسخ به پیام با پشتیبانی از دکمه شیشه‌ای"""
        return await self.send_message(
            message.chat_id,
            text,
            reply_to_message_id=message.message_id,
            inline_keyboard=inline_keyboard
        )
    
    async def edit_message_text(
        self,
        chat_id: str,
        message_id: str,
        text: str,
        inline_keyboard: Optional[InlineKeyboard] = None
    ) -> bool:
        """ویرایش پیام"""
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }
        if inline_keyboard:
            data["reply_markup"] = inline_keyboard.to_dict()
        result = await self._request("editMessageText", data)
        return result.get("ok", False)
    
    async def delete_message(self, chat_id: str, message_id: str) -> bool:
        """حذف پیام"""
        data = {"chat_id": chat_id, "message_id": message_id}
        result = await self._request("deleteMessage", data)
        return result.get("ok", False)
    
    # ---------- مدیریت گروه ----------
    
    async def get_chat_member(self, chat_id: str, user_id: str) -> Dict:
        """دریافت اطلاعات یک عضو گروه"""
        data = {"chat_id": chat_id, "user_id": user_id}
        result = await self._request("getChatMember", data)
        return result.get("result", {})
    
    async def kick_chat_member(self, chat_id: str, user_id: str) -> bool:
        """اخراج کاربر از گروه"""
        data = {"chat_id": chat_id, "user_id": user_id}
        result = await self._request("kickChatMember", data)
        return result.get("ok", False)
    
    async def unban_chat_member(self, chat_id: str, user_id: str) -> bool:
        """برداشتن بن کاربر"""
        data = {"chat_id": chat_id, "user_id": user_id}
        result = await self._request("unbanChatMember", data)
        return result.get("ok", False)
    
    async def restrict_chat_member(
        self,
        chat_id: str,
        user_id: str,
        can_send_messages: bool = True
    ) -> bool:
        """محدود کردن دسترسی کاربر (سکوت)"""
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "permissions": {"can_send_messages": can_send_messages}
        }
        result = await self._request("restrictChatMember", data)
        return result.get("ok", False)
    
    async def pin_chat_message(self, chat_id: str, message_id: str) -> bool:
        """پین کردن پیام"""
        data = {"chat_id": chat_id, "message_id": message_id}
        result = await self._request("pinChatMessage", data)
        return result.get("ok", False)
    
    async def unpin_chat_message(self, chat_id: str) -> bool:
        """برداشتن پین پیام"""
        data = {"chat_id": chat_id}
        result = await self._request("unpinChatMessage", data)
        return result.get("ok", False)
    
    # ---------- دکمه‌های شیشه‌ای ----------
    
    async def answer_callback_query(self, callback_query_id: str, text: str, show_alert: bool = False) -> bool:
        """پاسخ به دکمه شیشه‌ای"""
        data = {
            "callback_query_id": callback_query_id,
            "text": text,
            "show_alert": show_alert
        }
        result = await self._request("answerCallbackQuery", data)
        return result.get("ok", False)
    
    # ---------- هندلرها ----------
    
    def on_message(self, callback: Callable):
        """دکوراتور برای هندلر پیام‌ها"""
        self.handlers.append(callback)
        return callback
    
    def on_callback(self, data: str):
        """دکوراتور برای هندلر دکمه‌های شیشه‌ای"""
        def decorator(callback: Callable):
            self.callback_handlers[data] = callback
            return callback
        return decorator
    
    # ---------- پردازش بروزرسانی‌ها ----------
    
    async def _process_updates(self):
        """دریافت و پردازش بروزرسانی‌ها"""
        data = {"offset": self.offset, "limit": 10}
        result = await self._request("getUpdates", data)
        
        if not result.get("ok"):
            return
        
        for update_data in result.get("result", []):
            self.offset = update_data["update_id"] + 1
            update = self._parse_update(update_data)
            
            if update.message:
                for handler in self.handlers:
                    try:
                        await handler(self, update.message)
                    except Exception as e:
                        print(f"خطا در هندلر پیام: {e}")
            
            if update.callback_query:
                handler = self.callback_handlers.get(update.callback_query.data)
                if handler:
                    try:
                        await handler(self, update.callback_query)
                    except Exception as e:
                        print(f"خطا در هندلر دکمه: {e}")
    
    def _parse_update(self, data: Dict) -> Update:
        """تبدیل داده خام به مدل Update"""
        message_data = data.get("message")
        message = None
        
        if message_data:
            reply_to = None
            if message_data.get("reply_to_message"):
                reply_data = message_data["reply_to_message"]
                reply_to = Message(
                    message_id=reply_data["message_id"],
                    chat_id=reply_data["chat"]["id"],
                    sender_id=reply_data["from"]["id"],
                    text=reply_data.get("text"),
                    raw_data=reply_data
                )
            
            message = Message(
                message_id=message_data["message_id"],
                chat_id=message_data["chat"]["id"],
                sender_id=message_data["from"]["id"],
                text=message_data.get("text"),
                reply_to_message=reply_to,
                raw_data=message_data,
                new_chat_members=message_data.get("new_chat_members")
            )
        
        callback_data = data.get("callback_query")
        callback = None
        if callback_data:
            callback = CallbackQuery(
                id=callback_data["id"],
                from_id=callback_data["from"]["id"],
                chat_id=callback_data["message"]["chat"]["id"],
                data=callback_data["data"],
                message=Message(
                    message_id=callback_data["message"]["message_id"],
                    chat_id=callback_data["message"]["chat"]["id"],
                    sender_id=callback_data["from"]["id"],
                    text=callback_data["message"].get("text"),
                    raw_data=callback_data["message"]
                )
            )
        
        return Update(
            update_id=data["update_id"],
            message=message,
            callback_query=callback
        )
    
    # ---------- اجرا ----------
    
    async def run(self):
        """اجرای ربات"""
        self.running = True
        
        bot_info = await self.get_me()
        print(f"🐱 ربات {bot_info.get('username', 'میویی')} شروع به کار کرد!")
        
        while self.running:
            try:
                await self._process_updates()
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                self.running = False
                print("\n👋 ربات متوقف شد.")
            except Exception as e:
                print(f"❌ خطا: {e}")
                await asyncio.sleep(5)