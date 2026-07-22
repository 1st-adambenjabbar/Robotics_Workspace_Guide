# 01 - Hello Stage ★

## Goal
Boot Isaac Sim from Python, create a `World`, add the default ground plane,
and step the physics/render loop.

## What you learn
- The critical `SimulationApp` rule: it must be created **first**, and all
  `omni.*` imports come **after** it.
- The `World` abstraction (scene + physics + stepping).
- Headless vs GUI execution.

## Run
```bash
~/env_isaacsim/bin/python hello_stage.py            # GUI
~/env_isaacsim/bin/python hello_stage.py --headless # no window
```

## If imports fail on the newest build
Replace `from omni.isaac.core import World` with
`from isaacsim.core.api import World` and
`from omni.isaac.kit import SimulationApp` accordingly.
