#!/usr/bin/env python3
"""Add a rotating range sensor (LIDAR) and read back its measurements."""
import argparse
import numpy as np
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()
sim_app = SimulationApp({"headless": args.headless})

from omni.isaac.core import World
from omni.isaac.core.objects import DynamicCuboid
import omni.kit.commands
from omni.isaac.range_sensor import _range_sensor

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()
# walls around the sensor
for i, (x, y) in enumerate([(3, 0), (-3, 0), (0, 3), (0, -3)]):
    world.scene.add(DynamicCuboid(
        prim_path=f"/World/wall{i}", name=f"wall{i}",
        position=np.array([x, y, 0.5]),
        scale=np.array([0.2, 2.0, 1.0]) if x else np.array([2.0, 0.2, 1.0])))

omni.kit.commands.execute(
    "RangeSensorCreateLidar", path="/World/Lidar",
    min_range=0.1, max_range=20.0,
    horizontal_fov=360.0, vertical_fov=10.0,
    horizontal_resolution=1.0, vertical_resolution=1.0,
    rotation_rate=10.0, draw_points=True, draw_lines=True)

lidar_iface = _range_sensor.acquire_lidar_sensor_interface()
world.reset()
for i in range(120):
    world.step(render=not args.headless)
    if i == 100:
        depths = lidar_iface.get_linear_depth_data("/World/Lidar")
        print("LIDAR beams:", np.array(depths).shape)
        print("min/max range:", float(np.min(depths)), float(np.max(depths)))

sim_app.close()
