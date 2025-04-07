from pydantic import BaseModel
from typing import List, Dict

# Debate Models
class DebateRequest(BaseModel):
    user_claim: str

class DebateResponse(BaseModel):
    claim: str
    evidence: str
    counterargument: str
    conclusion: str
    fallacies: Dict[str, List[str]]  # AI-generated fallacies

# Fact-Checking Models
class FactCheckRequest(BaseModel):
    claim: str

class FactCheckResponse(BaseModel):
    claim: str
    is_true: bool
    sources: List[str]
    confidence_score: float

# Fallacy Detection Models
class FallacyCheckRequest(BaseModel):
    text: str

class FallacyCheckResponse(BaseModel):
    text: str
    fallacies: List[str]

class BiasCheckRequest(BaseModel):
    text: str

class BiasCheckResponse(BaseModel):
    text: str
    bias_label: str
    confidence: float
    bias_score: float
    explanation: str