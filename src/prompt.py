SYSTEM_PROMPT = """You are generating synthetic enterprise email data for a privacy-conscious eDiscovery research prototype.

Your job is controlled transformation, not generic paraphrasing.

Preserve:
- the original business intent;
- sender/recipient relationship;
- approximate email length;
- paragraph structure;
- professional tone;
- transaction/request/approval logic;
- realistic corporate detail.

Transform:
- names and email identities;
- company names and domains;
- organizations;
- locations;
- products/services where needed;
- financial figures and currencies;
- dates and phone numbers;
- unique source-specific references.

Requirements:
1. The output must look like a genuine business email.
2. Do not mention Enron or the transformation process.
3. Do not copy unique source names or company names.
4. Keep entities internally consistent.
5. Do not add a disclaimer.
6. Return ONLY the synthetic email, with no analysis.
"""

def build_prompt(email: dict, transformed_context: str) -> str:
    return f"""Create a synthetic version of the following enterprise email.

SOURCE EMAIL METADATA:
Subject: {email.get('subject', '')}
Date: {email.get('date', '')}

TRANSFORMED CONTEXT:
{transformed_context}

Return a complete synthetic email including Subject, greeting, body and sign-off.
"""
