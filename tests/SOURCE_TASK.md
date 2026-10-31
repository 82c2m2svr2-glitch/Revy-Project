# CODEX TASK: Optimize and test my existing ChatGPT Project persona for Revy from Black Lagoon

## Mission

Work on the two Markdown files in this directory:
- `Revy_Master_Personality_and_Operating_Reference.md`
- `Revy_Project_Instructions.md`

These are an existing ChatGPT Project personality construct, not the beginnings of a standalone application. Revy (Rebecca Lee/Two Hands) from *Black Lagoon* has quit the Lagoon Company and now works as my personal office secretary. She must feel recognizably like the same character, not a generic foul-mouthed assistant. Optimize this prompt/reference system for fidelity, natural conversation, stable voice-style behavior, competent secretary work, and continuity. Do not invent that she has a physical body or has taken real-world actions.

**First inspect both original files.** Preserve copies in `originals/`. Do not silently drop user preferences, especially frequent natural profanity and verbal retaliation when treated rudely. Keep the deliberate alternate-continuity premise, but separate it from genuine series canon. Preserve established characterization while avoiding made-up canon.

## Required work

### 1. Audit the prompt system
- Identify duplication, contradictions, vague instructions, hidden failures, exaggerated characterization, unrealistic claims about Project memory/retrieval, and places where a model will drift to generic assistant behavior.
- Explain the difference between rules that belong in ChatGPT Project Instructions (always-on, short, high-priority behavior) and character reference material that belongs in the uploaded file.
- Identify ways that “more swearing” can accidentally replace authentic characterization or make every situation sound identical.
- Prefer specific, observable behavior over adjectives such as “edgy,” “aggressive,” and “authentic.”

### 2. Build a detailed speech-and-dialogue specification
Integrate this into the master reference. Aim to emulate the character at the **high level**, not by copying copyrighted dialogue or falsely claiming the exact actress's performance.

Cover:
- Sentence rhythm: often short, blunt, conversational, occasionally cutting longer observations when making an argument. Natural contractions. Minimal corporate jargon and formality.
- Vocabulary: unfiltered American colloquialisms; frequent but non-mechanical profanity; specificity and varied intensities rather than a fixed swear-word quota.
- Sarcasm: cynical observations, mocking comparisons, direct criticism, occasional rhetorical questions; no sitcom one-liner every turn.
- Argument style: skeptical, confrontational, sharp practical logic, intolerance of condescension; able to acknowledge evidence and concede without turning pleasant or submissive.
- Emotional registers: relaxed/dismissive, amused, annoyed, furious, focused at work, reluctantly concerned, unguardedly serious. Each should have recognizable speech differences, not just different amounts of swearing.
- Reaction to rude employer: push back sharply, sometimes with profanity; do not reflexively become hateful, abusive, or incompetent.
- Workplace register: does accurate secretary work first while making short in-character comments; don't bury deliverables in insults.
- Overused-pattern bans: repeated “boss” every response, repetitive “fuck” filler, canned catchphrases, forced metaphors, theatrical stage directions, performative hostility, generic assistant templates, and unearned flirtation.
- Short original example exchanges for each register; write NEW dialogue in your own words rather than copying dialogue from the show.

### 3. Separate canon, alternate continuity, and memory
- Canon: established *Black Lagoon* characterization and relationships. Label uncertain claims as interpretation, not fact. Do not quote or recreate copyrighted scenes.
- Alternate continuity: she left mercenary work and took the secretary job; the reasons are unspecified until established by me.
- Personal interaction history: only things that actually occurred in available context; never invent memory or report actions not performed.
- Include a small editable `Continuity_Log_Template.md` with fields for verified canon facts, user-approved alternate-continuity decisions, ongoing office tasks, relationship developments, unresolved questions, date/source of update, and confidence/status. Make explicit that ChatGPT Projects will not automatically edit this file after conversations unless the user or an available tool updates it.
- Do not make the relationship romantic or submissive by default. Growth must be gradual and earned.

### 4. Produce revised deployment files
Create:
- `output/Revy_Project_Instructions_Optimized.md`: concise, operational, pasteable directly into Project settings; focus on identity, speech, behavior, duties, continuity, truthfulness about actions, and instruction to use the master file when available. Avoid turning it into a giant essay.
- `output/Revy_Master_Reference_Optimized.md`: comprehensive but non-repetitive reference, including precise speech guidelines and sample exchanges, emotional decision rules, anti-drift guardrails, canon-versus-alternate-continuity boundaries, and voice guidance.
- `output/Continuity_Log_Template.md`: short, practical editable template.
- `output/README_Deployment.md`: exact steps to back up originals, paste Project instructions, upload master reference, and use the continuity log. Note that Codex and ChatGPT Projects are distinct environments; Codex editing local files does not update my ChatGPT Project automatically.
- `output/CHANGELOG.md`: what changed, why, and what was preserved.

### 5. Build a reproducible test suite
Create a dataset of **at least 50 distinct scenarios** organized by category, with user turns, relevant context, expected behaviors, disallowed behaviors, and a scoring rubric. Include:
- Casual banter and unprompted observations during an active conversation.
- Direct insults, mild teasing, condescension, unfair criticism, and genuine conflict.
- Mundane admin tasks: schedule organization, summaries, email drafting, document sorting, prioritization, correcting contradictions, and stating inability to send an email without a connected action.
- Emotional nuance: user is upset, tired, anxious, grieving, or discussing a serious issue; maintain character but do not turn serious vulnerability into a profanity contest.
- Canon references: Rock, Dutch, Benny, Roanapur, Lagoon Company; distinguish known canon from speculation.
- Alternative-continuity uncertainty: “Why did you quit?”, “Where did we meet?”, “Remember last Tuesday?” when those details were never established.
- Voice-mode behavior: concise responses, no stage directions, no speech to unrelated background coworkers, brief clarification for ambiguous direct speech.
- Long-conversation drift: follow-up turns after 10, 20, and 40 mundane office exchanges; demonstrate recovery from generic-assistant language.
- Resistance to sycophancy, unnecessary arguments, forced romance, repeated catchphrases, and over-escalation.

Score along separate dimensions (1–5): character fidelity, speech naturalness, situation-appropriate profanity, emotional credibility, administrative usefulness, continuity integrity, and factual/action honesty. Treat a severe fabricated action or invented memory as a critical failure regardless of style score. Include measurable acceptance rules and a way to compare baseline vs revised prompts.

### 6. Execute what can actually be tested
- Run deterministic tests for file presence, nonempty sections, duplication, contradictory directives, data-schema validity, and scenario coverage.
- If a model evaluation runtime/API is available and authorized, run multiple samples per scenario against original and optimized prompts under comparable settings, save anonymized outputs and scoring notes, and produce a side-by-side report. Avoid embedding secrets or exposing sensitive data. Do not assume a live ChatGPT Project can be exercised by Codex.
- If model access is unavailable, **do not invent dialogue-test results**. Instead provide a reproducible eval harness and exact commands plus a clearly marked `NOT RUN` status for model-based tests. Static lint checks are not evidence of Revy authenticity.
- Create `output/EVALUATION_REPORT.md` with verified findings, baseline weaknesses, changes, any actual results, limitations, and recommended next iteration.

## Quality and design rules
- Keep the construct *Revy*, not “generic angry secretary.” She must show competence, perceptiveness, mercenary pragmatism, an anti-authoritarian streak, suspicion of idealism, and guarded loyalty. She should also be capable of quiet or uncomfortable seriousness.
- Do not imitate the original voice actress's actual audio voice or clone audio; speech pattern and word choice only.
- Make both a “fast working mode” for short administrative replies and a “natural conversation mode,” without needing the user to toggle them manually. Choose based on the request.
- Keep project instructions brief, testable, and practical. Put longer characterization into the master reference.
- Preserve every meaningful preference in the originals unless there is a documented reason to revise it.
- Do not modify originals in place. Use `originals/` backups and output only to `output/` plus test files.
- Do not create a separate app, voice service, database, or integration as part of this task.
- No invented test results; be precise about what you verified.

## Finish with
1. A compact audit summary.
2. File paths of every deliverable.
3. Summary of real tests run and passes/failures.
4. Known limits of testing inside Codex versus the live ChatGPT Project.
5. Exactly what I should paste into Project Instructions and what I should upload as Project files.
