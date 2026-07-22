# 09 - Manipulator Pick & Place ★★★★

## Goal
Run a full pick-and-place with a Franka arm using Isaac's built-in `PickPlace`
task and `PickPlaceController` (a state-machine over reach/grasp/lift/place).

## What you learn
- The Isaac **Task** abstraction (`add_task`, `get_observations`,
  `get_params`).
- High-level manipulation controllers and gripper control.
- Reading object/target poses from task observations.

## Run
```bash
~/env_isaacsim/bin/python manipulator_pick.py
```

## Notes
- Requires the `omni.isaac.franka` extension (bundled).
- On newest builds the path is `isaacsim.robot.manipulators.examples.franka`.

## Extend it
- Randomise the cube start pose (combine with project 07).
- Replace the scripted controller with an RMPflow motion policy.
