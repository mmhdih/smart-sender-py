import time
import pywhatkit
from telethon.sync import TelegramClient
import threading

class MessageSender:
    def __init__(self, api_id=None, api_hash=None):
        # برای تلگرام نیاز به api_id و api_hash دارید که باید از my.telegram.org بگیرید
        self.api_id = api_id 
        self.api_hash = api_hash

    def send_whatsapp(self, numbers, message, callback):
        def task():
            try:
                for num in numbers:
                    # ارسال پیام در واتس‌اپ وب (نیازمند باز بودن مرورگر و لاگین)
                    pywhatkit.sendwhatmsg_instantly(num, message, wait_time=15, tab_close=True)
                    time.sleep(2)
                callback(True, "پیام‌ها با موفقیت در واتس‌اپ ارسال شدند.")
            except Exception as e:
                callback(False, f"خطا در واتس‌اپ: {str(e)}")
        
        threading.Thread(target=task, daemon=True).start()

    def send_telegram(self, numbers, message, callback):
        def task():
            try:
                if not self.api_id or not self.api_hash:
                    callback(False, "تنظیمات API تلگرام وارد نشده است.")
                    return
                
                client = TelegramClient('session_name', self.api_id, self.api_hash)
                client.start()
                for num in numbers:
                    client.send_message(num, message)
                    time.sleep(1) # جلوگیری از اسپم
                client.disconnect()
                callback(True, "پیام‌ها با موفقیت در تلگرام ارسال شدند.")
            except Exception as e:
                callback(False, f"خطا در تلگرام: {str(e)}")
                
        threading.Thread(target=task, daemon=True).start()