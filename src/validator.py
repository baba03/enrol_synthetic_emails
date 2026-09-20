import re
from typing import Dict, List

def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower()).strip()

def leakage_check(source_text: str, synthetic_text: str, source_entities: List[Dict]) -> Dict:
    syn = normalize(synthetic_text)
    leaked = []
    for e in source_entities:
        value = normalize(e["text"])
        if len(value) >= 3 and value in syn:
            leaked.append(e["text"])
    return {
        "leakage_count": len(set(leaked)),
        "leaked_entities": sorted(set(leaked)),
        "passed": len(leaked) == 0
    }

def pii_check(text: str) -> Dict:
    patterns = {
        "email": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "phone": r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)",
        "url": r"\b(?:https?://|www\.)\S+",
    }
    findings = {}
    total = 0
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text, re.I)
        findings[name] = sorted(set(matches))
        total += len(matches)
    return {"count": total, "findings": findings, "passed": total == 0}

def structural_check(source: str, synthetic: str) -> Dict:
    def paragraphs(x): return [p.strip() for p in re.split(r"\n\s*\n", x) if p.strip()]
    def sentences(x): return max(1, len(re.findall(r"[.!?]+", x)))
    sl, tl = len(source), len(synthetic)
    ratio = tl / sl if sl else 0
    return {
        "source_chars": sl,
        "synthetic_chars": tl,
        "length_ratio": round(ratio, 3),
        "paragraphs_source": len(paragraphs(source)),
        "paragraphs_synthetic": len(paragraphs(synthetic)),
        "sentence_count_source": sentences(source),
        "sentence_count_synthetic": sentences(synthetic),
        "length_reasonable": 0.45 <= ratio <= 1.8
    }

def quality_heuristic(text: str) -> Dict:
    markers = ["dear ", "thanks", "thank you", "regards", "best regards", "subject:"]
    low = text.lower()
    present = [m for m in markers if m in low]
    score = min(5, 1 + len(present))
    return {
        "score": score,
        "max_score": 5,
        "markers_found": present,
        "note": "Heuristic only; production evaluation should include human review and semantic/LLM-based evaluation."
    }

def validate(source_email: dict, synthetic_email: str, source_entities: List[Dict]) -> Dict:
    source_body = source_email.get("body", "")
    return {
        "leakage": leakage_check(source_body, synthetic_email, source_entities),
        "pii": pii_check(synthetic_email),
        "structure": structural_check(source_body, synthetic_email),
        "quality": quality_heuristic(synthetic_email),
    }
