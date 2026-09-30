
"""
predict.py
Phase 1e: load the saved model + vectorizer once, expose predict_ticket()
for use by app.py.
 
Also loads templates.json (built by extract_templates.py) to attach a
suggested reply template based on the predicted category.
 
Note: LinearSVC has no predict_proba, so we convert its decision_function
scores to pseudo-probabilities via softmax to get a confidence value.
The calibrated model (CalibratedClassifierCV) has predict_proba natively
and is used directly - this is the path you'll hit if you followed the
notebooks through 06_save_model.ipynb.
"""
import os
import json
import numpy as np
import joblib
from preprocessing import clean_text
 
# Build paths relative to THIS file's location, not the current working
# directory. This way it works no matter which folder you run uvicorn from.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(_THIS_DIR, "..", "models", "model.pkl")
VECTORIZER_PATH = os.path.join(_THIS_DIR, "..", "models", "vectorizer.pkl")
TEMPLATES_PATH = os.path.join(_THIS_DIR, "..", "models", "templates.json")
 
_model = joblib.load(MODEL_PATH)
_vectorizer = joblib.load(VECTORIZER_PATH)
 
# Templates are optional - if extract_templates.py hasn't been run yet,
# predictions still work, just without a suggested_response field.
try:
    with open(TEMPLATES_PATH, "r", encoding="utf-8") as f:
        _templates = json.load(f)
except FileNotFoundError:
    _templates = {}
 
 
def _softmax(scores):
    exp_scores = np.exp(scores - np.max(scores))
    return exp_scores / exp_scores.sum()
 
 
def predict_ticket(text: str) -> dict:
    """
    Takes raw ticket text, returns:
    {"category": str, "confidence": float, "suggested_response": str | None}
    """
    cleaned = clean_text(text)
    features = _vectorizer.transform([cleaned])
 
    if hasattr(_model, "predict_proba"):
        # Calibrated model / LogisticRegression path
        probs = _model.predict_proba(features)[0]
        idx = int(np.argmax(probs))
        category = _model.classes_[idx]
        confidence = float(probs[idx])
    else:
        # Uncalibrated LinearSVC path -> softmax over decision scores
        scores = _model.decision_function(features)[0]
        probs = _softmax(scores)
        idx = int(np.argmax(probs))
        category = _model.classes_[idx]
        confidence = float(probs[idx])
 
    category = str(category)
    suggested_response = _templates.get(category)
 
    return {
        "category": category,
        "confidence": round(confidence, 4),
        "suggested_response": suggested_response,
    }
 
 
if __name__ == "__main__":
    # quick manual test
    sample = "I want to track my refund for order 12345"
    print(predict_ticket(sample))
 
