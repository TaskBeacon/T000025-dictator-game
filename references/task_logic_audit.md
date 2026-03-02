# Task Logic Audit: Dictator Game

## 1. Paradigm Intent

- Task: `dictator_game`.
- Research construct: unilateral allocation preferences (prosocial vs self-serving) under stake manipulation.
- Manipulated factor in this implementation: stake condition (`low_stake`, `medium_stake`, `high_stake`).
- Core decision: participant chooses one fixed split option each trial.

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `3` blocks x `24` trials.
- QA/sim profiles: `1` block x `9` trials (mechanism-complete short profile).
- Block scheduling: controller shuffles condition assignments within each block.

### Trial State Machine

1. `stake_prompt`
- Display current stake/endowment and prompt participant to prepare for allocation decision.
- Duration: `timing.stake_prompt_duration`.
- Trigger: condition-specific prompt onset.

2. `pre_decision_fixation`
- Neutral fixation between prompt and response window.
- Duration: `timing.pre_decision_fixation_duration`.

3. `decision`
- Display three-way split options and collect key response.
- Duration: `timing.decision_duration`.
- Triggers: condition-specific decision onset, response marker, timeout marker.

4. `choice_feedback`
- Brief post-choice acknowledgement (`generous/equal/selfish/timeout`).
- Duration: `timing.choice_feedback_duration`.
- Trigger: `choice_feedback_onset`.

5. `outcome_feedback`
- Display self/other allocations and running totals.
- Duration: `timing.outcome_feedback_duration`.
- Trigger: `outcome_feedback_onset`.

6. `inter_trial_interval`
- Fixation before the next trial.
- Duration: `timing.iti_duration`.
- Trigger: `iti_onset`.

## 3. Condition Semantics

- `low_stake`: endowment `10`.
- `medium_stake`: endowment `20`.
- `high_stake`: endowment `30`.

Condition affects stake magnitude only; response options and timing structure remain constant.

## 4. Response and Scoring Rules

- Key mapping:
- `f` -> `generous`
- `space` -> `equal`
- `j` -> `selfish`

- Allocation profiles:
- `generous`: self ratio `0.3`
- `equal`: self ratio `0.5`
- `selfish`: self ratio `0.9`

- Timeout rule:
- If no valid key is captured by decision deadline, choice is registered as `equal` and `timed_out=True`.

- Outcome computation:
- `self_amount = round(stake * self_ratio)` (clamped to `[0, stake]`)
- `other_amount = stake - self_amount`
- `self_total` and `other_total` accumulate across trials.

## 5. Stimulus Layout Plan

- All participant-facing text is defined in YAML (`stimuli.*`) for localization portability.
- `decision_panel` presents three options in stable left/center/right textual order aligned with key mapping.
- Fixation is center-screen and reused across neutral intervals.
- Outcome and block summary screens use centered multiline text with wrap width control.

## 6. Trigger Plan

| Trigger | Code | Meaning |
|---|---:|---|
| `exp_onset` | 1 | Experiment start |
| `exp_end` | 2 | Experiment end |
| `block_onset` | 10 | Block start |
| `block_end` | 11 | Block end |
| `low_stake_prompt_onset` | 20 | Low-stake prompt onset |
| `medium_stake_prompt_onset` | 21 | Medium-stake prompt onset |
| `high_stake_prompt_onset` | 22 | High-stake prompt onset |
| `low_stake_decision_onset` | 30 | Low-stake decision onset |
| `medium_stake_decision_onset` | 31 | Medium-stake decision onset |
| `high_stake_decision_onset` | 32 | High-stake decision onset |
| `decision_response` | 50 | Decision response captured |
| `decision_timeout` | 51 | Decision timeout |
| `choice_feedback_onset` | 52 | Choice feedback onset |
| `outcome_feedback_onset` | 53 | Outcome feedback onset |
| `iti_onset` | 60 | ITI onset |

## 7. Architecture Decisions (Auditability)

- `main.py` uses a single mode-aware execution flow (`human|qa|sim`) with shared setup order.
- `src/run_trial.py` phase labels are aligned to dictator-game state names (`stake_prompt`, `decision`, `choice_feedback`, `outcome_feedback`) and no MID template labels remain.
- Participant-facing text remains config-driven (`stim_bank.get_and_format(...)`) rather than code literals.
- `decision` unit label is retained for compatibility with QA/sim artifact contracts (`decision_response`).

## 8. Inference Log

- Selected papers define dictator-game principles but do not prescribe exact display durations; timing values are inferred implementation parameters.
- The three discrete split options (30/50/90% self-share) are an inferred operationalization for repeated-trial behavioral sampling.
- Stake levels (`10/20/30`) are inferred implementation tiers for controlled context variation.