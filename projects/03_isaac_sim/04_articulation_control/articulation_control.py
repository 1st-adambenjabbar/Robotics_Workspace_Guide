#!/usr/bin/env python3
"""Command joint targets to a Franka articulation with a sinusoidal sweep."""
import argparse
import numpy as np
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()
sim_app = SimulationApp({"headless": args.headless})

from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.nucleus import get_assets_root_path
from omni.isaac.core.utils.types import ArticulationAction

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()
assets = get_assets_root_path()
add_reference_to_stage(assets + "/Isaac/Robots/Franka/franka.usd",
                       "/World/Franka")
robot = world.scene.add(Robot(prim_path="/World/Franka", name="franka"))
world.reset()
controller = robot.get_articulation_controller()

home = np.array([0.0, -0.4, 0.0, -2.0, 0.0, 1.6, 0.8, 0.04, 0.04])
for i in range(600):
    t = i / 60.0
    target = home.copy()
    target[1] += 0.4 * np.sin(t)      # shoulder sweep
    target[3] += 0.4 * np.sin(t * 0.7)
    controller.apply_action(ArticulationAction(joint_positions=target))
    world.step(render=not args.headless)
    if i % 120 == 0:
        print("joint pos:", np.round(robot.get_joint_positions(), 2))

sim_app.close()
