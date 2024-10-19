import json
from openai import OpenAI
from dotenv import load_dotenv
from services.prompt import prompt_template
import os
import base64

load_dotenv()

class PromptService:
    def __init__(self, openai_api_key=None):
        self.openai_client = OpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))

    def get_response(self, messages, model="gpt-4o-mini", json_output=False):
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
            # print('*' * 10)
            # print('openai prompt:', json.dumps(messages, indent=2))
            # print('*' * 10)

            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=512,
                response_format={"type": "json_object"} if json_output else None
            )
            print('Model response:', response.choices[0].message.content)
            return 0, response.choices[0].message.content
        except Exception as e:
            return 1, f"Error creating the prompt: {e}"
    
    def create_prompt(self, template, text, image_paths=None):
        print("Requested template:", template)
        print("Available templates:", list(prompt_template.keys()))
        try:
            prompt_text = prompt_template[template].format(input=text)
            messages = [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]

            if image_paths:
                for image_path in image_paths:
                    try:
                        with open(image_path, "rb") as image_file:
                            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                        messages[0]["content"].append({
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        })
                    except Exception as e:
                        print(f"Error processing image {image_path}: {e}")

            return messages

        except KeyError:
            prompt_text = (
                "You are a music generation expert. Now we have various input from the user as follows:\n"
                "{{input}}\n"
                "Summarize the information as a Title and a Description.\n"
                "Title: A concise title for the music piece.\n"
                "Description: A brief description of the music piece.\n"
                "Keep your response in 5 words for Title and 20 words for Description."
                "Example Json Output: {\"Title\": \"Mystery of the Unknown\", \"Description\": \"A mysterious and enchanting piece that evokes a sense of wonder and curiosity.\"}"
            ).format(input=text)
            print(f"Warning: Template '{template}' not found in prompt. Using default template.")
            return [{"role": "user", "content": [{"type": "text", "text": prompt_text}]}]
        except Exception as e:
            print(f"Error creating prompt: {e}")
            return [{"role": "user", "content": [{"type": "text", "text": text}]}]

    def get_text(self, text_paths):
        text_information = []
        for text_path in text_paths:
            with open(text_path, 'r') as file:
                text = file.read()
                text_information.append(text)
        text = "\n".join(text_information)
        return text

    def parse_summary_response(self, response):
        try:
            # Attempt to parse the response as JSON
            summary = json.loads(response)
            return summary
        except json.JSONDecodeError:
            # If JSON parsing fails, return a dictionary with error information
            return {
                "Title": "Error parsing response",
                "Description": "The response could not be parsed as JSON. Original response: " + response
            }

prompt_service = PromptService()

# if __name__ == "__main__":
#     service = PromptService()

#     result_code, prompt_response = service.create_prompt("Describe this image", image_url="https://example.com/image.jpg")
#     if result_code == 0:
#         print(prompt_response)
#     else:
#         print(f"Error: {prompt_response}")
