# Gazebo Design Languages : SDF, URDF & Xacro
> How to **design robots and worlds** for Gazebo simulation
> SDF · URDF · Xacro — every tag, attribute, and concept explained from scratch 🐚

---

## Part of Learning Path

This guide is part of the **Ultimate Robotics Guide** structured learning sequence:

1. **[Linux Commands Cheat Sheet](Linux%20Commands%20Cheat%20Sheet.md)** - Essential terminal skills
2. **[OOP explained](OOP%20explained%20.md)** - Programming fundamentals (Python, C++, Java, C)
3. **[WSL Installation](WSL%20Installation.md)** - Windows Subsystem for Linux (Windows users)
4. **[ROS 2 Installation Guide](ROS%202%20Installation%20Guide.md)** - Setup ROS2 Humble
5. **[Programming With ROS2](Programming%20With%20ROS2.md)** - Write ROS2 nodes (Publishers, Subscribers, Services, Actions)
6. **[Design Languages for Gazebo](Design%20Languages%20for%20Gazebo.md)** ← **You are here** - Design robot URDF/SDF files
7. **[Gazebo simulation coding guide](Gazebo%20simulation%20coding%20guide.md)** - Write simulation code (LiDAR, sensors, control)
8. **[CUDA Installation](Cuda%20Installation.md)** - GPU acceleration setup
9. **[Isaac Sim Installation and Use](isaac%20sim%20Installation%20and%20Use.md)** - Advanced GPU simulation
10. **[Docker - Git](Docker%20-%20Git.md)** - Containerization and version control

---

# 📑 Table of Contents

1. [What are Design Languages and Why They Exist](#1-what-are-design-languages-and-why-they-exist)
2. [XML Basics — The Syntax Everything is Built On](#2-xml-basics--the-syntax-everything-is-built-on)
3. [SDF — Simulation Description Format](#3-sdf--simulation-description-format)
4. [URDF — Unified Robot Description Format](#4-urdf--unified-robot-description-format)
5. [Links — The Building Blocks](#5-links--the-building-blocks)
6. [Joints — Connecting Links Together](#6-joints--connecting-links-together)
7. [Geometry — Shapes You Can Design](#7-geometry--shapes-you-can-design)
8. [Materials & Visual Appearance](#8-materials--visual-appearance)
9. [Physics — Mass, Inertia & Collision](#9-physics--mass-inertia--collision)
10. [Sensors in SDF/URDF](#10-sensors-in-sdfurdf)
11. [Plugins — Adding Behavior](#11-plugins--adding-behavior)
12. [Xacro — Writing Smarter URDF](#12-xacro--writing-smarter-urdf)
13. [Complete Robot Design — Step by Step](#13-complete-robot-design--step-by-step)
14. [Complete World Design — Step by Step](#14-complete-world-design--step-by-step)
15. [SDF vs URDF — When to Use Which](#15-sdf-vs-urdf--when-to-use-which)
16. [Cheat Sheet & Tag Reference](#16-cheat-sheet--tag-reference)

---

# 1. What are Design Languages and Why They Exist

Before Gazebo can simulate your robot, it needs to know:

- What **shape** is the robot? (box, cylinder, sphere, mesh)
- How **heavy** is it? (mass, center of mass)
- How do the parts **connect**? (joints: fixed, rotating, sliding)
- What **sensors** does it have? (LiDAR, camera, IMU)
- What **behaviors** does it have? (differential drive, ROS2 bridge)

This description is written in a **design language** — a structured text format that Gazebo reads and converts into a 3D simulation.

```
You write:              Gazebo reads:           Gazebo simulates:
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ robot.urdf   │  ───▶  │ Parse XML    │  ───▶  │ 3D physics   │
│ or           │        │ Build model  │        │ Sensors      │
│ robot.sdf    │        │ Apply physics│        │ Collisions   │
└──────────────┘        └──────────────┘        └──────────────┘
```

There are **two** main design languages for Gazebo:

| Language | File extension | Used for | Used by |
|---|---|---|---|
| **URDF** | `.urdf` or `.urdf.xacro` | Robot description | ROS2 (primary format) |
| **SDF** | `.sdf` or `.world` | Robots AND worlds | Gazebo (native format) |
| **Xacro** | `.urdf.xacro` | Smarter URDF with variables | ROS2 + Gazebo |

> - **URDF** is simpler but limited (no friction, no world elements).
> - **SDF** is more powerful but more verbose. Gazebo converts URDF to SDF internally.
> - **Xacro** is not a format — it's a **preprocessor** that generates URDF.

---

*For the complete guide content, see the full file on GitHub.*