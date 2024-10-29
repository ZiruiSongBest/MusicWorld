prompt_template = {
    "analyze_audio": (
        "You are a audio analysis expert. We have used model to transcribe the audio and get the emotion as follows:\n"
        "{emotion}\n"
        "Based on the analysis and your own judgement, please give a simple analysis of the audio piece with following aspects:\n"
        "1. Basic description of the audio piece\n"
        "2. The instruments and the emotions expressed (if there is any)\n"
        "3. The scene and genre of the audio piece\n"
    ),
    "instruction_analysis": (
        "You are a audio generation expert.\nThe user gives an instruction:\n"
        "{input}\n"
        "Please describe the audio instruction of what the user want in one sentence."
    ),
    "generate_audio_prompt": (
        "You are a audio generation expert.\n"
        "{input}\n"
        "Generate keywords for a piece of audio considering the following four aspects:\n\n"
        # "Instrument/Sound: Suggest a type of musical instrument or sound that would suit the overall mood and theme. This could range from classical instruments like piano, violin, or flute, to modern instruments like electric guitar or synthesizer. It can also be a sound effect, or animal sound. Be creative and brave to use unconventional instruments.\n\n"
        # "Melody: Describe the type of melody that would best fit the mood of the piece. Consider whether it should be fast-paced, slow, uplifting, melancholic, rhythmic, smooth, or dynamic.\n\n"
        # "Scene: Provide a scene or setting that could inspire the music. This could be a physical place (like a forest, cityscape, or beach), a time of day (such as dawn, dusk, or midnight), or a specific event (like a celebration, meditation, or a battle).\n\n"
        # "Description: Give a brief description of the intended mood, atmosphere, or story behind the music. Use emotional and sensory language to convey the feeling the music should evoke, such as 'mysterious and enchanting,' 'bright and energetic,' or 'calm and introspective.'\n\n"
        "Sound, Scene, Melody (if any), Description\n"
        "The output should consist of four keywords or phrases that capture each aspect clearly and complement each other to inspire the music composition. If user's instruction or scene explicitly mentions what audio/music should be, you should align to the user's instruction, otherwise you should generate a music piece that best match the scene or emotion. Only output the keywords, no more other text. Example: 'Bird chirping, cheerful, forest, morning'"
    ),
    "summarize": (
        "You are a audio generation expert.\n"
        "{input}\n"
        "Based on the user's instruction and audio theme, summarize the audio piece as a Title and a Description that best contain the theme.\n"
        "Title: A concise title for the audio piece.\n"
        "Description: A brief description of the audio piece.\n"
        "Length: The length of the audio piece in seconds that is good for this situation, range from 10 to 42 seconds.\n"
        "Keep your response in 5 words for Title and 15 words for Description."
        "Your json output should have a dict with three keys: 'Title' and 'Description' and 'Length."
    )
}
