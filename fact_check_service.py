import google.generativeai as genai
import json
import re
import requests
from config import GEMINI_API_KEY, GOOGLE_FACT_CHECK_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def clean_json(text):
    """ Extract JSON from AI response using regex """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group()
    return None

def query_wikipedia(claim):
    """ Search Wikipedia for a relevant page and return the summary. """
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={claim}"
    response = requests.get(search_url).json()

    if "query" in response and response["query"]["search"]:
        title = response["query"]["search"][0]["title"]
        page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
        summary_response = requests.get(summary_url).json()
        summary = summary_response.get("extract", "No summary available.")

        return {"title": title, "summary": summary, "url": page_url}
    return None

def query_google_fact_check(claim):
    """ Query Google Fact Check API for verification. """
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={claim}&key={GOOGLE_FACT_CHECK_API_KEY}"
    response = requests.get(url).json()

    sources = []
    is_true = None

    if "claims" in response:
        for claim_data in response["claims"]:
            for review in claim_data.get("claimReview", []):
                sources.append(review["url"])
                rating = review["textualRating"].lower()

                if "true" in rating or "correct" in rating:
                    is_true = True
                elif "false" in rating or "incorrect" in rating:
                    is_true = False

    return {"is_true": is_true, "sources": sources}

def fact_check_with_gemini(claim):
    """ Use Gemini AI to fact-check a claim. """
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are a fact-checking AI. Check the accuracy of the claim and return results in JSON format.
    
    Output Format:
    {{
        "claim": "{claim}",
        "is_true": true/false,
        "sources": ["https://reliable-source1.com", "https://reliable-source2.com"]
    }}

    Claim: "{claim}"
    """

    response = model.generate_content(prompt)

    cleaned_json = clean_json(response.text)
    
    if not cleaned_json:
        return {"is_true": None, "sources": []}

    try:
        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        return {"is_true": None, "sources": []}

def compute_confidence_score(results):
    """ Compute confidence score based on agreement among sources. """
    truth_votes = sum(1 for r in results if r["is_true"] is True)
    false_votes = sum(1 for r in results if r["is_true"] is False)
    total_votes = truth_votes + false_votes

    if total_votes == 0:
        return 0.5  # Neutral confidence if no clear decision

    return round(truth_votes / total_votes, 2)  # Normalize confidence score

def fact_check_claim(claim: str):
    wikipedia_result = query_wikipedia(claim)
    google_result = query_google_fact_check(claim)
    gemini_result = fact_check_with_gemini(claim)

    sources = google_result["sources"] + gemini_result["sources"]
    if wikipedia_result:
        sources.append(wikipedia_result["url"])

    results = [google_result, gemini_result]
    if wikipedia_result:
        results.append({"is_true": True, "sources": [wikipedia_result["url"]]})

    confidence_score = compute_confidence_score(results)

    return {
        "claim": claim,
        "is_true": confidence_score > 0.5,
        "sources": sources if sources else ["No verified sources found"],
        "confidence_score": confidence_score
    }

