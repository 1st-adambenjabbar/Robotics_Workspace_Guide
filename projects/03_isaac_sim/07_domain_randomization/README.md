# 07 - Domain Randomization ★★★

## Goal
Randomise an object's pose and color (and, with Replicator, lighting and
textures) periodically — the core trick that makes models trained in sim
transfer to the real world.

## What you learn
- Why DR matters for sim2real generalisation.
- Programmatic scene perturbation with a seeded RNG.
- Setting pose and visual material at runtime.

## Run
```bash
~/env_isaacsim/bin/python domain_randomization.py
```

## Extend it
- Use `omni.replicator.core` for proper randomisers (lights, textures,
  camera pose) and capture a labelled, randomised dataset.
- Combine with project 05 to generate a perception training set.
