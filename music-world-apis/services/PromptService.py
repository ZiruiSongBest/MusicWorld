from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

import os
import google.generativeai as genai

class PromptService:
    def __init__(self, openai_api_key=None):
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        self.gemini_client = genai.GenerativeModel("gemini-1.5-pro")
        self.openai_client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))

    def analyze_audio_file(self, file_path, prompt):
        """
        Analyze an audio file under 20MB by sending it inline to Gemini API along with a prompt.
        
        Args:
            file_path (str): The path to the audio file.
            prompt (str): The prompt to describe the task.
        
        Returns:
            tuple: (result_code, response_text). result_code 0 for success, 1 for error.
        """
        pass

    def generate_chat_response(self, text, image_url=None, model="gpt-4o"):
        """
        Create a chat response that using OpenAI.
        
        Args:
            text (str): prompt.
            image_url (str): Optional image.
            model (str): default: gpt-4o.
        
        Returns:
            tuple: (result_code, response_text). result_code 0 for success, 1 for error.
        """
        try:
            messages = [{"role": "user", "content": {"type": "text", "text": text}}]

            if image_url:
                image_content = {
                    "type": "image_url",
                    "image_url": {"url": image_url}
                }
                messages.append({"role": "user", "content": image_content})

            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=512
            )

            return 0, response.choices[0]['message']['content']
        except Exception as e:
            return 1, f"Error creating the prompt: {e}"

prompt_service = PromptService()