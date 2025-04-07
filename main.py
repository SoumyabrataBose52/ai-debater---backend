from fastapi import FastAPI, HTTPException
from models import DebateRequest, DebateResponse, FactCheckRequest, FactCheckResponse, FallacyCheckRequest, FallacyCheckResponse, BiasCheckRequest, BiasCheckResponse
from debate_service import generate_debate_response
from fact_check_service import fact_check_claim
from fallacy_detection import detect_fallacies
from bias_analyzer import analyze_political_bias
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Debate Platform Backend is running!"}

@app.post("/debate", response_model=DebateResponse)
def debate(request: DebateRequest):
    try:
        debate_response = generate_debate_response(request.user_claim)
        return DebateResponse(**debate_response)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

@app.post("/fact-check", response_model=FactCheckResponse)
def fact_check(request: FactCheckRequest):
    try:
        fact_check_result = fact_check_claim(request.claim)
        return FactCheckResponse(**fact_check_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fact-checking failed.")

@app.post("/fallacy-check", response_model=FallacyCheckResponse)
def fallacy_check(request: FallacyCheckRequest):
    try:
        detected_fallacies = detect_fallacies(request.text)
        return FallacyCheckResponse(text=request.text, fallacies=detected_fallacies)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fallacy detection failed.")

@app.post("/bias-check", response_model=BiasCheckResponse)
def bias_check(request: BiasCheckRequest):
    """
    Endpoint to analyze political bias in the provided text.
    """
    try:
        result = analyze_political_bias(request.text)
        return BiasCheckResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Bias detection failed.")
    