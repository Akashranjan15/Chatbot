
# 🧠 Mental Health Support Chatbot

This is an AI-powered mental health support chatbot built with **Gradio**, **Groq (LLaMA3)**, **TextBlob** (for sentiment analysis), and **NLTK** for NLP tasks. It streams responses line-by-line, analyzes user sentiment, and offers appropriate coping strategies.

## 🌐 Live Demo (if hosted)
You can deploy it on Render, Replit, or other platforms. Example (Gradio Live): `https://your-custom-url.gradio.live`

---

## 🚀 Features
- ✅ **Line-by-line streaming responses** (more human-like)
- 😊 **Sentiment analysis** using TextBlob
- 🧘‍♀️ **Coping strategy suggestions** based on mood
- 🎵 **Calming music** built into the UI
- 📜 **Chat logging** + error logging
- 🔐 **API key loading via environment variable**
- 🌐 Ready to deploy on Render, Replit, etc.

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Akashranjan15/Chatbot.git
cd Chatbot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Groq API Key
Create a `.env` file or set it in the shell:
```bash
export groq_api_key=your_groq_api_key_here
```

### 4. Run the App
```bash
python app.py
```

---

## 📝 .env Example
```
groq_api_key=your_real_key_here
```

---

## 📦 Requirements

See `requirements.txt` or install manually:

```txt
gradio==4.27.0
textblob==0.18.0
nltk==3.8.1
groq
```

---

## 📁 Files Included

- `app.py` – Main chatbot app
- `requirements.txt` – Python dependencies
- `chat_log.txt` – Stores past chats (created at runtime)
- `error_log.txt` – Error tracking
- `README.md` – This file

---

## 🛡️ Disclaimer
This is **not a replacement for professional help**. For emergencies, contact a mental health professional or use the provided emergency numbers.

---

## 🙌 Acknowledgements
- [Gradio](https://www.gradio.app)
- [Groq](https://console.groq.com)
- [TextBlob](https://textblob.readthedocs.io/)
- [NLTK](https://www.nltk.org/)
