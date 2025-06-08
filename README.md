# ⚡ AutoTranslator - Real-Time Screen Text Translator 🔍🌍

**AutoTranslator** is a smart Python application that uses OCR (Optical Character Recognition) and AI-powered translation to capture and translate any on-screen text **instantly**.

Whether you're watching a foreign-language video, playing games, or attending an online lecture, AutoTranslator makes understanding content easier — live and in real-time.

---

## 📸 Demo
## Logo App

<p align="center">
  <img src="https://github.com/user-attachments/assets/b8df65f1-6d81-4fa2-abe0-94559428f98f" alt="icon" width="100"/>
</p>

> 🔽 Add your screenshots or demo GIFs in the `screenshots/` folder and link them below:

---

<p align="center">
  <img src="https://github.com/user-attachments/assets/c87b010d-994b-41de-8571-5e0e004e4540" alt="Screen 1" width="600" style="margin: 10px;"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/4ffafa96-b50a-4b25-9c75-2efdd5b65599" alt="Screen 2" width="300" style="margin: 10px;"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/4e441235-c3c0-4b0d-8880-f8a118904995" alt="Screen 3" width="600" style="margin: 10px;"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/4378c49e-7a64-4ab1-95c7-546343ef0d3e" alt="Screen 4" width="300" style="margin: 10px;"/>
</p>

## 🚀 Features

- ✅ Real-time translation of selected screen areas  
- ✅ Automatic language detection and translation  
- ✅ Clean GUI using Tkinter  
- ✅ Smart OCR filtering to remove noise and symbols  
- ✅ Hotkey (Shift + Q) to instantly select and translate  
- ✅ Lightweight and fast performance  
- ✅ Supports all languages via Google Translate API

---

## 🔍 How It Works

1. User presses `Shift + Q` to select a region on the screen  
2. The app takes a screenshot of the selected region  
3. Text is extracted using **Tesseract OCR**  
4. Text is translated using **Google Translate** via `deep_translator`  
5. The translated text appears in a clean GUI window

---

## 🧰 Tech Stack

- Python 3.8+
- Tesseract OCR (`pytesseract`)
- `deep_translator` (Google Translate)
- `mss` (for screenshot capturing)
- `OpenCV` (for image preprocessing)
- `Tkinter` (for GUI)
- `keyboard` (for global hotkey)

---

## 📦 Installation

1. Clone the repo:
```bash
git clone https://github.com/YOUR_USERNAME/AutoTranslator.git
cd AutoTranslator
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Run the app:

python main.py

🎯 Use Cases

    Translate text from YouTube videos or movies

    Understand content in foreign games or software

    Help language learners and researchers

    Real-time learning from non-English courses

    Assist users with dyslexia or vision difficulties
requirements.txt

```
pytesseract==0.3.10
deep-translator==1.11.4
opencv-python==4.9.0.80
mss==9.0.1
Pillow==10.3.0
numpy==1.26.4
keyboard==0.13.5
customtkinter==5.2.1
```

🖼️ Project Structure
```
AutoTranslator/
│
├── main.py                  # Main launcher & GUI for translated text
├── requirements.txt         # Dependencies
└── screenshots/             # Demo images and GIFs
```

Video on YouTube Channel

``` https://paste here ..... ```
