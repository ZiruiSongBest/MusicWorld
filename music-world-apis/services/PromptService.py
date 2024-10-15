from openai import OpenAI
from dotenv import load_dotenv
from services.prompt import prompt
import os

load_dotenv()

class PromptService:
    def __init__(self, openai_api_key=None):
        self.openai_client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))

    def create_prompt(self, text, image_url=None, model="gpt-4o-mini"):
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
            print('Model response:', response.choices[0]['message']['content'])
            return 0, response.choices[0]['message']['content']
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