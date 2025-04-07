from transformers import pipeline
from typing import Dict

# Initialize the zero-shot classification pipeline with a pre-trained model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def analyze_political_bias(text: str) -> Dict:
    """
    Analyzes the input text for political bias using a zero-shot classifier.

    Args:
        text (str): The user input text.

    Returns:
        Dict: A dictionary containing the bias label, confidence, a numeric bias score, 
              and an explanation.
    """
    # Use more descriptive candidate labels
    candidate_labels = [
        "The text expresses a liberal (left-leaning) political bias",
        "The text expresses a conservative (right-leaning) political bias",
        "The text is politically neutral"
    ]
    
    # Use a custom hypothesis template
    hypothesis_template = "This text expresses {} political bias."
    
    # Get zero-shot classification results using the custom hypothesis
    result = classifier(text, candidate_labels, hypothesis_template=hypothesis_template)
    
    # The label with the highest confidence is the top prediction
    top_label = result["labels"][0]
    top_score = result["scores"][0]
    
    # Map descriptive labels to a numeric bias score
    # (0.0: liberal, 0.5: neutral, 1.0: conservative)
    bias_mapping = {
        candidate_labels[0]: 0.0,
        candidate_labels[1]: 1.0,
        candidate_labels[2]: 0.5
    }
    bias_score = bias_mapping.get(top_label, 0.5)

    return {
        "text": text,
        "bias_label": top_label,
        "confidence": round(top_score, 2),
        "bias_score": round(bias_score, 2),
        "explanation": f"The model classified the text as '{top_label}' with {round(top_score * 100, 2)}% confidence."
    }

# Example usage:
text_input = "The government has recently announced policies that aim to redistribute wealth."
output = analyze_political_bias(text_input)
print(output)
