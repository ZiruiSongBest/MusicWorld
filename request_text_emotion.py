from openai import OpenAI
import json

client = OpenAI()

system_prompt = """
Text Classification Model for Emotions, Personality Traits, and Clinical Psychological Trait
"""

user_prompt = """
This model classifies text inputs based on emotions, text atmosphere, in text character personality traits, and clinical psychological traits. 
Provide the text you want to classify.

Examples:
Input: "I love my new job, it's fantastic!" {"emotion":"joy", "confidence_emotion":0.95, "intensity_emotion":0.90, "personality_trait":"optimistic", "confidence_trait":0.92, "clinical_trait":"non-depressive", "confidence_clinical":0.97}
Input: "I can't believe they messed up my order again!" {"emotion":"anger", "confidence_emotion":0.92, "intensity_emotion":0.85, "personality_trait":"impatient", "confidence_trait":0.90, "clinical_trait":"non-anxious", "confidence_clinical":0.95}
Input: "The food was great, but the service was terrible." {"emotion":"mixed", "confidence_emotion":0.88, "intensity_emotion":0.75, "personality_trait":"critical_thinker", "confidence_trait":0.87, "clinical_trait":"non-anxious", "confidence_clinical":0.94}
Input: "This product exceeded my expectations!" {"emotion":"surprise", "confidence_emotion":0.97, "intensity_emotion":0.80, "personality_trait":"open-minded", "confidence_trait":0.95, "clinical_trait":"non-depressive", "confidence_clinical":0.98}
Input: "I'm so frustrated with the slow internet connection!" {"emotion":"frustration", "confidence_emotion":0.93, "intensity_emotion":0.88, "personality_trait":"impatient", "confidence_trait":0.89, "clinical_trait":"non-anxious", "confidence_clinical":0.96}

"""

def request_text_emotion(text):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt + text}
        ],
        response_format={ "type": "json_object" }
    )

    text_emotion = json.loads(completion.choices[0].message.content)
    emotion = text_emotion['emotion']
    confidence_emotion = text_emotion['confidence_emotion']
    intensity_emotion = text_emotion['intensity_emotion']
    personality_trait = text_emotion['personality_trait']
    confidence_trait = text_emotion['confidence_trait']
    clinical_trait = text_emotion['clinical_trait']
    confidence_clinical = text_emotion['confidence_clinical']
    
    return emotion, confidence_emotion, intensity_emotion, personality_trait, confidence_trait, clinical_trait, confidence_clinical

print(request_text_emotion("I love my new job, it's fantastic!"))