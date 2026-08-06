import customtkinter as ctk
from src.backend import MessageSender
import threading

# تنظیمات ظاهری شبیه به iOS
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SmartSenderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Sender")
        self.geometry("450x650")
        self.resizable(False, False)
        
        # بک‌اند (برای تست تلگرام باید مقادیر واقعی api_id و api_hash را وارد کنید)
        self.backend = MessageSender(api_id="YOUR_API_ID", api_hash="YOUR_API_HASH")

        # فونت‌ها
        title_font = ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        main_font = ctk.CTkFont(family="Helvetica", size=14)

        # عنوان
        self.lbl_title = ctk.CTkLabel(self, text="ارسال پیام گروهی", font=title_font)
        self.lbl_title.pack(pady=(30, 20))

        # باکس دریافت شماره‌ها
        self.lbl_numbers = ctk.CTkLabel(self, text="لیست شماره‌ها (هر خط یک شماره همراه با کد کشور):", font=main_font)
        self.lbl_numbers.pack(anchor="w", padx=30)
        self.txt_numbers = ctk.CTkTextbox(self, height=120, corner_radius=10)
        self.txt_numbers.pack(fill="x", padx=30, pady=(5, 15))

        # باکس دریافت متن پیام
        self.lbl_message = ctk.CTkLabel(self, text="متن پیام:", font=main_font)
        self.lbl_message.pack(anchor="w", padx=30)
        self.txt_message = ctk.CTkTextbox(self, height=120, corner_radius=10)
        self.txt_message.pack(fill="x", padx=30, pady=(5, 15))

        # انتخاب پلتفرم (رادیو باتن)
        self.platform_var = ctk.StringVar(value="whatsapp")
        self.radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.radio_frame.pack(fill="x", padx=30, pady=10)
        
        self.rb_wa = ctk.CTkRadioButton(self.radio_frame, text="واتس‌اپ", variable=self.platform_var, value="whatsapp", font=main_font)
        self.rb_wa.pack(side="left", padx=10)
        
        self.rb_tg = ctk.CTkRadioButton(self.radio_frame, text="تلگرام", variable=self.platform_var, value="telegram", font=main_font)
        self.rb_tg.pack(side="left", padx=10)

        # دکمه ارسال با طراحی گرد
        self.btn_send = ctk.CTkButton(self, text="ارسال پیام‌ها", font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"), 
                                      height=45, corner_radius=20, command=self.start_sending)
        self.btn_send.pack(fill="x", padx=30, pady=20)

        # لیبل وضعیت
        self.lbl_status = ctk.CTkLabel(self, text="", font=main_font, text_color="gray")
        self.lbl_status.pack(pady=10)

    def start_sending(self):
        numbers_raw = self.txt_numbers.get("1.0", "end-1c").strip()
        message = self.txt_message.get("1.0", "end-1c").strip()

        if not numbers_raw or not message:
            self.show_status("لطفاً شماره‌ها و متن پیام را وارد کنید.", "red")
            return

        # پاک‌سازی شماره‌ها
        numbers = [n.strip() for n in numbers_raw.split("\n") if n.strip()]
        platform = self.platform_var.get()

        self.btn_send.configure(state="disabled", text="در حال ارسال...")
        self.show_status("عملیات آغاز شد، لطفاً صبر کنید...", "yellow")

        if platform == "whatsapp":
            self.backend.send_whatsapp(numbers, message, self.on_complete)
        else:
            self.backend.send_telegram(numbers, message, self.on_complete)

    def on_complete(self, success, msg):
        # اجرای تغییرات UI در Thread اصلی
        self.after(0, self.update_ui_post_send, success, msg)

    def update_ui_post_send(self, success, msg):
        color = "green" if success else "red"
        self.show_status(msg, color)
        self.btn_send.configure(state="normal", text="ارسال پیام‌ها")

    def show_status(self, text, color):
        self.lbl_status.configure(text=text, text_color=color)