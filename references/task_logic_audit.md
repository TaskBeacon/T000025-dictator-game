# Task Logic Audit: Dictator Game

## 1. Paradigm Intent

- Task: `dictator_game` (unilateral allocation task).
- Research construct: prosocial vs self-interested allocation behavior when only the allocator (participant) decides the split.
- Manipulated factor in this implementation: stake/endowment size (`low_stake=10`, `medium_stake=20`, `high_stake=30` points).
- Response alternatives per trial:
  - `generous`: self 30% / other 70%
  - `equal`: self 50% / other 50%
  - `selfish`: self 90% / other 10%
- Key references used for paradigm-level grounding:
  - `W2128769827` (Camerer & Thaler, 1995)
  - `W3125258780` (Krupka & Weber, 2013)
  - `W2039329578` (Israel et al., 2009)

## 2. Block and Trial Workflow

### Block Structure

- Total blocks: `3`
- Trials per block: `24`
- Total trials: `72`
- Block scheduling: `Controller.prepare_block(...)` generates a shuffled sequence over stake conditions for each block.

### Trial State Machine (Implemented)

1. `stake_prompt`
   - Participant sees current endowment amount (`本轮分配金额：{stake} 分`).
   - Trigger: condition-specific prompt onset (`low_stake_prompt_onset`, `medium_stake_prompt_onset`, `high_stake_prompt_onset`).
   - Duration: `timing.stake_prompt_duration` (fallback-compatible with legacy `cue_duration`).
   - Response: none.
2. `pre_decision_fixation`
   - Participant sees central fixation (`+`) before decision.
   - Trigger: no dedicated marker in current map.
   - Duration: `timing.pre_decision_fixation_duration` (fallback-compatible with legacy `anticipation_duration`).
   - Response: none.
3. `decision`
   - Participant sees three allocation options and responds with `f` / `space` / `j`.
   - Trigger: condition-specific decision onset + response/timeout markers.
   - Duration: `timing.decision_duration`.
   - Timeout policy: no response within deadline is handled as `equal` choice.
4. `choice_feedback`
   - Participant sees immediate acknowledgment of selected allocation type (or timeout notice).
   - Trigger: `choice_feedback_onset` (fallback-compatible with legacy `decision_feedback_onset`).
   - Duration: `timing.choice_feedback_duration` (fallback-compatible with legacy `decision_feedback_duration`).
   - Response: none.
5. `outcome_feedback`
   - Participant sees trial split (self/other) and running totals.
   - Trigger: `outcome_feedback_onset`.
   - Duration: `timing.outcome_feedback_duration` (fallback-compatible with legacy `feedback_duration`).
   - Response: none.
6. `iti`
   - Participant sees fixation before next trial.
   - Trigger: `iti_onset`.
   - Duration: `timing.iti_duration`.
   - Response: none.

## 3. Condition Semantics

- `low_stake`
  - Endowment is fixed at `10` points.
  - Same three allocation rules are available; only the stake magnitude changes.
- `medium_stake`
  - Endowment is fixed at `20` points.
- `high_stake`
  - Endowment is fixed at `30` points.

Condition is shown to participants as a human-readable stake descriptor (`low stake` / `medium stake` / `high stake`) alongside the endowment amount.

## 4. Response, Timeout, and Scoring Rules

- Key mapping:
  - `f` -> `generous`
  - `space` -> `equal`
  - `j` -> `selfish`
- Timeout handling:
  - If no valid key is captured in decision window, `timed_out=True` and allocation is registered as `equal`.
- Payoff computation (`Controller.register_decision`):
  - `self_amount = round(stake * self_ratio)` (clamped to `[0, stake]`)
  - `other_amount = stake - self_amount`
- Running totals:
  - `self_total` and `other_total` are accumulated across trials and shown in block/end summaries.

## 5. Stimulus Layout Plan

- `stake_prompt_text`, `decision_panel`, `outcome_feedback`, and summary screens are centrally displayed text stimuli with `wrapWidth=980` and `font=SimHei`.
- Decision screen keeps three options in a fixed left/center/right text list to preserve stable key-option mapping.
- `fixation` is center-screen (`+`) and reused for pre-decision and ITI phases.

## 6. Trigger Plan

| Trigger | Code | Meaning |
|---|---:|---|
| `exp_onset` | 1 | Task start marker |
| `exp_end` | 2 | Task end marker |
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
| `choice_feedback_onset` | 52 | Choice-feedback onset |
| `outcome_feedback_onset` | 53 | Outcome feedback onset |
| `iti_onset` | 60 | ITI onset |

## 7. Inference Log

- Exact exposure durations were not directly specified in the selected paradigm-level papers; timing values are implementation choices marked as inferred runtime parameters.
- Fixed three-option split ratios (30/50/90% self-share) are an implementation-level operationalization of dictator allocations for repeatable behavioral sampling.
- Legacy MID-style labels (`cue/anticipation/target`) were removed from active runtime phases for paradigm-appropriate event semantics.
