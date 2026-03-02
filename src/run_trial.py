from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, set_trial_context


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _parse_condition(condition: Any) -> dict[str, Any]:
    if isinstance(condition, tuple) and len(condition) >= 5:
        name, condition_label, stake, condition_id, trial_index, *_ = condition
        return {
            "condition": str(name),
            "condition_label": str(condition_label),
            "stake": int(stake),
            "condition_id": str(condition_id),
            "trial_index": int(trial_index),
        }

    if isinstance(condition, dict):
        return {
            "condition": str(condition.get("condition", "medium_stake")),
            "condition_label": str(condition.get("condition_label", "medium stake")),
            "stake": int(condition.get("stake", 20)),
            "condition_id": str(condition.get("condition_id", "unknown")),
            "trial_index": int(condition.get("trial_index", 0)),
        }

    return {
        "condition": str(condition),
        "condition_label": str(condition),
        "stake": 20,
        "condition_id": str(condition),
        "trial_index": 0,
    }


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one Dictator Game trial."""
    parsed = _parse_condition(condition)
    block_idx_val = int(block_idx) if block_idx is not None else 0
    trial_id = int(parsed["trial_index"]) if parsed["trial_index"] > 0 else 1
    generous_key, equal_key, selfish_key = list(settings.key_list)

    trial_data = {
        "trial_id": trial_id,
        "block_id": str(block_id) if block_id is not None else "block_0",
        "block_idx": block_idx_val,
        "condition": parsed["condition"],
        "condition_id": parsed["condition_id"],
        "condition_label": parsed["condition_label"],
        "stake": int(parsed["stake"]),
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    stake_prompt = make_unit(unit_label="stake_prompt").add_stim(
        stim_bank.get_and_format(
            "stake_prompt_text",
            condition_label=parsed["condition_label"],
            stake=int(parsed["stake"]),
        )
    )
    set_trial_context(
        stake_prompt,
        trial_id=trial_id,
        phase="stake_prompt",
        deadline_s=_deadline_s(settings.stake_prompt_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "stake_prompt",
            "condition": parsed["condition"],
            "stake": int(parsed["stake"]),
            "block_idx": block_idx_val,
        },
        stim_id="stake_prompt_text",
    )
    stake_prompt.show(
        duration=settings.stake_prompt_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_prompt_onset"),
    ).to_dict(trial_data)

    pre_decision_fixation = make_unit(unit_label="pre_decision_fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        pre_decision_fixation,
        trial_id=trial_id,
        phase="pre_decision_fixation",
        deadline_s=_deadline_s(settings.pre_decision_fixation_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "pre_decision_fixation",
            "condition": parsed["condition"],
            "stake": int(parsed["stake"]),
            "block_idx": block_idx_val,
        },
        stim_id="fixation",
    )
    pre_decision_fixation.show(duration=settings.pre_decision_fixation_duration).to_dict(trial_data)

    decision = make_unit(unit_label="decision").add_stim(
        stim_bank.get_and_format("decision_panel", stake=int(parsed["stake"]))
    )
    set_trial_context(
        decision,
        trial_id=trial_id,
        phase="decision",
        deadline_s=_deadline_s(settings.decision_duration),
        valid_keys=[generous_key, equal_key, selfish_key],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "decision",
            "condition": parsed["condition"],
            "stake": int(parsed["stake"]),
            "generous_key": generous_key,
            "equal_key": equal_key,
            "selfish_key": selfish_key,
            "block_idx": block_idx_val,
        },
        stim_id="decision_panel",
    )
    decision.capture_response(
        keys=[generous_key, equal_key, selfish_key],
        duration=settings.decision_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_decision_onset"),
        response_trigger=settings.triggers.get("decision_response"),
        timeout_trigger=settings.triggers.get("decision_timeout"),
    )
    decision.to_dict(trial_data)

    response = decision.get_state("response")
    timed_out = response not in (generous_key, equal_key, selfish_key)
    if response == generous_key:
        choice = "generous"
    elif response == selfish_key:
        choice = "selfish"
    else:
        choice = "equal"

    outcome = controller.register_decision(
        condition=parsed["condition"],
        block_idx=block_idx_val,
        trial_index=trial_id,
        stake=int(parsed["stake"]),
        choice=choice,
        timed_out=timed_out,
    )

    choice_feedback_stim_id = (
        "decision_timeout"
        if timed_out
        else "decision_generous"
        if choice == "generous"
        else "decision_selfish"
        if choice == "selfish"
        else "decision_equal"
    )
    choice_feedback = make_unit(unit_label="choice_feedback").add_stim(
        stim_bank.get_and_format(choice_feedback_stim_id, choice_label=outcome["choice_label"])
    )
    set_trial_context(
        choice_feedback,
        trial_id=trial_id,
        phase="choice_feedback",
        deadline_s=_deadline_s(settings.choice_feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "choice_feedback",
            "choice": choice,
            "choice_label": outcome["choice_label"],
            "timed_out": timed_out,
            "block_idx": block_idx_val,
        },
        stim_id=choice_feedback_stim_id,
    )
    choice_feedback.show(
        duration=settings.choice_feedback_duration,
        onset_trigger=settings.triggers.get("choice_feedback_onset"),
    ).to_dict(trial_data)

    outcome_feedback = make_unit(unit_label="outcome_feedback").add_stim(
        stim_bank.get_and_format(
            "outcome_feedback",
            stake=int(outcome["stake"]),
            choice_label=outcome["choice_label"],
            self_amount=int(outcome["self_amount"]),
            other_amount=int(outcome["other_amount"]),
            self_total=int(outcome["self_total"]),
            other_total=int(outcome["other_total"]),
        )
    )
    set_trial_context(
        outcome_feedback,
        trial_id=trial_id,
        phase="outcome_feedback",
        deadline_s=_deadline_s(settings.outcome_feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "outcome_feedback",
            "choice": choice,
            "stake": int(outcome["stake"]),
            "self_amount": int(outcome["self_amount"]),
            "other_amount": int(outcome["other_amount"]),
            "self_total": int(outcome["self_total"]),
            "other_total": int(outcome["other_total"]),
            "block_idx": block_idx_val,
        },
        stim_id="outcome_feedback",
    )
    outcome_feedback.show(
        duration=settings.outcome_feedback_duration,
        onset_trigger=settings.triggers.get("outcome_feedback_onset"),
    ).to_dict(trial_data)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=_deadline_s(settings.iti_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={"stage": "inter_trial_interval", "block_idx": block_idx_val},
        stim_id="fixation",
    )
    iti.show(duration=settings.iti_duration, onset_trigger=settings.triggers.get("iti_onset")).to_dict(trial_data)

    trial_data["choice"] = str(outcome["choice"])
    trial_data["choice_label"] = str(outcome["choice_label"])
    trial_data["timed_out"] = bool(outcome["timed_out"])
    trial_data["stake"] = int(outcome["stake"])
    trial_data["self_ratio"] = float(outcome["self_ratio"])
    trial_data["self_amount"] = int(outcome["self_amount"])
    trial_data["other_amount"] = int(outcome["other_amount"])
    trial_data["self_total"] = int(outcome["self_total"])
    trial_data["other_total"] = int(outcome["other_total"])
    trial_data["feedback_delta"] = int(outcome["self_amount"])

    return trial_data