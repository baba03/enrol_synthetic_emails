import hashlib
import random
import re
from typing import Dict, List

FIRST_NAMES = [
    "Rajiv", "Amit", "Priya", "Neha", "Vikram", "Rohan", "Ananya",
    "Karan", "Meera", "Arjun", "Nisha", "Sanjay", "Deepak", "Ishita"
]
LAST_NAMES = [
    "Sharma", "Singh", "Malhotra", "Mehta", "Kapoor", "Iyer", "Gupta",
    "Verma", "Joshi", "Patel", "Nair", "Chopra", "Reddy", "Bose"
]
COMPANIES = [
    "Agriculture India Pvt. Ltd.", "Northstar Energy Services",
    "Meridian Industrial Group", "GreenField Holdings",
    "Summit Logistics Pvt. Ltd.", "BlueRiver Trading",
    "Horizon Infrastructure", "Crescent Capital Partners"
]
DOMAINS = ["agriindia.com", "northstarenergy.com", "meridian-group.com",
           "greenfieldholdings.com", "summitlogistics.in"]

def _rng(seed: str):
    return random.Random(int(hashlib.sha256(seed.encode()).hexdigest()[:12], 16))

def person_name(seed: str) -> str:
    r = _rng(seed)
    return f"{r.choice(FIRST_NAMES)} {r.choice(LAST_NAMES)}"

def company_name(seed: str) -> str:
    r = _rng(seed)
    return r.choice(COMPANIES)

def domain_for(seed: str) -> str:
    r = _rng(seed)
    return r.choice(DOMAINS)

def replacement_for(entity: str, label: str, seed: str) -> str:
    if label == "PERSON":
        return person_name(seed + entity)
    if label == "ORG":
        return company_name(seed + entity)
    if label in {"GPE", "LOC"}:
        return "New Delhi"
    if label == "PRODUCT":
        return "premium-grade agricultural products"
    if label == "EMAIL":
        name = person_name(seed + entity).lower().replace(" ", ".")
        return f"{name}@{domain_for(seed + entity)}"
    if label == "PHONE":
        return "+91-11-0000-0000"
    return f"[SYNTHETIC_{label}]"

def build_mapping(entities: List[Dict], seed: str = "consilio-demo") -> Dict[str, str]:
    mapping = {}
    for e in entities:
        key = e["text"]
        if key not in mapping:
            mapping[key] = replacement_for(key, e["label"], seed)
    return mapping

def apply_mapping(text: str, mapping: Dict[str, str]) -> str:
    # Longest first avoids partial replacement.
    for old, new in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
        text = re.sub(re.escape(old), new, text, flags=re.I)
    return text
