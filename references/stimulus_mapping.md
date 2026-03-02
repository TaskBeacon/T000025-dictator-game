# Stimulus Mapping

Task: `Dictator Game`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence Type | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `low_stake` | `stake_prompt_text`, `decision_panel`, `decision_generous`, `decision_equal`, `decision_selfish`, `decision_timeout`, `outcome_feedback`, `fixation` | `W2128769827` | Dictator-game allocation decision with unilateral split outcome (paradigm-level) | `psychopy_builtin` | Endowment fixed to 10 points by controller stake map. |
| `medium_stake` | `stake_prompt_text`, `decision_panel`, `decision_generous`, `decision_equal`, `decision_selfish`, `decision_timeout`, `outcome_feedback`, `fixation` | `W2128769827` | Dictator-game allocation decision with unilateral split outcome (paradigm-level) | `psychopy_builtin` | Endowment fixed to 20 points by controller stake map. |
| `high_stake` | `stake_prompt_text`, `decision_panel`, `decision_generous`, `decision_equal`, `decision_selfish`, `decision_timeout`, `outcome_feedback`, `fixation` | `W2128769827` | Dictator-game allocation decision with unilateral split outcome (paradigm-level) | `psychopy_builtin` | Endowment fixed to 30 points by controller stake map. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye`, `fixation` | `W3125258780` | Task envelope and repeated decision framing | `psychopy_builtin` | Shared Chinese instruction/summary screens used across human/qa/sim configs. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered with PsychoPy text primitives configured in YAML.
- `generated_reference_asset`: task-specific generated assets from literature-described rules.
- `licensed_external_asset`: external licensed media with citation linkage.
