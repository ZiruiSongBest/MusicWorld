import google.generativeai as genai
import os
import time
# 读取 API 密钥
#GOOGLE_API_KEY = os.getenv('AIzaSyCzmyGtXMN8n3ew5w6DoLDpYvDUGvZ35LQ')
genai.configure(api_key='AIzaSyCzmyGtXMN8n3ew5w6DoLDpYvDUGvZ35LQ')

try:
    video_file_path = "test.mp4"

    print(f"Uploading file...")
    video_file = genai.upload_file(path=video_file_path)
    print(f"Completed upload: {video_file.uri}")
    # Create the prompt.
    prompt = "Summarize this video. Then create a quiz with answer key based on the information in the video."

    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# Make the LLM request.
    print("Making LLM inference request...")
    response = model.generate_content([video_file, prompt],
    request_options={"timeout": 600})

# Print the response, rendering any Markdown
    Markdown(response.text)
except Exception as e:
    print("An error occurred:", e)
