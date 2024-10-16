import whisper
from transformers import pipeline
import gradio as gr
import pathlib
import google.generativeai as genai
import os
from services.prompt import prompt as prompt_template
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
    
    def transcribe_audio(self, audio_path):
        try:
            # Load and preprocess audio
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
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None, None
    
    def audio_inference(self, audio_path):
        lang, text = self.transcribe_audio(audio_path)
        print("lang: ", lang)
        print("text: ", text)
        results = self.sentiment_analysis(text)
        sentiment_results = {result['label']: result['score'] for result in results}
        sentiment_text = ""
        for sentiment, score in sentiment_results.items():
            sentiment_text += f"{sentiment}: {score}\n"
        return lang, text, sentiment_text
    
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
    
    def analyze_audio_gemini(self, audio_path, prompt):
        """
        Analyze an audio file under 20MB by sending it inline to Gemini API along with a prompt.
        
        Args:
            audio_path (str): The path to the audio file.
            prompt (str): The prompt to describe the task.
        
        Returns:
            tuple: (result_code, response_text). result_code 0 for success, 1 for error.
        """
        try:
            mime_type = self._get_mime_type(audio_path)
            
            audio_data = open(audio_path, 'rb').read()

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
    
    def audio_analysis(self, audio_path, prompt):
        """
        Analyze an audio file.

        Args:
            audio_path (str): The path to the audio file.
            prompt (str): The prompt to describe the task.

        Returns:
            str: The response text.
        """
        try:
            audio_inference_result = self.audio_inference(audio_path)

            audio_prompt = prompt_template["analyze_audio"].format(emotion=audio_inference_result)
            if prompt:
                audio_prompt += f"\nAlso user attached additional prompt: {prompt}"
            audio_prompt += "\nHere begin your analysis:"

            audio_analysis_result = self.analyze_audio_gemini(audio_path, audio_prompt)

            print("Gemini response:", audio_analysis_result)

            return audio_analysis_result
            # return audio_prompt
        except Exception as e:
            return f"Error analyzing the audio file: {e}"

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
