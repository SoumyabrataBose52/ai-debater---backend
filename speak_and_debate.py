import speech_recognition as sr
import requests

DEBATE_API_URL = "http://127.0.0.1:8000/debate/"

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your debate claim now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    return None

def send_to_debate(claim):
    payload = {"user_claim": claim}
    response = requests.post(DEBATE_API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        print("\nDebate Result:")
        print(f"-Claim: {result['claim']}")
        print(f"-Evidence: {result['evidence']}")
        print(f"-Counterargument: {result['counterargument']}")
        print(f"-Conclusion: {result['conclusion']}")

    else:
        print("API Error:", response.status_code, response.text)

if __name__ == "__main__":
    spoken_claim = recognize_speech()
    if spoken_claim:
        send_to_debate(spoken_claim)
