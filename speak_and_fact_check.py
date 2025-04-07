import speech_recognition as sr
import requests

FASTAPI_URL = "http://127.0.0.1:8000/fact-check"

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak your claim now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition; {e}")
    
    return None

def send_to_fact_check(claim):
    payload = {"claim": claim}
    response = requests.post(FASTAPI_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        print("\nFact-Check Result:")
        print(f"- Claim: {result['claim']}")
        print(f"- Truth Value: {'True' if result['is_true'] else 'False'}")
        print(f"- Confidence Score: {result['confidence_score']}")
        print(f"- Sources:\n  - " + "\n  - ".join(result["sources"]))
    else:
        print("API Error:", response.status_code, response.text)

if __name__ == "__main__":
    spoken_claim = recognize_speech()
    if spoken_claim:
        send_to_fact_check(spoken_claim)
