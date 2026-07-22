# 02 - Spawn Primitives ★

## Goal
Add dynamic rigid bodies (a cube and a sphere), let gravity act on them, and
read their world poses back each second as they settle.

## What you learn
- `DynamicCuboid` / `DynamicSphere` and the `prim_path` USD hierarchy.
- Adding objects to `world.scene`.
- `get_world_pose()` to query state during stepping.

## Run
```bash
~/env_isaacsim/bin/python spawn_primitives.py
```

## Extend it
- Add a `PhysicsMaterial` with high restitution and watch them bounce.
- Apply an impulse with `apply_force` / set initial linear velocity.
