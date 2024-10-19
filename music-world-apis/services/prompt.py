prompt_template = {
    "analyze_audio": (
        "You are a audio analysis expert. We have used model to transcribe the audio and get the emotion as follows:\n"
        "{emotion}\n"
        "Based on the analysis and your own judgement, please give a simple analysis of the audio piece with following aspects:\n"
        "1. Basic description of the audio piece\n"
        "2. The instruments and the emotions expressed (if there is any)\n"
        "3. The scene and genre of the audio piece\n"
    ),
    "generate_audio_prompt": (
        "You are a music generation expert. Now we have various input from the user as follows:\n"
        "{input}\n"
        "Generate keywords for a piece of music considering the following four aspects:\n\n"
        "Instrument: Suggest a type of musical instrument or combination of instruments that would suit the overall mood and theme. This could range from classical instruments like piano, violin, or flute, to modern instruments like electric guitar or synthesizer.\n\n"
        "Melody: Describe the type of melody that would best fit the mood of the piece. Consider whether it should be fast-paced, slow, uplifting, melancholic, rhythmic, smooth, or dynamic.\n\n"
        "Scene: Provide a scene or setting that could inspire the music. This could be a physical place (like a forest, cityscape, or beach), a time of day (such as dawn, dusk, or midnight), or a specific event (like a celebration, meditation, or a battle).\n\n"
        "Description: Give a brief description of the intended mood, atmosphere, or story behind the music. Use emotional and sensory language to convey the feeling the music should evoke, such as 'mysterious and enchanting,' 'bright and energetic,' or 'calm and introspective.'\n\n"
        "The output should consist of four keywords or phrases that capture each aspect clearly and complement each other to inspire the music composition. Only output the keywords, no more text."
    ),
    "summarize": (
        "You are a music generation expert. Now we have various input from the user as follows:\n"
        "{{input}}\n"
        "Summarize the information as a Title and a Description.\n"
        "Title: A concise title for the music piece.\n"
        "Description: A brief description of the music piece.\n"
        "Keep your response in 5 words for Title and 15 words for Description."
        "Your json output should have a dict with two keys: 'Title' and 'Description'."
    )
}
