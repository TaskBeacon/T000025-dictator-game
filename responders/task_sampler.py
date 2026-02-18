from __future__ import annotations

from dataclasses import dataclass
from math import exp
import random as _py_random
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for Dictator Game three-way allocation choices."""

    generous_key: str = "f"
    equal_key: str = "space"
    selfish_key: str = "j"
    continue_key: str = "space"
    generosity_bias: float = 0.6
    equal_bias: float = 0.2
    stake_sensitivity: float = 0.5
    inverse_temp: float = 6.0
    lapse_rate: float = 0.03
    rt_mean_s: float = 0.38
    rt_sd_s: float = 0.08
    rt_min_s: float = 0.16

    def __post_init__(self) -> None:
        self.generosity_bias = float(self.generosity_bias)
        self.equal_bias = float(self.equal_bias)
        self.stake_sensitivity = float(self.stake_sensitivity)
        self.inverse_temp = max(1e-6, float(self.inverse_temp))
        self.lapse_rate = max(0.0, min(1.0, float(self.lapse_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))
        self._rng: Any = None

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _rand(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _softmax(self, values: list[float]) -> list[float]:
        if not values:
            return []
        max_v = max(values)
        exps = [exp(self.inverse_temp * (v - max_v)) for v in values]
        total = sum(exps)
        if total <= 0:
            return [1.0 / len(values)] * len(values)
        return [v / total for v in exps]

    def _sample_index(self, probs: list[float]) -> int:
        u = self._rand()
        c = 0.0
        for idx, p in enumerate(probs):
            c += p
            if u <= c:
                return idx
        return max(0, len(probs) - 1)

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        phase = str(obs.phase or "")
        if phase != "target" and self.continue_key in valid_keys:
            return Action(
                key=self.continue_key,
                rt_s=max(self.rt_min_s, self.rt_mean_s - 0.12),
                meta={"source": "task_sampler", "policy": "continue"},
            )

        if phase != "target":
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "phase": phase})

        factors = dict(obs.task_factors or {})
        stake = float(factors.get("stake", 20.0))
        stake_norm = (stake - 20.0) / 10.0

        logits = [
            self.generosity_bias - self.stake_sensitivity * stake_norm,
            self.equal_bias,
            -self.generosity_bias + self.stake_sensitivity * stake_norm,
        ]
        probs = self._softmax(logits)

        rt = max(self.rt_min_s, self._normal(self.rt_mean_s, self.rt_sd_s))

        keys = [self.generous_key, self.equal_key, self.selfish_key]

        if self._rand() < self.lapse_rate:
            key = valid_keys[int(self._rand() * len(valid_keys)) % len(valid_keys)]
            return Action(key=key, rt_s=rt, meta={"source": "task_sampler", "policy": "lapse"})

        idx = self._sample_index(probs)
        key = keys[idx]
        if key not in valid_keys:
            key = valid_keys[0]

        return Action(
            key=key,
            rt_s=rt,
            meta={
                "source": "task_sampler",
                "policy": "three_way_softmax",
                "stake": stake,
                "p_generous": probs[0],
                "p_equal": probs[1],
                "p_selfish": probs[2],
            },
        )
