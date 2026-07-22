#!/usr/bin/env python3
"""Minimal Isaac Sim app: open a stage, add a ground plane and a light,
then step the simulation for a few seconds."""
import argparse
from isaacsim import SimulationApp   # on older builds: from omni.isaac.kit import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()

sim_app = SimulationApp({"headless": args.headless})

# Imports that need the app running must come AFTER SimulationApp(...)
from omni.isaac.core import World
from omni.isaac.core.objects import GroundPlane

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()
world.reset()

print("Stepping simulation...")
for i in range(240):
    world.step(render=not args.headless)
    if i % 60 == 0:
        print(f"  step {i}")

print("Done.")
sim_app.close()
