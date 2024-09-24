import torch
import soundfile as sf
from diffusers import StableAudioPipeline

class AudioGenerator:
    def __init__(self, model_path, device="cuda"):
        self.pipe = StableAudioPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
        self.pipe = self.pipe.to(device)
        self.device = device

    def generate_audio(self, prompt, output_file, negative_prompt=None, num_inference_steps=200, 
                       audio_end_in_s=10.0, num_waveforms_per_prompt=1, seed=0):
        """
        Args:
        - prompt (str): The text description of the audio to generate.
        - output_file (str): The path to save the generated audio file.
        - negative_prompt (str, optional): Describes what to avoid in the audio generation. Default is None.
        - num_inference_steps (int, optional): Number of inference steps. Default is 200.
        - audio_end_in_s (float, optional): Length of generated audio in seconds. Default is 10.0.
        - num_waveforms_per_prompt (int, optional): Number of audio waveforms to generate. Default is 1.
        - seed (int, optional): Seed for the generator for reproducibility. Default is 0.
        
        Returns:
        - output (numpy.ndarray): The generated audio waveform as a numpy array.
        """
        
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

        sf.write(output_file, output, self.pipe.vae.sampling_rate)
        
        return output