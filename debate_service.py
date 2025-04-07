import json
import re
import google.generativeai as genai
from config import GEMINI_API_KEY
from fallacy_detection import detect_fallacies  # Import fallacy detection

genai.configure(api_key=GEMINI_API_KEY)

def clean_json(text):
    """ Extract and clean JSON from Gemini response using regex. """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group()
    return None

def generate_debate_response(user_claim: str):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    You are an AI Debate Assistant. Generate a structured debate response in strict JSON format. 
    Do not include any extra text, explanations, or markdown. 
    Only output a JSON object with the following keys: "claim", "evidence", "counterargument", "conclusion".

    Example:
    {{
      "claim": "AI will replace human jobs.",
      "evidence": "Automation has already replaced many repetitive jobs, such as manufacturing and data entry. AI can work 24/7 without breaks, improving efficiency.",
      "counterargument": "AI also creates new job opportunities in AI development, maintenance, and oversight. Historically, technological advances have shifted jobs rather than eliminated them.",
      "conclusion": "While AI may replace some jobs, it will also generate new employment opportunities. The future depends on how society adapts to these changes."
    }}

    User Claim: "{user_claim}"
    """

    response = model.generate_content(prompt)

    # Extract JSON if Gemini adds extra text
    cleaned_json = clean_json(response.text)

    if not cleaned_json:
        raise ValueError("Gemini response was not valid JSON.")

    try:
        debate_response = json.loads(cleaned_json)
    except json.JSONDecodeError:
        raise ValueError("Gemini response contained invalid JSON format.")

    # Detect fallacies in the AI-generated response
    detected_fallacies = {
        "evidence_fallacies": detect_fallacies(debate_response.get("evidence", "")),
        "counterargument_fallacies": detect_fallacies(debate_response.get("counterargument", "")),
        "conclusion_fallacies": detect_fallacies(debate_response.get("conclusion", ""))
    }

    # Add detected fallacies to the response
    debate_response["fallacies"] = detected_fallacies

    return debate_response

