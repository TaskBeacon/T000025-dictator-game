# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task.conditions | `task.conditions` | `['low_stake', 'medium_stake', 'high_stake']` | W2128769827 | Dictator paradigm uses repeated allocation trials; this implementation samples across stake contexts. | inferred | Three stake levels operationalize context variation while preserving unilateral allocation logic. |
| task.trials | `task.total_blocks`, `task.trial_per_block`, `task.total_trials` | `3 x 24 = 72` (human), `1 x 9 = 9` (qa/sim) | W2128769827 | Repeated one-shot allocation decisions are standard in dictator-game batteries. | inferred | QA/sim shortened for fast gate execution. |
| task.keys | `task.key_list` | `['f', 'space', 'j']` | W2128769827 | Paper does not fix keyboard mapping; mapping is implementation-defined. | inferred | Mapping is taught in instruction text and mirrored in decision panel. |
| timing.stake_prompt | `timing.stake_prompt_duration` | `0.6s` human, `0.3s` qa/sim | W2128769827 | No fixed exposure duration reported for this display stage. | inferred | Prompt introduces stake before choice. |
| timing.pre_decision_fixation | `timing.pre_decision_fixation_duration` | `0.5s` human, `0.3s` qa/sim | W2128769827 | No fixed fixation duration specified. | inferred | Neutral pre-decision interval. |
| timing.decision_window | `timing.decision_duration` | `2.2s` human, `0.7s` qa/sim | W2128769827 | Decision is participant-paced within a bounded response window in computerized implementations. | inferred | Timeout is recorded and mapped to default allocation policy. |
| timing.choice_feedback | `timing.choice_feedback_duration` | `0.5s` human, `0.3s` qa/sim | W2128769827 | No exact value reported. | inferred | Immediate post-choice acknowledgement. |
| timing.outcome_feedback | `timing.outcome_feedback_duration` | `1.0s` human, `0.4s` qa/sim | W2128769827 | Outcome presentation duration is implementation-defined. | inferred | Displays self/other split and running totals. |
| timing.iti | `timing.iti_duration` | `0.8s` human, `0.3s` qa/sim | W2128769827 | No exact ITI requirement in selected papers. | inferred | Keeps rhythmic spacing between trials. |
| controller.allocation_profiles | `controller.allocation_profiles` | generous=0.3 self, equal=0.5 self, selfish=0.9 self | W2128769827 | Dictator task is defined by unilateral split decisions; exact menu values are implementation parameters. | inferred | Fixed three-option menu ensures stable repeated-trial sampling. |
| controller.stake_levels | `controller.stake_levels` | low=10, medium=20, high=30 | W3125258780 | Papers discuss variability in sharing context/norms, not fixed numerical stakes. | inferred | Stake tiers provide controlled context manipulation. |
| trigger.plan | `triggers.map` | exp/block/stake_prompt/decision/response/timeout/feedback/iti markers | W2128769827 | Event coding for EEG/behavior logging is implementation-specific. | inferred | Condition-specific prompt/decision onset triggers are maintained. |