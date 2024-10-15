from openai import OpenAI
from dotenv import load_dotenv
from services.prompt import prompt
import os

load_dotenv()

import os
import pathlib
import google.generativeai as genai
import openai

class PromptService:
    def __init__(self, gemini_api_key=None, openai_api_key=None):
        # Initialize the Gemini and OpenAI clients with provided API keys
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        self.gemini_client = genai.GenerativeModel("gemini-1.5-pro")
        self.openai_client = openai.OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))

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

    def create_prompt(self, text, image_url=None, model="gpt-4o"):
        """
        Create a prompt that combines text and optional image content using OpenAI.
        
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

    def _get_mime_type(self, file_path):
        """
        determine the MIME type based on the file extension.
        
        Args:
            file_path (str): path to the file.
        
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

prompt_service = PromptService()

# # Example usage:
# if __name__ == "__main__":
#     service = PromptService()

#     # Analyze an audio file with a prompt (e.g., summarize or transcribe)
#     result_code, response = service.analyze_audio_file("sample.mp3", "Summarize the audio content")
#     if result_code == 0:
#         print(response)
#     else:
#         print(f"Error: {response}")

#     # Create a text and image-based prompt
#     result_code, prompt_response = service.create_prompt("Describe this image", image_url="https://example.com/image.jpg")
#     if result_code == 0:
#         print(prompt_response)
#     else:
#         print(f"Error: {prompt_response}")