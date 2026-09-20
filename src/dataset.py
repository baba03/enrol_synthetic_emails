import argparse
import json
import re
from pathlib import Path
import pandas as pd

def pick_col(df, candidates):
    lower = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lower:
            return lower[candidate.lower()]
    return None

def profile(path, sample_size=2000):
    df = pd.read_csv(path, nrows=sample_size)
    body_col = pick_col(df, ["body", "message", "content", "text", "email"])
    subject_col = pick_col(df, ["subject", "subject_line"])
    sender_col = pick_col(df, ["from", "sender", "from_email"])
    to_col = pick_col(df, ["to", "recipient", "recipients"])
    date_col = pick_col(df, ["date", "timestamp", "sent_date"])

    result = {
        "rows_sampled": len(df),
        "columns": list(df.columns),
        "missingness": df.isna().mean().round(4).to_dict()
    }

    if body_col:
        lengths = df[body_col].fillna("").astype(str).str.len()
        result["body"] = {
            "column": body_col,
            "mean_chars": round(float(lengths.mean()), 2),
            "median_chars": round(float(lengths.median()), 2),
            "p95_chars": round(float(lengths.quantile(.95)), 2),
        }
    if subject_col:
        lengths = df[subject_col].fillna("").astype(str).str.len()
        result["subject"] = {
            "column": subject_col,
            "mean_chars": round(float(lengths.mean()), 2),
            "median_chars": round(float(lengths.median()), 2),
        }
    if sender_col:
        result["unique_senders"] = int(df[sender_col].nunique(dropna=True))
    if to_col:
        result["unique_recipients_or_values"] = int(df[to_col].nunique(dropna=True))
    if date_col:
        parsed = pd.to_datetime(df[date_col], errors="coerce")
        result["date_range"] = {
            "min": str(parsed.min()),
            "max": str(parsed.max()),
            "valid_dates": int(parsed.notna().sum())
        }

    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--sample-size", type=int, default=2000)
    args = parser.parse_args()

    result = profile(args.input, args.sample_size)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
