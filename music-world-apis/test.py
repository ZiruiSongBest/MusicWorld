from services.AudioAnalyzerService import audio_analyzer_service

result = audio_analyzer_service.audio_analysis("/home/yaohli/Data/workspace/music_gen/MusicWorld/testcases/kidsplaying.mp3", None)

print('-' * 100)
print(result)