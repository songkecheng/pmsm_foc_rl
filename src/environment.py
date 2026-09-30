"""Gym Electric Motor adapters used by Stable-Baselines3."""

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class FlattenPMSMObservation(gym.ObservationWrapper):
    """Convert GEM's (motor state, reference) tuple into one float32 vector."""

    def __init__(self, env: gym.Env):
        super().__init__(env)
        if not isinstance(env.observation_space, spaces.Tuple):
            raise TypeError("Expected a tuple observation from Gym Electric Motor")
        low = np.concatenate([np.asarray(s.low).ravel() for s in env.observation_space.spaces]).astype(np.float32)
        high = np.concatenate([np.asarray(s.high).ravel() for s in env.observation_space.spaces]).astype(np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

    def observation(self, observation):
        return np.concatenate([np.asarray(part).ravel() for part in observation]).astype(np.float32)


class Float32Action(gym.ActionWrapper):
    """Expose float32 actions to SB3 and cast them for GEM's float64 space."""

    def __init__(self, env: gym.Env):
        super().__init__(env)
        if not isinstance(env.action_space, spaces.Box):
            raise TypeError("This wrapper currently expects a continuous action space")
        self.action_space = spaces.Box(
            low=env.action_space.low.astype(np.float32),
            high=env.action_space.high.astype(np.float32),
            dtype=np.float32,
        )

    def action(self, action):
        return np.asarray(action, dtype=self.env.action_space.dtype)


def make_continuous_pmsm_env(seed: int | None = None) -> gym.Env:
    """Create a GEM continuous-current PMSM environment compatible with SB3."""
    env = gem_make("Cont-CC-PMSM-v0")
    env = FlattenPMSMObservation(env)
    env = Float32Action(env)
    if seed is not None:
        env.reset(seed=seed)
    return env


def gem_make(env_id: str) -> gym.Env:
    # Keep the GEM import local so this module's wrappers remain easy to inspect.
    import gym_electric_motor as gem

    return gem.make(env_id)
