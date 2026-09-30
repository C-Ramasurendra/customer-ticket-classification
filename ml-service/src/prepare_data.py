"""
prepare_data.py
Phase 1a: load the raw dataset, inspect it, split into train/val/test,
save to data/processed/.

Usage:
    python src/prepare_data.py

Before running: place the raw CSV at data/raw/tickets.csv
Adjust TEXT_COL and LABEL_COL below to match your actual downloaded file.
"""
import pandas as pd
from sklearn.model_selection import train_test_split

# ---- CONFIG: change these two if your CSV has different column names ----
RAW_PATH = "data/raw/tickets.csv"
TEXT_COL = "instruction"   # the ticket text column
LABEL_COL = "category"     # the 11-class label column (use "intent" for 27-class)
# ---------------------------------------------------------------------

OUT_DIR = "data/processed"


def main():
    print(f"Loading {RAW_PATH} ...")
    df = pd.read_csv(RAW_PATH)

    print("\nColumns found:", list(df.columns))
    print("\nShape:", df.shape)

    if TEXT_COL not in df.columns or LABEL_COL not in df.columns:
        raise ValueError(
            f"Expected columns '{TEXT_COL}' and '{LABEL_COL}' not found. "
            f"Actual columns: {list(df.columns)}. Update TEXT_COL/LABEL_COL above."
        )

    # Keep only what we need, drop missing/duplicate rows
    df = df[[TEXT_COL, LABEL_COL]].dropna()
    df = df.drop_duplicates(subset=[TEXT_COL])
    df.columns = ["text", "label"]

    print("\nClass distribution:")
    print(df["label"].value_counts())

    # 80 / 10 / 10 stratified split
    train_df, temp_df = train_test_split(
        df, test_size=0.2, stratify=df["label"], random_state=42
    )
    val_df, test_df = train_test_split(
        temp_df, test_size=0.5, stratify=temp_df["label"], random_state=42
    )

    train_df.to_csv(f"{OUT_DIR}/train.csv", index=False)
    val_df.to_csv(f"{OUT_DIR}/val.csv", index=False)
    test_df.to_csv(f"{OUT_DIR}/test.csv", index=False)

    print(f"\nSaved: train={len(train_df)}  val={len(val_df)}  test={len(test_df)}")
    print(f"Files written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
