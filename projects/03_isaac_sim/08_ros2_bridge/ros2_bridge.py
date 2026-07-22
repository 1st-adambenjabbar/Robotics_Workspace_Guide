#!/usr/bin/env python3
"""Enable the ROS 2 bridge and publish a camera image + TF from Isaac Sim.
Run alongside a sourced ROS 2 Humble environment to see the topics."""
import argparse
import numpy as np
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
args, _ = ap.parse_known_args()
# The ROS2 bridge extension must be enabled at startup:
sim_app = SimulationApp({"headless": args.headless})

from omni.isaac.core.utils.extensions import enable_extension
enable_extension("omni.isaac.ros2_bridge")
sim_app.update()

from omni.isaac.core import World
from omni.isaac.sensor import Camera
import omni.isaac.core.utils.numpy.rotations as rot_utils
import omni.graph.core as og

world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()
cam = Camera(prim_path="/World/camera",
             position=np.array([2.0, 0.0, 1.0]),
             frequency=20, resolution=(640, 480),
             orientation=rot_utils.euler_angles_to_quats(
                 np.array([0, 15, 180]), degrees=True))
world.reset()
cam.initialize()

# Build an OmniGraph action graph that publishes the camera on ROS 2.
og.Controller.edit(
    {"graph_path": "/World/ROS2Camera", "evaluator_name": "execution"},
    {
        og.Controller.Keys.CREATE_NODES: [
            ("Tick", "omni.graph.action.OnPlaybackTick"),
            ("Ctx", "omni.isaac.ros2_bridge.ROS2Context"),
            ("Pub", "omni.isaac.ros2_bridge.ROS2CameraHelper"),
        ],
        og.Controller.Keys.CONNECT: [
            ("Tick.outputs:tick", "Pub.inputs:execIn"),
            ("Ctx.outputs:context", "Pub.inputs:context"),
        ],
        og.Controller.Keys.SET_VALUES: [
            ("Pub.inputs:topicName", "/isaac/camera/rgb"),
            ("Pub.inputs:type", "rgb"),
            ("Pub.inputs:renderProductPath", cam.get_render_product_path()),
        ],
    },
)

print("Publishing /isaac/camera/rgb on ROS 2. In another sourced shell:")
print("  ros2 topic list ; ros2 topic hz /isaac/camera/rgb")
for i in range(2000):
    world.step(render=True)

sim_app.close()
