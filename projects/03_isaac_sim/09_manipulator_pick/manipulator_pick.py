#!/usr/bin/env python3
"""Franka pick task using the built-in PickPlace controller + task API."""
import argparse
import numpy as np
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()
sim_app = SimulationApp({"headless": args.headless})

from omni.isaac.core import World
from omni.isaac.franka.tasks import PickPlace
from omni.isaac.franka.controllers import PickPlaceController

world = World(stage_units_in_meters=1.0)
task = PickPlace(name="franka_pick")
world.add_task(task)
world.reset()

params = task.get_params()
franka = world.scene.get_object(params["robot_name"]["value"])
controller = PickPlaceController(
    name="pick_place", gripper=franka.gripper,
    robot_articulation=franka)

for i in range(1500):
    obs = world.get_observations()
    cube_name = params["cube_name"]["value"]
    target = params["target_position"]["value"]
    actions = controller.forward(
        picking_position=obs[cube_name]["position"],
        placing_position=target,
        current_joint_positions=franka.get_joint_positions())
    franka.apply_action(actions)
    if controller.is_done():
        print("Pick-and-place complete.")
        break
    world.step(render=not args.headless)

sim_app.close()
