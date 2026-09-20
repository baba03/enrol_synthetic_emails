# Experiment Plan

## Objective

Build a proof-of-concept pipeline that converts Enron emails into realistic synthetic corporate emails while de-identifying the source. The synthetic data should preserve useful enterprise-email characteristics such as business intent, structure, tone, relationships and complexity, while replacing source-specific people, organizations, contact details, locations and commercial context.

## Research / technique selection

The prototype combines:
- pandas for rapid dataset profiling;
- regex for deterministic detection of emails, phones, URLs, dates and monetary values;
- optional spaCy NER for PERSON, ORG, GPE/LOC, PRODUCT, DATE and related entities;
- deterministic entity mapping to maintain consistency;
- an OpenRouter-hosted LLM for controlled transformation;
- automated leakage, PII, structure and heuristic quality checks.

The central design choice is to separate **privacy transformation** from **language generation**: obvious PII is detected locally before any LLM call, and the LLM receives a transformed context rather than raw contact identifiers.

## Methodology

1. Profile a sample of the Enron dataset.
2. Select a small experiment set of representative emails.
3. Detect PII and named entities locally.
4. Build a deterministic replacement map.
5. Apply replacements to a safe transformation context.
6. Ask the LLM to preserve intent, structure, tone and approximate complexity while creating a new company/person context.
7. Validate source-entity leakage and PII leakage.
8. Compare source and synthetic length/paragraph/sentence distributions.
9. Review a small sample manually for realism and semantic consistency.
10. Record failures and iterate the prompt/mapping strategy.

## Success criteria

- No obvious source PII in synthetic output.
- Source-specific company/person names are not reproduced.
- Business intent is retained.
- Entity references remain internally consistent.
- Synthetic emails have realistic corporate structure and tone.
- The approach is reproducible and explainable.

A production implementation would require stronger privacy guarantees, broader NER coverage, adversarial leakage testing, human review, and formal privacy evaluation.
