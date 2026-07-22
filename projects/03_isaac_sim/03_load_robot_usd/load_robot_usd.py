#!/usr/bin/env python3
"""Load a robot from the Isaac asset library and inspect its articulation
(DOF names, joint limits)."""
import argparse
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()
sim_app = SimulationApp({"headless": args.headless})

from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.nucleus import get_assets_root_path

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

assets = get_assets_root_path()
franka_usd = assets + "/Isaac/Robots/Franka/franka.usd"
add_reference_to_stage(usd_path=franka_usd, prim_path="/World/Franka")
robot = world.scene.add(Robot(prim_path="/World/Franka", name="franka"))

world.reset()
print("DOF names :", robot.dof_names)
print("DOF count :", robot.num_dof)
print("Lower lim :", robot.dof_properties["lower"])
print("Upper lim :", robot.dof_properties["upper"])

for i in range(120):
    world.step(render=not args.headless)

sim_app.close()
