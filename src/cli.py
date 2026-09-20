import argparse
import json
from pathlib import Path
from .pipeline import generate

def main():
    parser = argparse.ArgumentParser(description="Generate a synthetic corporate email.")
    parser.add_argument("--input", required=True, help="Input JSON email.")
    parser.add_argument("--output", required=True, help="Output JSON path.")
    parser.add_argument("--offline", action="store_true", help="Use deterministic offline generation.")
    args = parser.parse_args()

    email = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = generate(email, offline=args.offline)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Saved result to {args.output}")

if __name__ == "__main__":
    main()
