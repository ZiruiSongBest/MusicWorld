import whisper
from transformers import pipeline
import gradio as gr

class SentimentAnalyzerService:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.sentiment_analysis = pipeline(
            "sentiment-analysis",
            framework="pt",
            model="SamLowe/roberta-base-go_emotions",
            device="cuda"
        )
    
    def analyze_sentiment(self, text):
        results = self.sentiment_analysis(text)
        sentiment_results = {result['label']: result['score'] for result in results}
        return sentiment_results

sentiment_analyzer_service = SentimentAnalyzerService()