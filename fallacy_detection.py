import re
from typing import List

def detect_fallacies(text: str) -> List[str]:
    """
    Detects logical fallacies in a given text.
    Returns a list of detected fallacies.
    """
    fallacies = {
        "Strawman Argument": r"\b(misrepresents|distorts).*?(opponent|argument)\b",
        "Slippery Slope": r"\b(if.*?then.*?(lead to|result in))\b",
        "Appeal to Fear": r"\b(if we don’t.*?horrible consequences|disastrous results)\b",
        "False Equivalence": r"\b(this is just like|equally as bad as)\b",
        "Ad Hominem": r"\b(attacks.*?(person|character).*?(not argument))\b",
        "Circular Reasoning": r"\b(because.*?\b(same claim|repeats\b))\b"
    }
    
    detected = []
    for fallacy, pattern in fallacies.items():
        if re.search(pattern, text, re.IGNORECASE):
            detected.append(fallacy)
    
    return detected