# Evaluation report

Prepared 2026-10-31. Status: implementation complete; **15 deterministic tests passed, 0 failed**. Live-model and live-Project tests: **NOT RUN**.

## Findings and changes

The supplied baseline already separates fictional immersion from real action claims and protects independence, competence, emotional range, and non-romantic defaults. Its likely weak points are retrieval-dependent short instructions, repeated identity rules, adjective-heavy speech guidance, and unspecified resolution of retaliation versus useful work. These are inspection findings, not measured model failures. See AUDIT.md for source-section mapping and CHANGELOG.md for preserved preferences and deliberate revisions.

The optimized system adds a retrieval-independent operational core, seven speech registers, concrete conflict and concession decisions, automatic work/conversation selection, recipient-appropriate drafts, explicit continuity layers, and a manual-update log. Examples are original authored illustrations, not sampled model results.

## Verification ledger

Executed from /workspace/Revy-Project:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/evaluate.py generate --model UNCONFIGURED --samples 3 --dry-run --out /tmp/revy-eval-dry-run-final
```

Results: **15 tests passed; 0 failed**. Dry run completed: **0/360 model requests executed**. The dry-run manifest is copied to output/DRY_RUN_MANIFEST.json; its status is DRY RUN, not a behavioral result. The first test pass exposed a missing document heading/empty parent section; those document-structure issues were corrected before the successful run. Both uploaded originals were also compared directly against the backup bytes. The suite checks original hashes, deliverable content, nonempty sections, exact substantive paragraph duplication, limited known contradictory-directive patterns, instruction length/reference fallback, registers, scenario schema/coverage, actual history lengths, API serialization/error handling with mocks, and strict score completeness/critical-failure aggregation. Semantic contradictions and fidelity are not exhaustively decidable by these checks.

Dataset: 60 distinct scenarios covering banter, conflict, administration, emotional nuance, canon, continuity, voice, resistance, and drift. The drift fixtures contain 10, 20, and 40 actual user/assistant pairs, with a seeded generic final assistant answer. They measure next-response recovery, not self-generated long-run stability.

## Live behavioral comparison: NOT RUN

No evaluation model API binding, endpoint, or model runtime is configured in this environment. Only variable names/presence and platform binding metadata were inspected; no credential values were read. The assistant's ability to write this kit is not a callable baseline/revised evaluation runtime. No model requests, output samples, fidelity scores, acceptance claims, or baseline-versus-revised improvements are reported.

| Evidence | Baseline | Revised |
| --- | --- | --- |
| Source/editorial inspection | Completed; risks documented | Completed; targeted revisions documented |
| Live model samples | NOT RUN | NOT RUN |
| Human behavioral scores | NOT RUN | NOT RUN |
| Live ChatGPT Project retrieval/voice/continuity | NOT RUN | NOT RUN |

The optional Python harness supplies identical synthetic contexts and full master reference availability to both variants, randomizes request ordering, records settings and prompt hashes, and generates empty scoring forms for actual completions. The rubric requires seven separate 1–5 scores, zero critical failures, mean thresholds, category thresholds, and review of preserved frequent natural profanity. Mock API responses and synthetic numeric ratings in unit tests are software test fixtures only, not persona evaluation evidence.

## Limits and next iteration

Broad canon foundations were retained from the user's reference; no new episode facts or externally sourced canon verification are claimed. Human reviewers must assess character fidelity, psychological interpretation, naturalness, and contextual profanity. Run the authorized paired API comparison, review failure clusters, then repeat representative cases inside the actual ChatGPT Project. Test voice with real audio/background conditions and continuity across separate conversations. Retrieval, memory, and UI-specific behavior can differ from the harness even if direct API scores pass. No Project was modified and no environment was published by this work.

## Follow-up review and fixes

The optional API harness now rejects truncated or abnormally finished completions. Its summary separates numerical threshold checks from overall acceptance, which remains pending human qualitative review. A regression test covers incomplete finish statuses and the aggregation test verifies the pending-review label. QUICK_START.md adds a plain-language installation path and manual Project checks. The full suite was rerun: **15 passed, 0 failed**. No live-model or live-Project tests were performed in this follow-up. The deployment prompt texts and original backup files are unchanged.
