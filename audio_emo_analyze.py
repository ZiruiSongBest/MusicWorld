
from pydub import AudioSegment
from funasr import AutoModel
import os

class EmotionModel:
    def __init__(self, model_name="iic/emotion2vec_plus_large"):
        self.model = AutoModel(
            model=model_name,
            # vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
            # vad_model_revision="master",
            # vad_kwargs={"max_single_segment_time": 2000},
        )

    def generate(self, audio_file, output_dir="./outputs", granularity="utterance", extract_embedding=False):
        return self.model.generate(
            audio_file, output_dir=output_dir, granularity=granularity, extract_embedding=extract_embedding
        )

def split_audio(input_file, segment_length=30000):
    audio = AudioSegment.from_file(input_file)

    total_length = len(audio)
    
    num_segments = total_length // segment_length
    segments = []

    for i in range(num_segments + 1):
        start_time = i * segment_length
        end_time = min((i + 1) * segment_length, total_length)
        segment = audio[start_time:end_time]
        segments.append(segment)

    return segments

audio_file = 'happy.m4a'
segments = split_audio(audio_file)

print(f"The audio has been split into {len(segments)} segments, each segment is 30 seconds long (or the last segment is less than 30 seconds)")

model = EmotionModel()

for i, segment in enumerate(segments):
    segment.export(f"segment_{i}.wav", format="wav")
    res = model.generate(f"segment_{i}.wav")
    print(f"Segment {i} emotion recognition result: {res}")
    os.remove(f"segment_{i}.wav")