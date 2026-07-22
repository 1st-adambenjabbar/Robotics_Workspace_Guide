#!/usr/bin/env python3
"""Spawn dynamic rigid primitives, run physics, and read back their poses."""
import argparse
import numpy as np
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()
sim_app = SimulationApp({"headless": args.headless})

from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid, DynamicSphere

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

cube = world.scene.add(DynamicCuboid(
    prim_path="/World/cube", name="cube",
    position=np.array([0.0, 0.0, 1.0]),
    scale=np.array([0.2, 0.2, 0.2]),
    color=np.array([0.9, 0.2, 0.2])))
ball = world.scene.add(DynamicSphere(
    prim_path="/World/ball", name="ball",
    position=np.array([0.4, 0.0, 1.5]), radius=0.12,
    color=np.array([0.2, 0.4, 0.9])))

world.reset()
for i in range(300):
    world.step(render=not args.headless)
    if i % 60 == 0:
        cp, _ = cube.get_world_pose()
        bp, _ = ball.get_world_pose()
        print(f"step {i:3d} | cube z={cp[2]:.3f}  ball z={bp[2]:.3f}")

sim_app.close()
