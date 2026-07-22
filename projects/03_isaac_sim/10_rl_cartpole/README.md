# 10 - RL Cartpole Environment ★★★★★

## Goal
Wrap an Isaac Sim cartpole as a Gym-style RL environment with the standard
`reset / step / reward / done` contract, run a random policy, and optionally
train PPO with stable-baselines3.

## What you learn
- The RL environment interface that Isaac Lab / Gymnasium use.
- Reading articulation state as an observation vector and applying effort
  as an action.
- Reward shaping and episode termination.
- The bridge from a physics sim to a learning loop.

## Run
```bash
~/env_isaacsim/bin/python rl_cartpole.py            # random policy
~/env_isaacsim/bin/python rl_cartpole.py --train    # PPO (needs SB3 + gymnasium)
```
Install the training deps inside the Isaac python:
```bash
~/env_isaacsim/bin/python -m pip install gymnasium stable-baselines3
```

## Notes
- For serious RL use **Isaac Lab** (formerly Orbit), which provides
  vectorised GPU envs. This project is the conceptual minimal version.

## Extend it
- Vectorise across many cartpoles for faster training.
- Port the trained policy back and evaluate with rendering on.
