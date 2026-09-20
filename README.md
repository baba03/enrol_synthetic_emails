# Synthetic Corporate Email Generator

A rapid-prototyping project for the Consilio Labs .

## Objective

Transform an Enron email into a realistic synthetic corporate email while:

- removing/de-identifying identifiable information from the source;
- changing people, companies, domains, locations, products and financial context;
- preserving the original business intent, email structure, tone and approximate complexity;
- validating that source identities do not leak into the synthetic output.

The assessment asks for a prototype that accepts an Enron email and returns a synthetic email, with emphasis on process, experimentation and validation.

## Architecture

```text
Enron email
    |
    v
Parsing / normalization
    |
    v
Local PII + entity detection
    |
    v
Deterministic entity mapping
    |
    v
LLM transformation through OpenRouter
    |
    v
Synthetic email
    |
    +--> PII leakage check
    +--> source-entity leakage check
    +--> structural checks
    +--> consistency checks
    +--> heuristic quality checks
    |
    v
JSON result + CSV experiment summary
```

## Important security note

Never hard-code the assessment API key into the repository.

Set it as an environment variable:

```bash
export OPENROUTER_API_KEY="YOUR_KEY_HERE"
```

On Windows PowerShell:

```powershell
$env:OPENROUTER_API_KEY="YOUR_KEY_HERE"
```

Do not commit `.env`, API keys, or raw private datasets.

## Project structure

```text
enron_synthetic_email_project/
├── data/
│   └── sample/
│       └── sample_email.json
├── notebooks/
│   └── experiment_walkthrough.ipynb
├── outputs/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── pii.py
│   ├── mapping.py
│   ├── prompt.py
│   ├── openrouter.py
│   ├── validator.py
│   ├── pipeline.py
│   ├── dataset.py
│   └── cli.py
├── experiment_plan.md
├── experiment_results.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional local NER support:

```bash
python -m spacy download en_core_web_sm
```

The prototype still works without the spaCy model because regex and lightweight heuristics are included.

## Run a single email

```bash
python -m src.cli \
  --input data/sample/sample_email.json \
  --output outputs/synthetic_result.json
```

## Run the local/offline demo

This does not require an API key:

```bash
python -m src.cli \
  --input data/sample/sample_email.json \
  --output outputs/demo_result.json \
  --offline
```

Offline mode demonstrates the full pipeline but uses a deterministic template instead of an LLM. It is included so the repository can be executed immediately.

## Run with OpenRouter

```bash
export OPENROUTER_API_KEY="YOUR_KEY_HERE"

python -m src.cli \
  --input data/sample/sample_email.json \
  --output outputs/openrouter_result.json
```

The default model is configurable through `OPENROUTER_MODEL`.

## Dataset analysis

The dataset helper supports common CSV layouts. For a CSV:

```bash
python -m src.dataset \
  --input /path/to/emails.csv \
  --output outputs/dataset_profile.json \
  --sample-size 2000
```

It reports useful characteristics such as:

- number of rows;
- missingness;
- average body length;
- subject length;
- sender/recipient counts;
- date coverage;
- basic entity/PII counts.

## Experimental design

For a rapid assessment, use:

1. 500–2,000 emails for initial profiling.
2. 50–100 emails for the first synthesis experiment.
3. Compare source vs synthetic:
   - PII/entity leakage;
   - length and paragraph preservation;
   - subject/body consistency;
   - entity consistency;
   - semantic intent preservation;
   - LLM/heuristic realism score.

The point is not to claim perfect privacy from heuristics. The prototype should explicitly state its validation limitations and show how a production version would add stronger automated privacy testing and human review.

## Expected output

The output JSON contains:

```json
{
  "source": {...},
  "detected_entities": [...],
  "mapping": {...},
  "synthetic": {...},
  "validation": {...}
}
```

## explanation

A concise explanation:

> I treated the problem as controlled data transformation rather than simple paraphrasing. I first profiled the Enron distribution and locally detected PII and entities. I then created a consistent replacement map and used an LLM to transform the email while preserving intent, structure and business realism. Finally, I validated the result for source-entity leakage, PII leakage, structural preservation and consistency. This makes the experiment measurable instead of relying only on visual inspection.
