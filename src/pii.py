import re
from dataclasses import dataclass, asdict
from typing import List, Dict

@dataclass
class Entity:
    label: str
    text: str
    start: int
    end: int
    source: str

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")
MONEY_RE = re.compile(
    r"(?<!\w)(?:[$€£₹]\s?\d[\d,]*(?:\.\d+)?\s*(?:million|billion|m|bn|k)?|"
    r"\d[\d,]*(?:\.\d+)?\s*(?:million|billion)\s*(?:dollars|USD|euros|EUR|rupees|INR)?)(?!\w)",
    re.I
)
URL_RE = re.compile(r"\b(?:https?://|www\.)\S+", re.I)
DATE_RE = re.compile(
    r"\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b",
    re.I
)

def regex_entities(text: str) -> List[Entity]:
    entities = []
    patterns = [
        ("EMAIL", EMAIL_RE),
        ("PHONE", PHONE_RE),
        ("MONEY", MONEY_RE),
        ("URL", URL_RE),
        ("DATE", DATE_RE),
    ]
    for label, pattern in patterns:
        for m in pattern.finditer(text):
            entities.append(Entity(label, m.group(0), m.start(), m.end(), "regex"))
    return entities

def spacy_entities(text: str) -> List[Entity]:
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        return []
    doc = nlp(text)
    keep = {"PERSON", "ORG", "GPE", "LOC", "MONEY", "DATE", "PRODUCT", "EVENT"}
    return [
        Entity(ent.label_, ent.text, ent.start_char, ent.end_char, "spacy")
        for ent in doc.ents if ent.label_ in keep
    ]

def detect_entities(text: str) -> List[Dict]:
    entities = regex_entities(text) + spacy_entities(text)
    # Deduplicate exact spans.
    seen = set()
    output = []
    for e in sorted(entities, key=lambda x: (x.start, x.end)):
        key = (e.label, e.text.lower(), e.start, e.end)
        if key not in seen:
            seen.add(key)
            output.append(asdict(e))
    return output

def redact_for_llm(text: str, entities: List[Dict]) -> str:
    """Replace high-risk regex PII with typed placeholders before any external API call."""
    replacements = []
    for e in entities:
        if e["label"] in {"EMAIL", "PHONE", "URL"}:
            replacements.append((e["start"], e["end"], f"[{e['label']}]"))
    for start, end, token in sorted(replacements, reverse=True):
        text = text[:start] + token + text[end:]
    return text
