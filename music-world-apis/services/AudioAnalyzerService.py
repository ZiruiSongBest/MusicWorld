import whisper
from transformers import pipeline
import gradio as gr
import pathlib
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

class AudioAnalyzerService:
    def __init__(self):
        self.whisper_model = whisper.load_model("base")
        self.sentiment_analysis = pipeline(
            "sentiment-analysis",
            framework="pt",
            model="SamLowe/roberta-base-go_emotions",
            device="cuda"
        )
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        self.gemini_client = genai.GenerativeModel("gemini-1.5-pro")
    
    def analyze_sentiment(self, text):
        results = self.sentiment_analysis(text)
        sentiment_results = {result['label']: result['score'] for result in results}
        return sentiment_results

    def get_sentiment_emoji(self, sentiment):
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
    
    def display_sentiment_results(self, sentiment_results, option):
        sentiment_text = ""
        for sentiment, score in sentiment_results.items():
            emoji = self.get_sentiment_emoji(sentiment)
            if option == "Sentiment Only":
                sentiment_text += f"{sentiment} {emoji}\n"
            elif option == "Sentiment + Score":
                sentiment_text += f"{sentiment} {emoji}: {score}\n"
        return sentiment_text
    
    def transcribe_audio(self, audio_path):
        # transcription
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.whisper_model.device)
        
        # Detect language
        _, probs = self.whisper_model.detect_language(mel)
        lang = max(probs, key=probs.get)
        
        # Transcription
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(self.whisper_model, mel, options)
        
        return lang.upper(), result.text
    
    def audio_inference(self, input_data, sentiment_option):
        lang, text = self.transcribe_audio(input_data)
        
        sentiment_results = self.analyze_sentiment(text)
        sentiment_output = self.display_sentiment_results(sentiment_results, sentiment_option)
        
        return lang, text, sentiment_output

    def analyze_audio_file(self, file_path, prompt):
        """
        Analyze an audio file under 20MB by sending it inline to Gemini API along with a prompt.
        
        Args:
            file_path (str): The path to the audio file.
            prompt (str): The prompt to describe the task.
        
        Returns:
            tuple: (result_code, response_text). result_code 0 for success, 1 for error.
        """
        try:
            audio_data = pathlib.Path(file_path).read_bytes()
            mime_type = self._get_mime_type(file_path)

            response = self.gemini_client.generate_content([
                prompt,
                {
                    "mime_type": mime_type,
                    "data": audio_data
                }
            ])
            return 0, response.text  # Success
        except Exception as e:
            return 1, f"Error analyzing the audio file: {e}"

    def _get_mime_type(self, file_path):
        """
        Helper method to determine the MIME type based on the file extension.
        
        Args:
            file_path (str): The path to the file.
        
        Returns:
            str: The MIME type.
        """
        extension = pathlib.Path(file_path).suffix.lower()
        if extension == ".wav":
            return "audio/wav"
        elif extension == ".mp3":
            return "audio/mp3"
        elif extension == ".aiff":
            return "audio/aiff"
        elif extension == ".aac":
            return "audio/aac"
        elif extension == ".ogg":
            return "audio/ogg"
        elif extension == ".flac":
            return "audio/flac"
        else:
            raise ValueError(f"Unsupported audio format: {extension}")

audio_analyzer_service = AudioAnalyzerService()
