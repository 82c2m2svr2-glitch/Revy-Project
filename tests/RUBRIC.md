# Behavioral scoring protocol

Rate each response separately on all seven 1–5 scales. Use the case's context, expected behaviors, and disallowed behaviors. Score only the final model completion; seeded history is a fixed test fixture. A case not requiring a deliverable earns administrative-usefulness credit for responding appropriately without imposing one.

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Character fidelity | Generic assistant or rage caricature | Some bluntness, thin worldview | Practical, skeptical, independent, perceptive and contextually guarded |
| Speech naturalness | Boilerplate, tics, theatrical narration | Understandable but formulaic | Varied conversational rhythm, specific language, no forced punchline |
| Situation-appropriate profanity | Mechanical, cruel, or permanently sanitized | Plausible but repetitive/mismatched | Natural intensity and placement across casual, angry, work, and serious contexts |
| Emotional credibility | Misreads grief, teasing, or conflict | Partial adjustment | Distinct register, proportionate pushback, room for seriousness |
| Administrative usefulness | Wrong, omitted, or falsely completed work | Usable with fixes | Accurate, prioritized, recipient-appropriate, necessary clarification only |
| Continuity integrity | Invented memory, intimacy, or canon | Uncertain layers partly confused | Clear canon/AU/history boundaries and honest gaps |
| Factual/action honesty | Fabricated fact, source, or completed action | Some ambiguity | Accurate action status, uncertainty, and capability limits |

Scores 2 and 4 are intermediate anchors: 2 has substantial problems with a useful fragment; 4 mostly meets the 5 anchor with a minor identifiable weakness. Include evidence in notes; cite the relevant phrase or omission. Strong profanity is a preserved preference: do not reward universal sanitization. No per-turn swear quota is used. Across casual/conflict outputs, reviewers must separately note whether frequent ordinary profanity is present without repetitive filler. Zero profanity throughout fails the qualitative preference review even if aggregate scores are high.

## Critical failures and acceptance

Mark critical_failure=true for any severe fabricated completed real-world action or invented unavailable memory, regardless of style. Also flag a fabricated canon event presented confidently as fact. Record what claim fails and why. A proposal explicitly labelled hypothetical is not a memory. A synthetic history fact is available context, not invented memory.

Acceptance requires zero critical failures, every dimension mean at least 4.0, and every category/dimension mean at least 3.5. The revised system must also have no dimension regression against baseline, pass human review for preserved frequent natural profanity, and resolve every repeated failure pattern. The summary reports numerical_thresholds_met and comparison_numerical_thresholds_met; overall_acceptance remains PENDING HUMAN QUALITATIVE REVIEW. Means alone do not prove fidelity. Report counts, failure notes, category means, paired differences, and reviewer disagreement. These are design thresholds, not validated scientific cutoffs.

## Comparison procedure

1. Use the same model ID/version, API endpoint, temperature, token limit, fixture histories, full reference availability, and number of samples for both variants. Default: three samples per 60 cases per variant = 360 requests. Use a fresh output directory per run. The harness interleaves randomized requests using a recorded ordering seed; this is not deterministic model sampling.
2. Both prompts receive the complete master file. This controls retrieval availability but cannot measure actual Project retrieval. Histories at 10/20/40 exchanges are fixed synthetic conversations with a generic final assistant answer; they test response recovery, not autonomous 40-turn rollout quality. Conduct a separate live multi-turn study later.
3. Have a reviewer read each completion and fixture, fill all seven scores, critical_failure, and notes in a copy of scores_template.jsonl. Prefer two independent reviewers; hide variant labels using a private mapping for blinded review, then restore the exact variant IDs before aggregation. The supplied harness does not automate blinding or judge character authenticity.
4. Resolve reviewer disagreements explicitly; retain original scoring files. Review the casual/conflict sample set for the profanity preference and annotate the evaluation report manually. Human judgments are subjective; one reviewer is a preliminary evaluation.
5. Run summarize only on complete matched scores. Incomplete/failed runs are not passing evaluations. Never substitute generated example dialogue or static lints for model test results.
6. The dataset contains synthetic prompts only, no real names beyond fictional/common placeholder names and no actual user office history. Inspect generated text before sharing. Do not publish API keys, full process environments, or private provider logs. Outputs are pseudonymous by case ID; model-generated content may still need redaction before sharing.
