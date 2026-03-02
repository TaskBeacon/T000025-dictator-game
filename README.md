# Dictator Game

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Dictator Game |
| Version | v0.2.2-dev |
| URL / Repository | https://github.com/TaskBeacon/T000025-dictator-game |
| Short Description | Three-option allocation decisions (generous/equal/selfish) under different stake levels. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This task implements a standard Dictator Game. On each trial, participants choose one of three allocation rules (generous, equal, selfish) for a given stake amount. Choices directly determine self and other payoffs without partner response stages.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Schedule trials | `Controller.prepare_block(...)` generates balanced low/medium/high-stake trial sequences. |
| 2. Execute trials | `BlockUnit(...).run_trial(...)` executes stake prompt, decision, and outcome stages. |
| 3. Block summary | Allocation-type proportions and block-level earnings are shown. |
| 4. Final summary | Cumulative self/other totals are reported at task end. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Stake prompt | Stake amount for current trial is shown. |
| Pre-decision fixation | Fixation before decision panel. |
| Allocation decision | Three-choice allocation panel is presented and response is captured. |
| Decision confirmation | Selected rule (or timeout fallback) is shown. |
| Outcome feedback | Trial and cumulative self/other amounts are shown. |
| Inter-trial interval | Fixation interval before next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Stake schedule | Balances low/medium/high stake conditions. |
| Rule mapping | Maps chosen allocation type to `self_amount` and `other_amount`. |
| Totals | Updates cumulative self and other payoffs. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `stake_prompt` | Stake prompt stage. |
| `pre_decision_fixation` | Fixation before allocation choice. |
| `decision` | Three-option allocation decision stage. |
| `choice_feedback` | Decision confirmation stage. |
| `outcome_feedback` | Outcome feedback stage. |
| `iti` | ITI stage. |

## 3. Configuration Summary

### a. Subject Info

| Field | Description |
|---|---|
| `subject_id` | Participant identifier. |
| `subname` | Participant name token. |
| `age` | Participant age. |
| `gender` | Participant gender. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `stake_prompt_text` | text | Stake prompt shown before choice. |
| `decision_panel` | text | Three-option allocation panel. |
| `decision_*` | text | Choice confirmation screens. |
| `outcome_feedback` | text | Trial and cumulative payoff summary. |
| `fixation` | text | Central fixation marker. |

### d. Timing

| Phase | Duration |
|---|---|
| stake_prompt | 0.6 s |
| pre_decision_fixation | 0.5 s |
| decision | 2.2 s |
| choice_feedback | 0.5 s |
| outcome_feedback | 1.0 s |
| iti | 0.8 s |

## 4. Methods (for academic publication)

Participants acted as allocators in a repeated Dictator Game. For each stake level, they selected one of three allocation rules that determined how much money they kept versus gave to the other party.

The task emphasizes unilateral social allocation behavior without reciprocal feedback. Trial-level logs include stake condition, selected rule, response timing, self payoff, other payoff, and cumulative totals.

The implementation supports `human`, `qa`, and `sim` modes with consistent trial flow and responder context annotations.
