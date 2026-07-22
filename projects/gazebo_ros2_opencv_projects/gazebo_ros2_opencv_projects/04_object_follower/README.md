# 04 · Object Follower  ★★☆☆☆

**Package:** `object_follower`

## Goal
Detect a colored object and drive to keep it centered while approaching to a target apparent size — two coupled proportional loops.

## What you learn
- combining a color blob with a 2-DOF control law
- apparent area as a crude range proxy
- deadbands + saturation for smooth, safe motion

## Run
```bash
export TURTLEBOT3_MODEL=waffle
ros2 launch object_follower object_follower.launch.py
# default target is the green ball; change color or target size:
ros2 run object_follower object_follower_node --ros-args -p target_area_frac:=0.15
```

## Extend it
- Replace area-as-range with the real depth from a depth camera (see proj 07).
- Add a PID on both axes and log the step response.
- Make it chase a moving object (teleop a second robot as the target).

## Troubleshooting
- Robot creeps forever → target_area_frac too large for the object/distance.
- Jitters at center → widen the angular deadband (abs(ex) threshold).

---
Part of the *Gazebo · ROS 2 · OpenCV* 10-project series. Controls: press **q** in any OpenCV window to quit.
