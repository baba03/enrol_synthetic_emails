from .pii import detect_entities, redact_for_llm
from .mapping import build_mapping, apply_mapping
from .prompt import SYSTEM_PROMPT, build_prompt
from .openrouter import generate_with_openrouter
from .validator import validate

def offline_generation(email: dict, transformed: str) -> str:
    subject = email.get("subject", "Business Discussion")
    body = email.get("body", "")
    return (
        f"Subject: Synthetic {subject}\n\n"
        "Dear Colleague,\n\n"
        "Please find the attached document for your review. "
        "The transaction and related commercial terms have been updated "
        "to reflect a different business context while preserving the "
        "original request and approval flow.\n\n"
        "Please let me know if you have any questions or require further details.\n\n"
        "Best regards,\n"
        "Rajiv Sharma\n"
        "Agriculture India Pvt. Ltd."
    )

def generate(email: dict, offline: bool = False) -> dict:
    source_text = (
        f"From: {email.get('from', '')}\n"
        f"To: {email.get('to', '')}\n"
        f"Date: {email.get('date', '')}\n"
        f"Subject: {email.get('subject', '')}\n\n"
        f"{email.get('body', '')}"
    )

    entities = detect_entities(source_text)
    safe_text = redact_for_llm(source_text, entities)
    mapping = build_mapping(entities)

    # Apply the mapping only to the local transformation context.
    transformed_context = apply_mapping(safe_text, mapping)

    if offline:
        synthetic = offline_generation(email, transformed_context)
    else:
        synthetic = generate_with_openrouter(
            SYSTEM_PROMPT,
            build_prompt(email, transformed_context)
        )

    validation = validate(email, synthetic, entities)

    return {
        "source": email,
        "detected_entities": entities,
        "mapping": mapping,
        "synthetic": synthetic,
        "validation": validation,
    }
