import pytesseract
import mss
import numpy as np
import cv2
import tkinter as tk
import customtkinter as ctk
from deep_translator import GoogleTranslator, single_detection
import keyboard
import ctypes
from tkinter import messagebox
import re
import time

# ---------- إعداد اللغات ----------
languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es"
}

# ---------- نافذة التطبيق الرئيسية ----------

class RegionSelectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("⚡ Auto Translator")
        self.geometry("440x280")
        self.resizable(False, False)
        self.configure(bg="black")
        self.iconbitmap("data\\icon.ico")

        frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=15)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # --- اختيار اللغات ---
        lang_frame = ctk.CTkFrame(frame, fg_color="#1e1e1e", corner_radius=10)
        lang_frame.pack(pady=(10, 0))

        # لغة المصدر
        ctk.CTkLabel(lang_frame, text="Source:", text_color="#cccccc").grid(row=0, column=0, padx=(0, 4))
        self.src_lang_var = ctk.StringVar(value="Auto Detect")
        ctk.CTkOptionMenu(
            lang_frame, values=list(languages.keys()), variable=self.src_lang_var, width=140,
            fg_color="#333333", button_color="#444444", text_color="white"
        ).grid(row=0, column=1, pady=6)

        # لغة الهدف
        ctk.CTkLabel(lang_frame, text="Target:", text_color="#cccccc").grid(row=0, column=2, padx=(12, 4))
        self.tgt_lang_var = ctk.StringVar(value="Arabic")
        ctk.CTkOptionMenu(
            lang_frame, values=list(languages.keys()), variable=self.tgt_lang_var, width=140,
            fg_color="#333333", button_color="#444444", text_color="white"
        ).grid(row=0, column=3, pady=6)

        # رسالة الحالة
        self.log_label = ctk.CTkLabel(
            frame, text="Hotkey not ready", text_color="white",
            font=ctk.CTkFont("Arial", 16, "bold"), anchor="center"
        )
        self.log_label.pack(pady=(30, 12), padx=10)

        # زر الخروج
        ctk.CTkButton(
            frame, text="Exit", command=self.ext, fg_color="#d9534f", hover_color="#c9302c",
            text_color="white", font=ctk.CTkFont("Arial", 13, "bold"),
            corner_radius=10, height=36, width=120
        ).pack(pady=(10, 10))

        # تفعيل الاختصار لأول مرة
        self.after(300, self.bind_hotkey)

    # ---------- أدوات مساعدة ----------
    def log(self, message: str):
        self.log_label.configure(text=message)

    def bind_hotkey(self):
        keyboard.add_hotkey('shift+q', self.select_and_translate)
        self.log("Press Shift + Q to select region")

    def ext(self):
        keyboard.unhook_all()
        messagebox.askquestion("info", "Don't forget donations 😊 – Youssef Ibrahim", icon='warning')
        self.destroy()

    # ---------- بدء اختيار المنطقة ثم الترجمة ----------
    def select_and_translate(self):
        self.log("🖱️ Select a region...")

        selector = RegionSelector(self)
        self.wait_window(selector)

        if selector.region and selector.region["width"] > 10 and selector.region["height"] > 10:
            self.log("🌐 Translating selection...")

            # الرموز المختارة من القوائم
            src_code = languages[self.src_lang_var.get()]
            tgt_code = languages[self.tgt_lang_var.get()]

            highlighter = RegionHighlighter(selector.region)
            TranslationWindow(
                selector.region, src_lang=src_code, tgt_lang=tgt_code,
                highlighter=highlighter
            )
        else:
            self.log("⚠️ Region too small. Try again.")

# ---------- الحصول على أبعاد الشاشة الحقيقية ----------
def get_actual_screen_size():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# ---------- نافذة اختيار المنطقة ----------
class RegionSelector(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.region = None
        self.start_x = self.start_y = None
        self.rect = None

        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.attributes("-alpha", 0.3)

        screen_width, screen_height = get_actual_screen_size()
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        self.canvas = tk.Canvas(self, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.update_idletasks()
        self.focus_force()
        self.grab_set()

    def on_button_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_move_press(self, event):
        cur_x = event.x_root
        cur_y = event.y_root
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x = event.x_root
        end_y = event.y_root
        self.region = {
            "left": int(min(self.start_x, end_x)),
            "top": int(min(self.start_y, end_y)),
            "width": int(abs(end_x - self.start_x)),
            "height": int(abs(end_y - self.start_y))
        }
        self.grab_release()
        self.destroy()

# ---------- تظليل المنطقة المختارة ----------
class RegionHighlighter(tk.Toplevel):
    def __init__(self, region):
        super().__init__()
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-transparentcolor', 'black')
        self.configure(bg='black')
        self.geometry(f"{region['width']}x{region['height']}+{region['left']}+{region['top']}")
        canvas = tk.Canvas(
            self, width=region['width'], height=region['height'],
            bg='black', highlightthickness=0
        )
        canvas.pack()
        canvas.create_rectangle(0, 0, region['width'], region['height'], outline='white', width=3)

# ---------- نافذة الترجمة ----------
class TranslationWindow(tk.Toplevel):
    def __init__(self, region, src_lang: str, tgt_lang: str, highlighter=None):
        super().__init__()
        self.highlighter = highlighter
        self.geometry(f"800x120+{region['left']}+{region['top'] + region['height'] + 10}")
        self.configure(bg='black')
        self.attributes("-topmost", True)

        self.region = region
        self.src_lang = src_lang        # رمز اللغة المختارة أو 'auto'
        self.tgt_lang = tgt_lang
        self.last_extracted = ""
        self.last_update_time = time.time()

        self.label = tk.Label(
            self, text="", fg="white", bg="black",
            font=("Arial", 18), wraplength=780, justify='center'
        )
        self.label.pack(padx=10, pady=10)

        self.after(100, self.update_translation)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- تنسيق النصوص ----------
    def clean_text(self, text):
        # أحرف عربية + إنجليزية + أرقام + شرطات سفلية
        text = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)
        words = [w for w in text.split() if len(w) > 1]
        return ' '.join(words)

    def is_valid_text(self, text):
        return len(text.split()) >= 2

    # ---------- كشف اللغة ----------
    def detect_language(self, text):
        try:
            return single_detection(text, api='google')
        except Exception:
            return "auto"

    # ---------- الترجمة ----------
    def translate_text(self, text):
        try:
            if self.src_lang == "auto":
                # نكشف اللغة مرة واحدة فقط ثم نخزنها
                if not hasattr(self, 'detected_lang'):
                    self.detected_lang = self.detect_language(text)
                src = self.detected_lang
            else:
                src = self.src_lang

            return GoogleTranslator(source=src, target=self.tgt_lang).translate(text)
        except Exception:
            return ""

    # ---------- التقاط الشاشة ومعالجة الـ OCR ----------
    def update_translation(self):
        with mss.mss() as sct:
            img = np.array(sct.grab(self.region))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)          # تقليل الضوضاء
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,         # تحويل ثنائي مرن
            cv2.THRESH_BINARY, 11, 2
        )

        custom_config = r'--oem 3 --psm 3'
        extracted = pytesseract.image_to_string(
            thresh, lang='eng+ara+fra', config=custom_config
        ).strip()
        cleaned = self.clean_text(extracted)

        if self.is_valid_text(cleaned):
            if cleaned != self.last_extracted:
                translated = self.translate_text(cleaned)
                if translated:
                    self.label.config(text=translated)
                    self.last_extracted = cleaned
                    self.last_update_time = time.time()
        else:
            # لا نص صالح
            if time.time() - self.last_update_time > 3:
                self.label.config(text="⚠️ No clear text detected")

        self.after(500, self.update_translation)

    # ---------- إغلاق النافذة ----------
    def on_close(self):
        if self.highlighter:
            self.highlighter.destroy()
        self.destroy()

# ---------- تشغيل التطبيق ----------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = RegionSelectorApp()
    app.mainloop()