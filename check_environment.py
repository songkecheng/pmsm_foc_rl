"""Smoke check for the local Gym Electric Motor PMSM environments."""

from importlib.metadata import version
from stable_baselines3.common.env_checker import check_env

from src.environment import make_continuous_pmsm_env


def main() -> None:
    print(f"gym-electric-motor {version('gym-electric-motor')}")
    print(f"gymnasium {version('gymnasium')}")
    print(f"torch {version('torch')}")
    print(f"stable-baselines3 {version('stable-baselines3')}")

    env = make_continuous_pmsm_env(seed=7)
    try:
        check_env(env, warn=True)
        observation, info = env.reset(seed=7)
        action = env.action_space.sample()
        _, reward, terminated, truncated, _ = env.step(action)
        print(
            "Cont-CC-PMSM-v0: SB3-compatible reset/step OK; "
            f"observation_shape={observation.shape}; action_space={env.action_space}; "
            f"reward={reward:.4g}"
        )
    finally:
        env.close()


if __name__ == "__main__":
    main()
