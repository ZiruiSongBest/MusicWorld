import torch
import soundfile as sf
from diffusers import StableAudioPipeline

class AudioGenerator:
    def __init__(self, model_path=None, device="cuda"):
        if model_path == None:
            raise
        self.pipe = StableAudioPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
        self.pipe = self.pipe.to(device)
        self.device = device
    
    def get_prompt(self, text_prompt, emotion):
        return text_prompt

    def generate_audio(self, prompt, output_file='test.wav', negative_prompt=None, num_inference_steps=200, 
                       audio_end_in_s=40.0, num_waveforms_per_prompt=1, seed=0):
        
        generator = torch.Generator(self.device).manual_seed(seed)
        
        audio = self.pipe(
            prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            audio_end_in_s=audio_end_in_s,
            num_waveforms_per_prompt=num_waveforms_per_prompt,
            generator=generator,
        ).audios

        output = audio[0].T.float().cpu().numpy()

        # sf.write(output_file, output, self.pipe.vae.sampling_rate)
        
        return output

audio_generator_service = AudioGenerator('stabilityai/stable-audio-open-1.0')