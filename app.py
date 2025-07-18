import gradio as gr
from groq import Groq
from textblob import TextBlob
import os

#  Correct way to get environment variable
groq_api_key = os.environ.get("groq_api_key")

#  Initialize Groq client
client = Groq(api_key=groq_api_key)

#  Function to generate a response from Groq
def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Replace with actual available Groq model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

#  Analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", polarity
    elif 0.1 < polarity <= 0.5:
        return "Positive", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", polarity
    elif -0.5 < polarity < -0.1:
        return "Negative", polarity
    else:
        return "Very Negative", polarity

#  Provide coping strategy
def provide_coping_strategy(sentiment):
    strategies = {
        "Very Positive": "Keep up the positive vibes! Consider sharing your good mood with others.",
        "Positive": "It's great to see you're feeling positive. Keep doing what you're doing!",
        "Neutral": "Feeling neutral is okay. Consider engaging in activities you enjoy.",
        "Negative": "It seems you're feeling down. Try to take a break and do something relaxing.",
        "Very Negative": "I'm sorry to hear that you're feeling very negative. Consider talking to a friend or seeking professional help."
    }
    return strategies.get(sentiment, "Keep going, you're doing great!")

#  Main chatbot function
def chatbot(user_message, history=None):
    if history is None:
        history = []

    sentiment, polarity = analyze_sentiment(user_message)
    bot_response = generate_response(user_message)
    coping_strategy = provide_coping_strategy(sentiment)

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": bot_response})

    output = (
        f"Sentiment: {sentiment} (Polarity: {polarity})\n"
        f"Suggested Coping Strategy: {coping_strategy}"
    )

    return history, output, ""  # Clear input

#  Gradio UI
with gr.Blocks(theme='Respair/Shiki@1.2.1') as demo:
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
    user_input = gr.Textbox(label="You:", placeholder="Type your message here...")
    output_text = gr.Textbox(label="Analysis and Coping Strategy")
    submit_button = gr.Button("Send")

    gr.HTML("""
    <h2 style='color: #FF5733;'>Data Privacy Disclaimer</h2>
    <span style='color: #FF5733;'>
    This application stores your session data temporarily. Please avoid sharing personal information.
    </span>
    """)

    gr.Markdown("""
    ### 🛟 Resources
    - National Suicide Prevention Lifeline: 1-800-273-8255  
    - Crisis Text Line: Text 'HELLO' to 741741  
    - [More Resources](https://www.mentalhealth.gov/get-help/immediate-help)
    """)

    submit_button.click(chatbot, [user_input, chat_history], [chat_display, output_text, user_input])
    user_input.submit(chatbot, [user_input, chat_history], [chat_display, output_text, user_input])

# Launch app
demo.launch(server_name="0.0.0.0", server_port=10000)
