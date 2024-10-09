import websockets
import asyncio
import json
import base64
from pydub import AudioSegment
import os

prompt = """
I am uploading an audio file, and I would like a detailed and thorough analysis of its content. Please focus on the following aspects:

Main Theme or Summary: Provide a clear and concise summary of the main idea or topic discussed in the audio, if there is spoken text. Highlight the key points and purpose of the speech or conversation.

Voice Description: Analyze the human voice(s) in the audio, and provide detailed descriptions, including:

Gender (e.g., male, female)
Vocal tone and quality (e.g., gentle, rough, calm, energetic, assertive, etc.)
Any distinctive or noteworthy vocal characteristics (e.g., accents, intonation patterns)
Emotional Tone: Identify the emotions expressed by the speaker(s) throughout the audio. Describe the overall emotional tone (e.g., happy, sad, excited, frustrated), as well as any emotional changes or shifts during the speech.

Environmental Sounds: Identify and describe any background or environmental sounds in the audio, such as traffic noise, nature sounds, room acoustics, crowd noise, or any other non-verbal sounds present.
"""

def convert_audio_to_base64(audio_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    audio = audio.set_frame_rate(24000).set_channels(1).set_sample_width(2)
    raw_audio_data = audio.raw_data
    encoded_audio = base64.b64encode(raw_audio_data).decode('utf-8')
    return encoded_audio

async def send_audio_with_prompt(audio_file_path, prompt_text):
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
    encoded_audio = convert_audio_to_base64(audio_file_path)
    async with websockets.connect(
        url,
        extra_headers={
            "Authorization": "Bearer " + os.getenv("OPENAI_API_KEY"),
            "OpenAI-Beta": "realtime=v1",
        }
    ) as websocket:
        print("Connected to server.")
        event = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "audio": encoded_audio
                    },
                    {
                        "type": "input_text",
                        "text": prompt_text
                    }
                ]
            }
        }
        await websocket.send(json.dumps(event))
        print("Sent audio and text prompt.")
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            if data.get("type") == "response.created":
                text_response = data["response"]["content"][0]["text"]
                print(f"Response received: {text_response}")
                break

audio_file = "test_audio/exhausted_before_exam.mp3"
asyncio.run(send_audio_with_prompt(audio_file, prompt))
