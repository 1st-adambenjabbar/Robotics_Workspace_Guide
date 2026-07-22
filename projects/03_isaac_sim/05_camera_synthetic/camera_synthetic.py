#!/usr/bin/env python3
"""Attach a camera, render, and grab synthetic RGB + depth + segmentation."""
import argparse
import numpy as np
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()
sim_app = SimulationApp({"headless": args.headless})

from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid
from omni.isaac.sensor import Camera
import omni.isaac.core.utils.numpy.rotations as rot_utils

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()
world.scene.add(DynamicCuboid(prim_path="/World/box", name="box",
                              position=np.array([0, 0, 0.5]),
                              scale=np.array([0.3, 0.3, 0.3]),
                              color=np.array([0.1, 0.8, 0.2])))

cam = Camera(prim_path="/World/camera",
             position=np.array([2.5, 0.0, 1.5]),
             frequency=20, resolution=(640, 480),
             orientation=rot_utils.euler_angles_to_quats(
                 np.array([0, 20, 180]), degrees=True))
world.reset()
cam.initialize()
cam.add_distance_to_image_plane_to_frame()   # depth
cam.add_semantic_segmentation_to_frame()     # segmentation

for i in range(60):
    world.step(render=True)
rgb = cam.get_rgba()
depth = cam.get_current_frame().get("distance_to_image_plane")
print("RGB shape  :", None if rgb is None else rgb.shape)
print("Depth shape:", None if depth is None else depth.shape)

# Save with numpy so it works headless without a display
if rgb is not None:
    np.save("rgb.npy", rgb)
if depth is not None:
    np.save("depth.npy", depth)
print("Saved rgb.npy / depth.npy")

sim_app.close()
