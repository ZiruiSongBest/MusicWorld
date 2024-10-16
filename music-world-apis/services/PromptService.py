from openai import OpenAI
from dotenv import load_dotenv
from services.prompt import prompt as prompt_template
import os

load_dotenv()

class PromptService:
    def __init__(self, openai_api_key=None):
        self.openai_client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))

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
            prompt_text = prompt_template["generate_audio_prompt"].format(input=text)
            
            print('*' * 10)
            print('openai prompt:', prompt_text)
            print('*' * 10)

            messages = [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]

            if image_url:
                messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {"url": image_url}
                })

            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=512
            )
            print('Model response:', response.choices[0].message.content)
            return 0, response.choices[0].message.content
        except Exception as e:
            return 1, f"Error creating the prompt: {e}"

prompt_service = PromptService()

# if __name__ == "__main__":
#     service = PromptService()

#     result_code, prompt_response = service.create_prompt("Describe this image", image_url="https://example.com/image.jpg")
#     if result_code == 0:
#         print(prompt_response)
#     else:
#         print(f"Error: {prompt_response}")
