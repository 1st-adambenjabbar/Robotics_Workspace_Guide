#!/usr/bin/env python3
"""Randomise object pose, color and lighting every N steps (sim2real DR)."""
import argparse
import numpy as np
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()
sim_app = SimulationApp({"headless": args.headless})

from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()
box = world.scene.add(DynamicCuboid(
    prim_path="/World/box", name="box",
    position=np.array([0, 0, 0.5]), scale=np.array([0.3, 0.3, 0.3])))
world.reset()

rng = np.random.default_rng(0)
for i in range(600):
    if i % 60 == 0:
        pos = np.array([rng.uniform(-1, 1), rng.uniform(-1, 1), 0.5])
        color = rng.uniform(0.1, 0.9, size=3)
        box.set_world_pose(position=pos)
        try:
            box.get_applied_visual_material().set_color(color)
        except Exception:
            pass
        print(f"randomised: pos={np.round(pos,2)} color={np.round(color,2)}")
    world.step(render=not args.headless)

sim_app.close()
