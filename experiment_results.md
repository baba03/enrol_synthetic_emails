# Experiment Results and Findings

> This file is a submission template. Replace the placeholders with measurements from the actual Enron run before submitting.

## 1. Data analysis

Dataset sample size: **[N]**

Key observations:
- Median body length: **[X] characters**
- Mean body length: **[X] characters**
- Median subject length: **[X] characters**
- Unique senders in sample: **[X]**
- Date range: **[start] to [end]**
- Common patterns observed: approvals, requests, transactions, meetings, operational updates and relationship-driven business communication.

## 2. Synthesis process

The pipeline first detects PII and named entities locally. High-risk contact identifiers such as email addresses and phone numbers are replaced before external model interaction. A deterministic mapping layer creates consistent synthetic entities. The LLM then transforms the email while preserving intent, structure and professional style.

## 3. Validation

| Metric | Result |
|---|---:|
| Emails synthesized | [N] |
| Source entity leakage | [N] |
| PII findings | [N] |
| Average length ratio | [X] |
| Average structural score | [X] |
| Average realism score | [X/5] |

## 4. Challenges

### Entity consistency
A naive LLM rewrite can introduce multiple names for the same person. A deterministic mapping is therefore created before generation.

### PII leakage
The model can repeat source-specific identifiers. The prototype performs a post-generation leakage check and keeps the privacy-sensitive detection local where possible.

### Semantic drift
Over-aggressive rewriting can change the purpose of the email. The prompt explicitly asks the model to preserve business intent and relationship structure.

### Evaluation
"Looks realistic" is subjective. The prototype therefore combines deterministic checks with a future path toward semantic similarity and human/LLM evaluation.

## 5. Findings

The experiment should be interpreted as a feasibility prototype rather than a production privacy guarantee. The strongest evidence should come from measured leakage rates, structural distribution comparisons and representative qualitative examples.
