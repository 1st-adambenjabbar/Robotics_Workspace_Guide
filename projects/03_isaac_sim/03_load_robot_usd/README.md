# 03 - Load a Robot USD ★★

## Goal
Reference a robot (Franka Panda) from the Isaac Nucleus asset library into
the stage and print its articulation structure.

## What you learn
- `get_assets_root_path()` + `add_reference_to_stage` (USD referencing).
- The `Robot` articulation wrapper.
- Reading DOF names, count, and joint limits.

## Run
```bash
~/env_isaacsim/bin/python load_robot_usd.py
```

## Notes
- First run downloads/streams the asset from Nucleus; needs network access
  to the Omniverse asset server.
- On the newest builds use `isaacsim.storage.native.get_assets_root_path`.

## Extend it
- Swap the path for a Carter or UR10 USD.
- Print the link tree by walking the USD prim hierarchy.
