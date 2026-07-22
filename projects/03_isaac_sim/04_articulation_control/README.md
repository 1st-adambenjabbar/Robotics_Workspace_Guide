# 04 - Articulation Control ★★

## Goal
Drive the Franka's joints with position targets, sweeping two joints with a
sine wave while reading back the measured joint positions.

## What you learn
- `get_articulation_controller()` and `ArticulationAction`.
- Position vs velocity vs effort command modes.
- The joint ordering convention (7 arm DOF + 2 finger DOF).

## Run
```bash
~/env_isaacsim/bin/python articulation_control.py
```

## Extend it
- Command joint velocities instead of positions.
- Tune the drive gains (stiffness/damping) via `dof_properties`.
