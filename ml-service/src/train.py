"""
train.py
Phase 1c + 1d: fit TF-IDF, train Linear SVM and Logistic Regression,
compare on validation set, evaluate the winner on test set, save
model + vectorizer to models/.

Usage:
    python src/train.py
"""
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, f1_score, confusion_matrix

from preprocessing import clean_series

DATA_DIR = "data/processed"
MODEL_DIR = "models"


def load_split(name):
    df = pd.read_csv(f"{DATA_DIR}/{name}.csv")
    df["clean_text"] = clean_series(df["text"])
    return df


def main():
    train_df = load_split("train")
    val_df = load_split("val")
    test_df = load_split("test")

    # --- Feature engineering: fit TF-IDF on TRAIN ONLY (avoid leakage) ---
    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 2),   # unigrams + bigrams
        min_df=2,
        sublinear_tf=True,
    )
    X_train = vectorizer.fit_transform(train_df["clean_text"])
    X_val = vectorizer.transform(val_df["clean_text"])
    X_test = vectorizer.transform(test_df["clean_text"])

    y_train, y_val, y_test = train_df["label"], val_df["label"], test_df["label"]

    # --- Train candidate models ---
    svm = LinearSVC(class_weight="balanced", max_iter=5000)
    svm.fit(X_train, y_train)

    logreg = LogisticRegression(
        class_weight="balanced", max_iter=2000, n_jobs=-1
    )
    logreg.fit(X_train, y_train)

    # --- Compare on validation set ---
    svm_val_pred = svm.predict(X_val)
    logreg_val_pred = logreg.predict(X_val)

    svm_f1 = f1_score(y_val, svm_val_pred, average="macro")
    logreg_f1 = f1_score(y_val, logreg_val_pred, average="macro")

    print(f"Linear SVM       -> validation macro-F1: {svm_f1:.4f}")
    print(f"Logistic Regr.   -> validation macro-F1: {logreg_f1:.4f}")

    best_model, best_name = (svm, "LinearSVC") if svm_f1 >= logreg_f1 else (logreg, "LogisticRegression")
    print(f"\nSelected best model: {best_name}")

    # --- Final evaluation on held-out test set ---
    test_pred = best_model.predict(X_test)
    print("\n=== Test set classification report ===")
    print(classification_report(y_test, test_pred))
    print("=== Confusion matrix ===")
    print(confusion_matrix(y_test, test_pred))

    # --- Save model + vectorizer together ---
    joblib.dump(best_model, f"{MODEL_DIR}/model.pkl")
    joblib.dump(vectorizer, f"{MODEL_DIR}/vectorizer.pkl")
    print(f"\nSaved model.pkl and vectorizer.pkl to {MODEL_DIR}/")


if __name__ == "__main__":
    main()
