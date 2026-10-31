# Deploying the Revy prompt system

For a plain-language installation checklist and sample checks, start with QUICK_START.md. You do not need to run Python or use an API to install this prompt system.

These are ChatGPT Project documents, not a standalone application. Codex edits local files; it does not update your ChatGPT Project. No voice service, database, or integration is required.

## 1. Preserve and review

The two uploaded originals are backed up byte-for-byte in ../originals/. Their SHA-256 hashes are recorded in ../tests/original_hashes.json. Before deployment, also export or copy your current live Project Instructions and current Project files to a dated backup, since those may differ from these uploaded versions. Review AUDIT.md and CHANGELOG.md. EVALUATION_REPORT.md distinguishes actual deterministic checks from unrun model tests.

## 2. Paste instructions

Open your ChatGPT Project settings and replace its Instructions with the **entire contents** of Revy_Project_Instructions_Optimized.md. Do not paste the master reference, evaluation report, or source task into the Instructions field. Save using the controls provided by your current ChatGPT interface. The local file is under 8,000 characters; interface limits can change.

## 3. Upload reference and log

Upload Revy_Master_Reference_Optimized.md as a Project file, retaining that exact filename because the instructions refer to it. Upload a filled copy of Continuity_Log_Template.md as the current continuity log. Keep canon, alternate continuity, and actual office task records distinct. Leave unknown hiring/meeting/departure details unset. Remove or archive superseded Project reference versions so they do not compete in retrieval. Keep originals outside the active reference set for rollback.

Do not upload AUDIT.md, CHANGELOG.md, EVALUATION_REPORT.md, source briefs, scenario data, or evaluation scripts as character guidance. They are review/testing material, not deployment prompts.

## 4. Maintain continuity and validate in the Project

After significant conversations, request a proposed dated continuity entry, verify it, then update/re-upload the log yourself unless a connected authorized tool actually updates it. Ordinary conversations do not automatically edit uploaded files. Project memory and file retrieval are not guaranteed and differ from direct API evaluation.

Start a new Project chat and try representative cases: a rude but actionable request, a polite email draft, grief without a joke, a question about the unset first meeting, and an unavailable email send. Confirm voice behavior in the actual voice interface, including background speech. These are manual checks to perform, not results already obtained. Keep one current log and record dates/sources for updates.

## 5. Reproduce local checks

From /workspace/Revy-Project (Python 3.10+; standard library only):

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/evaluate.py generate --model YOUR_MODEL_ID --samples 3 --dry-run --out /tmp/revy-eval-dry-run-new
```

The output directory must not exist. A dry run validates fixture/prompt loading and request planning; it makes zero model calls and creates no dialogue scores. Static tests are not evidence of character authenticity. See ../tests/RUBRIC.md for acceptance and review instructions.

## 6. Optional live model comparison

Use an authorized HTTPS Chat Completions-compatible API supporting system messages, temperature, and max_tokens. Supply REVY_EVAL_ENDPOINT (full HTTPS completion URL) and REVY_EVAL_API_KEY through secure environment settings; do not put a key in a command, source file, or chat. Network policy must permit that provider. No credential or network configuration is changed by this kit. If the provider needs a different request schema, adapt the harness in a separate change rather than assuming compatibility.

```bash
python3 tests/evaluate.py generate --model YOUR_MODEL_ID --samples 3 --out /tmp/revy-eval-live-01
```

This makes 360 billable requests with synthetic scenarios, the supplied prompt texts, and fixed histories. Check budget and provider limits before running. Truncated or abnormally finished completions fail the run rather than becoming scored samples. There is no automatic retry; failed runs preserve partial results and fail visibly. The manifest records prompt/dataset hashes and settings. It does not retain credentials. Raw outputs use case IDs, not personal office data; inspect/redact generated content before sharing.

Copy scores_template.jsonl to scores_reviewed.jsonl in the run directory, then fill every dimension, critical_failure, and evidence note using the rubric. Do not manufacture ratings for a run that never executed. Generate the comparison:

```bash
python3 tests/evaluate.py summarize --scores /tmp/revy-eval-live-01/scores_reviewed.jsonl --out /tmp/revy-eval-live-01/comparison.json
```

Numerical threshold results are not overall approval. Review qualitative profanity preference separately and record it with the report. Comparing full master text by API does not establish ChatGPT Project retrieval, cross-chat memory, voice speaker recognition, or audio performance. To roll back, restore your dated live Instructions backup and original master reference, removing the optimized active copies.
