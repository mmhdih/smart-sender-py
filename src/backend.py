import time
import urllib.parse
import os
import pyautogui
from telethon.sync import TelegramClient
import threading

class MessageSender:
    def __init__(self, api_id=None, api_hash=None):
        self.api_id = api_id 
        self.api_hash = api_hash

    def send_whatsapp(self, numbers, message, wa_platform, callback):
        def task():
            try:
                for num in numbers:
                    # قابلیت ۴: حذف اتوماتیک فاصله‌ها از شماره
                    clean_num = num.replace(" ", "").replace("-", "")
                    encoded_msg = urllib.parse.quote(message)
                    
                    # قابلیت ۱: انتخاب پلتفرم ارسال
                    if wa_platform == "app":
                        # باز کردن اپلیکیشن نیتیو ویندوز
                        os.startfile(f"whatsapp://send?phone={clean_num}&text={encoded_msg}")
                    elif wa_platform == "chrome":
                        # باز کردن در گوگل کروم
                        os.system(f'start chrome "https://web.whatsapp.com/send?phone={clean_num}&text={encoded_msg}"')
                    elif wa_platform == "firefox":
                        # باز کردن در موزیلا فایرفاکس
                        os.system(f'start firefox "https://web.whatsapp.com/send?phone={clean_num}&text={encoded_msg}"')
                    
                    # صبر برای لود شدن واتس‌اپ (بسته به سرعت سیستم ممکن است نیاز به تغییر داشته باشد)
                    time.sleep(12) 
                    pyautogui.press('enter') # فشردن خودکار دکمه اینتر برای ارسال
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
                    # حذف اتوماتیک فاصله‌ها
                    clean_num = num.replace(" ", "").replace("-", "")
                    client.send_message(clean_num, message)
                    time.sleep(1)
                client.disconnect()
                callback(True, "پیام‌ها با موفقیت در تلگرام ارسال شدند.")
            except Exception as e:
                callback(False, f"خطا در تلگرام: {str(e)}")
                
        threading.Thread(target=task, daemon=True).start()
