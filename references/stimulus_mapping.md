# Stimulus Mapping

Task: `Dictator Game`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `low_stake` | `cue_text`, `decision_panel`, `decision_generous/equal/selfish/timeout`, `outcome_feedback` | `W2074783654`, `W3125258780` | Dictator allocations under low endowment level with fixed choice set and explicit payoff feedback. | `psychopy_builtin` | Stake mapped to `controller.stake_levels.low_stake=10`. |
| `medium_stake` | `cue_text`, `decision_panel`, `decision_generous/equal/selfish/timeout`, `outcome_feedback` | `W2074783654`, `W3125258780` | Same allocation structure under medium endowment to assess stake-dependent generosity. | `psychopy_builtin` | Stake mapped to `controller.stake_levels.medium_stake=20`. |
| `high_stake` | `cue_text`, `decision_panel`, `decision_generous/equal/selfish/timeout`, `outcome_feedback` | `W2074783654`, `W3125258780` | High-endowment allocation trials for stake modulation of social preference. | `psychopy_builtin` | Stake mapped to `controller.stake_levels.high_stake=30`. |
| Shared scaffolding | `fixation`, `block_break`, `good_bye` | `inferred` | Standard fixation/summary flow for block pacing and participant feedback. | `psychopy_builtin` | Operational support stimuli independent of stake condition. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
