import argparse, json, csv
from pathlib import Path
from .pipeline import generate

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--offline", action="store_true")
    args = p.parse_args()

    rows = []
    for path in sorted(Path(args.input_dir).glob("*.json")):
        email = json.loads(path.read_text(encoding="utf-8"))
        result = generate(email, offline=args.offline)
        v = result["validation"]
        rows.append({
            "file": path.name,
            "leakage_count": v["leakage"]["leakage_count"],
            "pii_count": v["pii"]["count"],
            "length_ratio": v["structure"]["length_ratio"],
            "quality_score": v["quality"]["score"],
        })

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else
                                ["file","leakage_count","pii_count","length_ratio","quality_score"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.output}")

if __name__ == "__main__":
    main()
