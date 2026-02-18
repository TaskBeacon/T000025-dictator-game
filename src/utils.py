from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from psychopy import logging


@dataclass(frozen=True)
class AllocationProfile:
    label: str
    self_ratio: float


class Controller:
    """Dictator-game scheduler and allocation tracker."""

    def __init__(
        self,
        *,
        allocation_profiles: dict[str, dict[str, Any]],
        stake_levels: dict[str, int],
        seed: int = 25025,
        enable_logging: bool = True,
    ) -> None:
        self.seed = int(seed)
        self.enable_logging = bool(enable_logging)
        self._rng = random.Random(self.seed)
        self._allocations = self._build_allocations(allocation_profiles)
        self._stakes = self._build_stakes(stake_levels)
        self._history: list[dict[str, Any]] = []
        self._self_total = 0
        self._other_total = 0

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "Controller":
        allocations = config.get("allocation_profiles", {})
        stakes = config.get("stake_levels", {})
        if not isinstance(allocations, dict) or not allocations:
            raise ValueError("controller.allocation_profiles must be a non-empty mapping")
        if not isinstance(stakes, dict) or not stakes:
            raise ValueError("controller.stake_levels must be a non-empty mapping")
        return cls(
            allocation_profiles=allocations,
            stake_levels=stakes,
            seed=int(config.get("seed", 25025)),
            enable_logging=bool(config.get("enable_logging", True)),
        )

    def _build_allocations(self, raw: dict[str, dict[str, Any]]) -> dict[str, AllocationProfile]:
        profiles: dict[str, AllocationProfile] = {}
        for key, spec in raw.items():
            self_ratio = float(spec.get("self_ratio", 0.5))
            self_ratio = max(0.0, min(1.0, self_ratio))
            profiles[str(key)] = AllocationProfile(label=str(spec.get("label", key)), self_ratio=self_ratio)
        return profiles

    def _build_stakes(self, raw: dict[str, int]) -> dict[str, int]:
        stakes: dict[str, int] = {}
        for key, value in raw.items():
            stakes[str(key)] = max(1, int(value))
        return stakes

    @property
    def self_total(self) -> int:
        return int(self._self_total)

    @property
    def other_total(self) -> int:
        return int(self._other_total)

    @property
    def histories(self) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for item in self._history:
            grouped.setdefault(str(item["condition"]), []).append(item)
        return grouped

    def get_stake(self, condition: str) -> int:
        condition = str(condition)
        if condition not in self._stakes:
            raise KeyError(f"Unknown condition: {condition!r}")
        return int(self._stakes[condition])

    def get_allocation(self, choice: str) -> AllocationProfile:
        choice = str(choice)
        if choice not in self._allocations:
            raise KeyError(f"Unknown allocation choice: {choice!r}")
        return self._allocations[choice]

    def prepare_block(self, *, block_idx: int, n_trials: int, conditions: list[str]) -> list[tuple[Any, ...]]:
        if n_trials <= 0:
            return []

        valid_conditions = [str(c) for c in conditions if str(c) in self._stakes]
        if not valid_conditions:
            raise ValueError("No valid dictator-game conditions available")

        scheduled = [valid_conditions[i % len(valid_conditions)] for i in range(n_trials)]
        self._rng.shuffle(scheduled)

        planned: list[tuple[Any, ...]] = []
        for trial_index, cond in enumerate(scheduled, start=1):
            stake = self.get_stake(cond)
            condition_label = cond.replace("_", " ")
            condition_id = f"{cond}_s{stake}_t{trial_index:03d}"
            planned.append((cond, condition_label, int(stake), condition_id, int(trial_index)))

        if self.enable_logging:
            logging.data(
                "[DictatorController] "
                f"block={block_idx} n_trials={n_trials} seed={self.seed} "
                f"conditions={valid_conditions}"
            )
        return planned

    def register_decision(
        self,
        *,
        condition: str,
        block_idx: int,
        trial_index: int,
        stake: int,
        choice: str,
        timed_out: bool,
    ) -> dict[str, Any]:
        profile = self.get_allocation(choice)
        stake_i = max(1, int(stake))
        self_amount = int(round(stake_i * float(profile.self_ratio)))
        self_amount = max(0, min(stake_i, self_amount))
        other_amount = int(stake_i - self_amount)

        self._self_total += self_amount
        self._other_total += other_amount

        record = {
            "condition": str(condition),
            "block_idx": int(block_idx),
            "trial_index": int(trial_index),
            "stake": stake_i,
            "choice": str(choice),
            "choice_label": str(profile.label),
            "timed_out": bool(timed_out),
            "self_ratio": float(profile.self_ratio),
            "self_amount": int(self_amount),
            "other_amount": int(other_amount),
            "self_total": int(self._self_total),
            "other_total": int(self._other_total),
        }
        self._history.append(record)

        if self.enable_logging:
            logging.data(
                "[DictatorController] "
                f"trial={trial_index} block={block_idx} condition={condition} "
                f"choice={choice} self={self_amount} other={other_amount} "
                f"self_total={self._self_total} other_total={self._other_total}"
            )

        return record
