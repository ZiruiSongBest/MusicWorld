import gradio as gr
import whisper
from transformers import pipeline

model = whisper.load_model("base")

sentiment_analysis = pipeline(
  "sentiment-analysis",
  framework="pt",
  model="SamLowe/roberta-base-go_emotions",
  device="cuda"
)

def analyze_sentiment(text):
    results = sentiment_analysis(text)
    sentiment_results = {result['label']: result['score'] for result in results}
    return sentiment_results

def get_sentiment_emoji(sentiment):
    emoji_mapping = {
        "disappointment": "😞",
        "sadness": "😢",
        "joy": "😄",
        "anger": "😡",
        "love": "❤️",
        "optimism": "😊",
        "neutral": "😐",
        "approval": "👍",
        "disapproval": "👎"
    }
    return emoji_mapping.get(sentiment, "")

def display_sentiment_results(sentiment_results, option):
    sentiment_text = ""
    for sentiment, score in sentiment_results.items():
        emoji = get_sentiment_emoji(sentiment)
        if option == "Sentiment Only":
            sentiment_text += f"{sentiment} {emoji}\n"
        elif option == "Sentiment + Score":
            sentiment_text += f"{sentiment} {emoji}: {score}\n"
    return sentiment_text

def inference(audio, sentiment_option):
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    lang = max(probs, key=probs.get)

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    sentiment_results = analyze_sentiment(result.text)
    sentiment_output = display_sentiment_results(sentiment_results, sentiment_option)

    return lang.upper(), result.text, sentiment_output

title = "🎤 Multilingual ASR 💬"
image_path = "/path/to/thumbnail.jpg"
description = """
    💻 This demo showcases Whisper, an advanced speech recognition model.
    ⚙️ Features: 
        - Multilingual speech recognition
        - Sentiment analysis
        - Language detection
"""

custom_css = """
    #banner-image { display: block; margin-left: auto; margin-right: auto; }
"""

block = gr.Blocks(css=custom_css)

with block:
    gr.HTML(title)
    with gr.Row():
        with gr.Column():
            gr.Image(image_path, elem_id="banner-image", show_label=False)
        with gr.Column():
            gr.HTML(description)

    with gr.Group():
        with gr.Row():
            audio = gr.Audio(label="Input Audio", show_label=False, type="filepath")
            sentiment_option = gr.Radio(choices=["Sentiment Only", "Sentiment + Score"], label="Select an option")
            btn = gr.Button("Transcribe")

    lang_str = gr.Textbox(label="Language")
    text = gr.Textbox(label="Transcription")
    sentiment_output = gr.Textbox(label="Sentiment Analysis Results")

    btn.click(inference, inputs=[audio, sentiment_option], outputs=[lang_str, text, sentiment_output])

    gr.HTML("<div>Model by <a href='https://github.com/openai/whisper' target='_blank'>OpenAI</a></div>")

block.launch()
