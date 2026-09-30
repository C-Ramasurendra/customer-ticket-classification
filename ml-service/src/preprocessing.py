"""
preprocessing.py
Shared text-cleaning logic. IMPORTANT: train.py and predict.py must both
call clean_text() so training and inference see identically-processed text.
"""
import re
import string


def clean_text(text: str) -> str:
    """
    Clean raw ticket text before vectorizing.
    Steps: lowercase -> remove placeholders -> remove punctuation/digits
    -> collapse whitespace.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()

    # Remove {{placeholder}} tokens some datasets (e.g. Bitext) include
    text = re.sub(r"\{\{.*?\}\}", " ", text)
    text = re.sub(r"\{.*?\}", " ", text)  # single-brace variants

    # Remove URLs / emails if present
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove standalone digits (keep words with letters+digits mixed as-is)
    text = re.sub(r"\b\d+\b", " ", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def clean_series(series):
    """Apply clean_text to a pandas Series of raw text."""
    return series.apply(clean_text)
