import datetime
from typing import Dict, List, Union

User = {
    "user_id": str,  # Unique identifier for each user
    "nickname": str, # User's nickname
    "name": str,  # User's name
    "age": int,  # User's age
    "gender": str,  # User's gender
    "preferences": {  # User's music and emotion preferences
        "genres": List[str],  # Preferred music genres (e.g., classical, rock, jazz)
        "mood_preferences": List[str],  # Preferred moods for music (e.g., happy, calm, energetic)
        "instrument_preferences": List[str],  # Preferred instruments (e.g., piano, guitar, violin)
    },
    "history": List[Dict],  # List of previous interactions, containing emotion and generated music details
}

EmotionData = {
    "input_id": str,  # Unique identifier for each user input
    "user_id": str,  # Reference to the User ID
    "input_type": str,  # Type of input ("text" or "audio")
    "input_content": Union[str, bytes],  # User input data (text or audio)
    "timestamp": datetime,  # Time when the input was recorded
    "emotion_analysis": {  # Result of the emotion analysis
        "primary_emotion": str,  # Detected primary emotion (e.g., joy, sadness, anger)
        "emotion_scores": Dict[str, float],  # Scores for multiple emotions (e.g., {"joy": 0.8, "sadness": 0.2})
    },
    "context": str,  # Additional context (e.g., location, activity)
}

MusicData = {
    "music_id": str,  # Unique identifier for each generated music piece
    "user_id": str,  # Reference to the User ID
    "input_id": str,  # Reference to the Input ID associated with this music
    "emotion_used": str,  # Emotion used for generating this music
    "generation_parameters": {  # Parameters used for music generation
        "tempo": int,  # Tempo of the generated music
        "key": str,  # Musical key (e.g., C major, G minor)
        "instrumentation": List[str],  # Instruments used in the music
        "style": str,  # Style of the music (e.g., classical, rock)
    },
    "music_file": bytes,  # The generated music file (in binary format, e.g., MP3 or WAV)
    "timestamp": datetime,  # Time when the music was generated
}

FeedbackData = {
    "feedback_id": str,  # Unique identifier for each feedback entry
    "user_id": str,  # Reference to the User ID
    "music_id": str,  # Reference to the generated Music ID
    "rating": int,  # User rating (e.g., 1 to 5)
    "comments": str,  # User comments for feedback
    "timestamp": datetime,  # Time when feedback was given
}


UIInteractionData = {
    "interaction_id": str,  # Unique identifier for each UI interaction
    "user_id": str,  # Reference to the User ID
    "action": str,  # Action performed by the user (e.g., "play", "pause", "skip")
    "timestamp": datetime,  # Time when the interaction occurred
    "session_duration": float,  # Duration of the session in seconds
}

SystemLog = {
    "log_id": str,  # Unique identifier for each log entry
    "event_type": str,  # Type of event (e.g., "error", "info", "warning")
    "description": str,  # Description of the event
    "timestamp": datetime,  # Time when the event occurred
    "severity_level": str,  # Severity of the log entry (e.g., "low", "medium", "high")
}

