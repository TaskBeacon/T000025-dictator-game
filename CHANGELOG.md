# CHANGELOG

## [v0.2.1-dev] - 2026-02-19

### Changed
- Rebuilt literature bundle with task-relevant curated papers and regenerated reference artifacts.
- Replaced corrupted `references/task_logic_audit.md` with a full state-machine audit.
- Updated `references/stimulus_mapping.md` to concrete implemented stimulus IDs per condition.
- Synced metadata (`README.md`, `taskbeacon.yaml`) with current configuration and evidence.


All notable development changes for `T000025-dictator-game` are documented here.

## [v0.2.0-dev] - 2026-02-18
### Added
- Dictator-game specific controller for stake scheduling and self/other payoff accounting.
- Dictator-game specific sampler responder with three-way softmax choice policy.

### Changed
- Replaced placeholder MID-style logic with true Dictator Game flow:
  - three-option allocation decision (generous/equal/selfish),
  - direct payoff mapping without partner response,
  - cumulative self/other totals tracked per trial.
- Rebuilt `src/run_trial.py` to sequence:
  - cue -> anticipation -> decision(target) -> decision feedback -> outcome feedback -> iti.
- Updated `main.py` block summaries to dictator metrics (choice rates, block and cumulative payoffs).
- Rewrote all config profiles to split human/qa/scripted-sim/sampler-sim usage with clear section comments.
- Rewrote README to standardized auditable format (`## 1`..`## 4`).

### Fixed
- Removed adaptive target-duration and hit/miss logic unrelated to Dictator Game.

### Validation
- `python -m psyflow.validate e:/Taskbeacon/T000025-dictator-game`
- `python main.py qa --config config/config_qa.yaml`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
