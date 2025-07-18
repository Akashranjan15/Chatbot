import gradio as gr
from groq import Groq
from textblob import TextBlob
import os
import nltk
import time
from datetime import datetime

# 📦 Download required NLTK models
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# 🔐 Load Groq API key from environment
groq_api_key = os.environ.get("groq_api_key")
if not groq_api_key:
    raise ValueError("❌ Groq API key not found in environment variables.")
client = Groq(api_key=groq_api_key)

# 🔁 Stream line-by-line response
def generate_response_stream(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        buffer = ""
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                buffer += content
                if "\n" in buffer:
                    lines = buffer.split("\n")
                    for line in lines[:-1]:
                        yield line + "\n"
                    buffer = lines[-1]
        if buffer:
            yield buffer
    except Exception as e:
        with open("error_log.txt", "a") as f:
            f.write(f"[{datetime.now()}] {str(e)}\n")
        yield f"❌ Error: {str(e)}"

# 😊 Sentiment Analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive 😊", polarity
    elif 0.1 < polarity <= 0.5:
        return "Positive 🙂", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral 😐", polarity
    elif -0.5 < polarity < -0.1:
        return "Negative 😟", polarity
    else:
        return "Very Negative 😢", polarity

# 💡 Coping Strategy Based on Sentiment
def provide_coping_strategy(sentiment):
    strategies = {
        "Very Positive 😊": "Keep up the positive vibes! Consider sharing your good mood with others.",
        "Positive 🙂": "It's great to see you're feeling positive. Keep doing what you're doing!",
        "Neutral 😐": "Feeling neutral is okay. Consider engaging in activities you enjoy.",
        "Negative 😟": "It seems you're feeling down. Try to take a break and do something relaxing.",
        "Very Negative 😢": "I'm sorry to hear that you're feeling very negative. Consider talking to a friend or seeking professional help."
    }
    return strategies.get(sentiment, "You're doing great, keep going!")

# 🤖 Main Chatbot Function
def chatbot(user_message, history=None):
    if history is None:
        history = []

    if not user_message.strip():
        return [history + [{"role": "assistant", "content": "⚠️ Please enter a message."}]], "", ""
    if len(user_message) > 1000:
        return [history + [{"role": "assistant", "content": "⚠️ Message too long. Please shorten your input."}]], "", user_message

    sentiment, polarity = analyze_sentiment(user_message)
    coping_strategy = provide_coping_strategy(sentiment)
    history.append({"role": "user", "content": user_message})

    def response_generator():
        yield history + [{"role": "assistant", "content": "💬 Typing..."}], "", ""
        bot_reply = ""
        for chunk in generate_response_stream(user_message):
            bot_reply += chunk
            time.sleep(0.05)  # Simulate natural typing
            yield history + [{"role": "assistant", "content": bot_reply}], (
                f"**Sentiment**: {sentiment} (Polarity: {polarity:.2f})\n"
                f"**Coping Tip**: {coping_strategy}"
            ), ""

        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}]\nUser: {user_message}\nSentiment: {sentiment}, Polarity: {polarity:.2f}\nBot: {bot_reply}\n---\n")

    return response_generator()

# 🎨 UI
with gr.Blocks(theme="Respair/Shiki@1.2.1") as demo:
    gr.Markdown("# 🧠 Mental Health Support Chatbot")

    gr.Markdown("## 🎵 Listen to a Calming Song")
    gr.Audio(
        value="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        label="Calming Background Music",
        autoplay=False,
        loop=True
    )

    chat_history = gr.State([])
    chat_display = gr.Chatbot(label="Chat History", type="messages")
    user_input = gr.Textbox(label="You:", placeholder="Type your message here...", lines=2)
    output_text = gr.Textbox(label="Sentiment & Coping Tip", lines=2)
    submit_button = gr.Button("💬 Send")

    gr.HTML("""
    <h2 style='color: #FF5733;'>🛡️ Data Privacy Disclaimer</h2>
    <p>This application temporarily stores session data. Please avoid entering personal or sensitive information.</p>
    """)

    gr.Markdown("""
    ### 🛟 Emergency Resources
    - 📞 National Suicide Prevention Lifeline: **1-800-273-8255**  
    - 📱 Crisis Text Line: Text '**HELLO**' to **741741**  
    - 🌐 [More Mental Health Resources](https://www.mentalhealth.gov/get-help/immediate-help)
    """)

    submit_button.click(
        fn=chatbot,
        inputs=[user_input, chat_history],
        outputs=[chat_display, output_text, user_input],
        api_name="chatbot",
        stream=True
    )
    user_input.submit(
        fn=chatbot,
        inputs=[user_input, chat_history],
        outputs=[chat_display, output_text, user_input],
        api_name="chatbot",
        stream=True
    )

# 🚀 Launch App (for Render, Replit, etc.)
demo.launch(server_name="0.0.0.0", server_port=10000)
