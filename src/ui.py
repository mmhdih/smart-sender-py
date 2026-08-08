import customtkinter as ctk
from src.backend import MessageSender

GOOGLE_BLUE = "#1a73e8"
GOOGLE_BLUE_HOVER = "#174ea6"

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class SmartSenderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Sender - Auto Background")
        self.geometry("500x650")
        self.resizable(False, False)
        
        self.backend = MessageSender(api_id="YOUR_API_ID", api_hash="YOUR_API_HASH")

        title_font = ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        main_font = ctk.CTkFont(family="Helvetica", size=14)
        bold_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")

        self.theme_switch = ctk.CTkSwitch(self, text="حالت تاریک", font=main_font, command=self.toggle_theme, progress_color=GOOGLE_BLUE)
        self.theme_switch.pack(anchor="e", padx=30, pady=(20, 0))

        self.lbl_title = ctk.CTkLabel(self, text="ارسال پیام گروهی", font=title_font, text_color=GOOGLE_BLUE)
        self.lbl_title.pack(anchor="e", padx=30, pady=(10, 20))

        self.lbl_numbers = ctk.CTkLabel(self, text=":لیست شماره‌ها (هر خط یک شماره)", font=bold_font)
        self.lbl_numbers.pack(anchor="e", padx=30)
        
        self.txt_numbers = ctk.CTkTextbox(self, height=120, corner_radius=8, border_width=1)
        self.txt_numbers.pack(fill="x", padx=30, pady=(5, 15))
        self.txt_numbers.configure(font=ctk.CTkFont(family="Helvetica", size=14))

        self.lbl_message = ctk.CTkLabel(self, text=":متن پیام", font=bold_font)
        self.lbl_message.pack(anchor="e", padx=30)
        self.txt_message = ctk.CTkTextbox(self, height=120, corner_radius=8, border_width=1)
        self.txt_message.pack(fill="x", padx=30, pady=(5, 15))

        self.lbl_platform = ctk.CTkLabel(self, text=":انتخاب پیام‌رسان", font=bold_font)
        self.lbl_platform.pack(anchor="e", padx=30)
        
        self.platform_var = ctk.StringVar(value="whatsapp")
        self.radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.radio_frame.pack(anchor="e", padx=30, pady=(5, 20))
        
        self.rb_tg = ctk.CTkRadioButton(self.radio_frame, text="تلگرام", variable=self.platform_var, value="telegram", font=main_font, fg_color=GOOGLE_BLUE)
        self.rb_tg.pack(side="right", padx=(10, 0))
        
        self.rb_wa = ctk.CTkRadioButton(self.radio_frame, text="واتس‌اپ (پس‌زمینه)", variable=self.platform_var, value="whatsapp", font=main_font, fg_color=GOOGLE_BLUE)
        self.rb_wa.pack(side="right", padx=(10, 10))

        self.btn_send = ctk.CTkButton(
            self, text="ارسال پیام‌ها", 
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"), 
            height=45, corner_radius=8, 
            fg_color=GOOGLE_BLUE, hover_color=GOOGLE_BLUE_HOVER,
            command=self.start_sending
        )
        self.btn_send.pack(fill="x", padx=30, pady=10)

        self.lbl_status = ctk.CTkLabel(self, text="", font=main_font)
        self.lbl_status.pack(pady=5)

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def start_sending(self):
        numbers_raw = self.txt_numbers.get("1.0", "end-1c").strip()
        message = self.txt_message.get("1.0", "end-1c").strip()

        if not numbers_raw or not message:
            self.show_status("لطفاً شماره‌ها و متن پیام را وارد کنید.", "red")
            return

        numbers = [n for n in numbers_raw.split("\n") if n.strip()]
        platform = self.platform_var.get()

        self.btn_send.configure(state="disabled", text="در حال پردازش...")
        self.show_status("در حال ارسال... ماوس و کیبورد شما آزاد است.", "#fbbc04")

        if platform == "whatsapp":
            self.backend.send_whatsapp(numbers, message, self.on_complete)
        else:
            self.backend.send_telegram(numbers, message, self.on_complete)

    def on_complete(self, success, msg):
        self.after(0, self.update_ui_post_send, success, msg)

    def update_ui_post_send(self, success, msg):
        color = "#34a853" if success else "#ea4335"
        self.show_status(msg, color)
        self.btn_send.configure(state="normal", text="ارسال پیام‌ها")
