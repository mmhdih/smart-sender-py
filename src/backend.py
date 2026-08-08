import os
import time
import urllib.parse
import threading
from telethon.sync import TelegramClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class MessageSender:
    def __init__(self, api_id=None, api_hash=None):
        self.api_id = api_id 
        self.api_hash = api_hash

    def send_whatsapp(self, numbers, message, callback):
        def task():
            try:
                # تنظیمات کروم برای اجرای مستقل و ذخیره سشن (برای اینکه هر دفعه QR Code نخواهد)
                chrome_options = Options()
                profile_path = os.path.join(os.environ['LOCALAPPDATA'], 'SmartSender_WA_Profile')
                chrome_options.add_argument(f"user-data-dir={profile_path}")
                
                # نصب و راه‌اندازی درایور کروم به صورت خودکار
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)

                for num in numbers:
                    # پاک‌سازی شماره
                    clean_num = num.replace(" ", "").replace("-", "")
                    encoded_msg = urllib.parse.quote(message)
                    url = f"https://web.whatsapp.com/send?phone={clean_num}&text={encoded_msg}"
                    
                    driver.get(url)
                    
                    # صبر می‌کند تا دکمه ارسال در صفحه لود شود (حداکثر 60 ثانیه برای اسکن احتمالی QR Code در دفعه اول)
                    wait = WebDriverWait(driver, 60)
                    send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
                    
                    # کلیک روی دکمه بدون درگیر کردن ماوس فیزیکی کاربر
                    send_btn.click()
                    time.sleep(2) # یک مکث کوتاه برای اطمینان از ارسال شدن پیام قبل از رفتن به شماره بعدی

                time.sleep(2)
                driver.quit()
                callback(True, "پیام‌ها با موفقیت و بدون درگیری ماوس ارسال شدند.")
            except Exception as e:
                callback(False, f"خطا در واتس‌اپ: (احتمالاً کروم بسته شد یا اینترنت قطع است)")
        
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
                    clean_num = num.replace(" ", "").replace("-", "")
                    client.send_message(clean_num, message)
                    time.sleep(1)
                client.disconnect()
                callback(True, "پیام‌ها با موفقیت در تلگرام ارسال شدند.")
            except Exception as e:
                callback(False, f"خطا در تلگرام: {str(e)}")
                
        threading.Thread(target=task, daemon=True).start()
