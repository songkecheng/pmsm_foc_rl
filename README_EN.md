# PMSM FOC and Reinforcement Learning Simulation Project

This project is for simulating permanent magnet synchronous motors (PMSMs), field-oriented control (FOC), and reinforcement-learning methods.

## Activate the Python Environment

```bash
cd /home/user/pmsm_foc_rl
source .venv/bin/activate
```

## Install Project Dependencies

```bash
python -m pip install -r requirements.txt
```

The requirements file includes PyTorch with CUDA 13.0. Using this version requires a working NVIDIA GPU driver. Motor simulation runs mainly on the CPU; PyTorch can use CUDA to train neural networks.

## Run a Quick PMSM Simulation Check

```bash
python check_environment.py
```

This script creates a continuous-current-control PMSM environment, resets it, and takes one action to check that the environment interface works with Stable-Baselines3.

## Current Target Motor for Simulation

The current target motor is the **42JSF840AS-1000-8**. The table below is based on the motor specification sheet shared for this project and can be used as the initial Gym Electric Motor (GEM) configuration. Values or definitions marked as provisional must be confirmed before using the simulation for quantitative conclusions.

| Item | Specification / GEM value | Notes |
|---|---:|---|
| Motor type | Three-phase PMSM | Permanent magnet synchronous motor |
| DC bus voltage | 24 V | Set GEM's voltage supply `u_nominal` to 24 V. The default PMSM environment uses 300 V, so override the default. |
| Number of poles / pole pairs | 8 / 4 | Set the GEM motor parameter `p=4`. |
| Rated speed | 4000 rpm (about 418.9 rad/s) | This is the rated speed; the specification sheet does not identify it as the maximum speed. |
| Rated current | 4.5 A | Confirm whether this is RMS or peak current. If it is phase RMS current, the sinusoidal peak is about 6.36 A. |
| Peak current | 13.5 A | Confirm the current convention and make sure it is compatible with the selected drive's current limit. |
| Rated / peak torque | 0.19 / 0.35 N·m |  |
| Rated output power | 78 W |  |
| Stator resistance `r_s` | 0.59 Ω (provisional) | The specification sheet does not say whether this is phase or line-to-line resistance. Confirm before final use. |
| d/q-axis inductance `l_d`, `l_q` | 0.66 mH each (provisional) | The sheet gives one inductance value, not separate d-axis and q-axis values. Initial assumption: `l_d ≈ l_q = 0.00066 H`. |
| Back-EMF constant | 2.95 Vrms/kRPM, line-to-line | The sheet labels this `Ke(RMS-L)`. With the sinusoidal PMSM line-to-line RMS convention, the provisional GEM flux linkage is `psi_p ≈ 0.00575 Wb`. |
| Rotor inertia `j_rotor` | `1.85e-5 kg·m²` | Provided on the specification sheet. |
| Simulation control step `tau` | Initially `1e-4 s` | This is GEM's default. Align it with the real control-loop period once that is known. |
| Initial load speed | 0 rad/s for initial current-loop checks | Add tests at different fixed speeds after the current response is stable. |

The sensor wiring table in the specification sheet lists Hall U/V/W signals but does not show encoder A/B/Z wiring. GEM's ideal motor model does not need physical encoder wiring, but confirm whether the motor has an encoder and how its signals are brought out before testing FOC on hardware.

The `Cont-CC-PMSM-v0` environment takes normalized voltage commands as actions. It does not implement the project's fixed PI current controller or reinforcement-learning-assisted PI gain adjustment by itself. Those controllers and the comparison workflow still need to be implemented separately.

## Configure VS Code

Open the project folder in VS Code and select `.venv/bin/python` as the Python interpreter.

## Project Folders

- `src/`: controllers, environment wrappers, and experiment code
- `results/`: generated figures and data
- `paper/`: paper drafts and reference material
- `check_environment.py`: script for checking the simulation environment installation
