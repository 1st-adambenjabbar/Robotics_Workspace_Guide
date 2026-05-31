# ️ Gazebo Design Languages — SDF, URDF & Xacro
> How to **design robots and worlds** for Gazebo simulation
> SDF · URDF · Xacro — every tag, attribute, and concept explained from scratch 


#  Table of Contents

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


# 2. XML Basics — The Syntax Everything is Built On

Both SDF and URDF are written in **XML** (**eXtensible **M**arkup **L**anguage).
Understanding XML syntax is essential before reading any design file.

```xml
<!-- This is an XML comment — ignored by the parser -->

<!-- An ELEMENT (also called a TAG) -->
<element_name>
    content goes here
</element_name>

<!-- A SELF-CLOSING element (no content) -->
<element_name/>

<!-- An element with ATTRIBUTES -->
<box size="1.0 2.0 0.5"/>
<!--       ↑             ↑
      attribute name   attribute value (always in quotes)  -->

<!-- Elements can be NESTED inside each other -->
<robot name="my_robot">          ← opening tag
    <link name="base_link">      ← child element
        <visual>                 ← grandchild element
            <geometry>
                <box size="0.3 0.2 0.1"/>
            </geometry>
        </visual>
    </link>
</robot>                         ← closing tag (matches opening)
```

> - **element** (or **tag**) — a named unit of data enclosed in `< >`. Every opening tag `<name>` must have a closing tag `</name>` (or be self-closing `<name/>`).
> - **attribute** — a name=value pair inside an opening tag. Values are always in **double quotes**.
> - **nested** — elements inside other elements. The outer element is the **parent**, the inner is the **child**.
> - **indentation** — spaces at the start of lines. XML doesn't care about indentation (unlike Python), but use it for readability.
> - **parser** — a program that reads and interprets structured text. Gazebo includes an XML parser to read your design files.

### XML rules you MUST follow:

```xml
<!--  CORRECT: every tag is closed -->
<link name="wheel">
    <visual/>
</link>

<!--  WRONG: unclosed tag — will crash Gazebo -->
<link name="wheel">
    <visual>
</link>

<!--  CORRECT: attribute values in quotes -->
<box size="0.3 0.2 0.1"/>

<!--  WRONG: missing quotes -->
<box size=0.3 0.2 0.1/>

<!--  CORRECT: self-closing when no content -->
<box size="1 1 1"/>

<!--  ALSO CORRECT: explicit close -->
<box size="1 1 1"></box>
```


# 3. SDF — Simulation Description Format

**SDF** is Gazebo's **native** format. It can describe:
- Complete **worlds** (lighting, physics, ground, obstacles)
- Individual **models** (robots, furniture, props)
- **Sensors** with full configuration
- **Plugins** (behaviors attached to models)

## SDF File Structure

```xml
<?xml version="1.0" ?>
<!-- ↑ XML declaration: tells the parser this is XML version 1.0 -->

<sdf version="1.6">
<!-- ↑ SDF root element. version="1.6" is the SDF specification version -->
<!-- Use 1.6 for Gazebo Classic, 1.8+ for Gazebo Harmonic -->

  <world name="my_world">
  <!-- ↑ A world contains everything in the simulation -->
  <!-- name: an identifier for this world (used internally) -->

    <!-- ── PHYSICS ENGINE SETTINGS ─────────────────────────── -->
    <physics type="ode">
    <!-- type: which physics engine to use -->
    <!--   "ode"  = Open Dynamics Engine (default, most compatible) -->
    <!--   "bullet" = Bullet Physics (alternative) -->
    <!--   "dart"   = Dynamic Animation and Robotics Toolkit -->

      <max_step_size>0.001</max_step_size>
      <!-- How many seconds each physics step represents -->
      <!-- 0.001s = 1ms per step = 1000 steps per simulated second -->
      <!-- Smaller = more accurate but slower simulation -->

      <real_time_factor>1.0</real_time_factor>
      <!-- Target ratio of sim time to wall time -->
      <!-- 1.0 = real time. 2.0 = twice as fast. 0.5 = half speed -->

      <real_time_update_rate>1000</real_time_update_rate>
      <!-- How many physics steps per wall-clock second -->
      <!-- 1000 Hz is default. Reduce for slower machines -->

      <gravity>0 0 -9.81</gravity>
      <!-- Gravity vector: x y z in m/s² -->
      <!-- Default: -9.81 in Z (downward). 0 = no gravity -->
    </physics>

    <!-- ── GLOBAL ILLUMINATION (sunlight) ──────────────────── -->
    <include>
      <uri>model://sun</uri>
      <!-- include a pre-built model from Gazebo's library -->
      <!-- model://sun = the built-in sun directional light -->
    </include>

    <!-- ── GROUND PLANE ────────────────────────────────────── -->
    <include>
      <uri>model://ground_plane</uri>
      <!-- the infinite flat ground surface -->
    </include>

    <!-- ── SCENE SETTINGS ─────────────────────────────────── -->
    <scene>
      <ambient>0.4 0.4 0.4 1</ambient>
      <!-- Background ambient light: R G B Alpha (0.0-1.0) -->
      <!-- 0.4 = medium grey ambient (everything slightly lit) -->

      <background>0.7 0.7 0.7 1</background>
      <!-- Sky background color: R G B Alpha -->

      <shadows>true</shadows>
      <!-- Enable real-time shadow rendering (costs performance) -->

      <fog>
        <color>0.9 0.9 0.9 1</color>
        <type>linear</type>   <!-- "linear" or "exp" or "exp2" -->
        <start>10</start>     <!-- fog starts at 10m -->
        <end>100</end>        <!-- fog fully opaque at 100m -->
        <density>0.01</density>
      </fog>
    </scene>

  </world>
</sdf>
```

> - `<?xml version="1.0" ?>` — **XML declaration**. Always the first line of any XML file. The `?` indicates a processing instruction (not a regular element).
> - **ODE** = **O**pen **D**ynamics **E**ngine. The most tested and stable physics engine for Gazebo Classic.
> - **Bullet Physics** — another popular open-source physics engine (used in games like Blender). Better for soft bodies.
> - **DART** = **D**ynamic **A**nimation and **R**obotics **T**oolkit. Best for robot arm simulation with accurate dynamics.
> - `model://` — the URI scheme Gazebo uses to look up pre-built models in its model database (`~/.gazebo/models` and system paths).
> - **URI** = **U**niform **R**esource **I**dentifier. A string that identifies a resource. Like a URL but not necessarily a web address.
> - **ambient light** — omnidirectional background light with no source direction. Prevents completely dark shadows.
> - **fog** — atmospheric effect. `linear` = fog increases linearly between start and end distances.


## SDF Model Block

```xml
<model name="my_obstacle">
<!-- name: unique identifier for this model in the world -->

  <static>true</static>
  <!-- true  = model doesn't respond to physics (won't fall, won't move) -->
  <!-- false = full physics simulation (gravity, collisions, inertia) -->
  <!-- Use static=true for: walls, floors, furniture, scenery -->
  <!-- Use static=false for: your robot, balls, moveable objects -->

  <pose>2.0 3.0 0.0  0 0 1.5707</pose>
  <!-- Position AND orientation of the model in the world -->
  <!-- Format: x y z  roll pitch yaw -->
  <!-- x=2, y=3, z=0 → 2m right, 3m forward, on the ground -->
  <!-- roll=0, pitch=0, yaw=1.5707 → rotated 90° around vertical axis -->
  <!-- All values in METRES (position) and RADIANS (rotation) -->

  <allow_auto_disable>true</allow_auto_disable>
  <!-- If true: physics engine can "sleep" this model when it stops moving -->
  <!-- Improves performance for many static-ish objects -->

  <link name="body">
    <!-- ... link content here ... -->
  </link>

</model>
```

> - `<pose>` — 6 numbers: **3 for position** (x, y, z) and **3 for orientation** (roll, pitch, yaw).
>   - All positions in **metres**.
>   - All angles in **radians**. `π rad = 180°`. `π/2 ≈ 1.5707 rad = 90°`.
>   - The coordinate system: **X** = forward, **Y** = left, **Z** = up.
> - **static** models use no CPU for physics. A world with 100 static walls costs almost nothing. A world with 100 dynamic falling boxes can bring Gazebo to a crawl.
> - **sleeping** — the physics engine pauses objects that have been still for a while. They "wake up" if something hits them.


# 4. URDF — Unified Robot Description Format

**URDF** is ROS2's standard robot description format.
Simpler than SDF but sufficient for most robots.

## URDF File Structure

```xml
<?xml version="1.0"?>

<robot name="my_robot">
<!-- The root element of every URDF is <robot> -->
<!-- name: the robot's name — appears in ROS2 as the model name in Gazebo -->

  <!-- A URDF contains only: -->
  <!--   <link>   elements (rigid body parts) -->
  <!--   <joint>  elements (connections between links) -->
  <!--   <gazebo> elements (Gazebo-specific extensions) -->
  <!--   <transmission> elements (for ros2_control) -->

  <link name="base_link">
    <!-- ... -->
  </link>

  <link name="left_wheel">
    <!-- ... -->
  </link>

  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child  link="left_wheel"/>
    <!-- ... -->
  </joint>

</robot>
```

> - `<robot>` — the root element. Every URDF has exactly one `<robot>` tag wrapping everything.
> - In URDF, **every robot must have a link named `base_link`**. It's the root link — all other links attach to it (directly or indirectly) through joints.
> - `<transmission>` — used with **ros2_control** (hardware abstraction layer for actuators). Beyond the scope of this guide.


# 5. Links — The Building Blocks

A **link** is one rigid body part of your robot.
Think of it as a single piece that cannot bend or deform.

```
A differential drive robot has these links:
                 
         ┌──────────────────┐
         │    base_link     │  ← main body
         │                  │
  ┌──┐   │                  │   ┌──┐
  │LW│───┤                  ├───│RW│  ← left_wheel, right_wheel
  └──┘   │                  │   └──┘
         │      ●           │
         │   caster_link     │  ← passive caster wheel
         └──────────────────┘
```

## Complete Link Anatomy

```xml
<link name="base_link">
<!-- name: unique identifier — used by joints to reference this link -->

  <!-- ── VISUAL (what you SEE in simulation) ─────────────────── -->
  <visual>
    <name>base_visual</name>
    <!-- optional name for this visual (a link can have multiple visuals) -->

    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <!-- Position and orientation of the visual RELATIVE to the link's origin -->
    <!-- xyz: offset in metres. rpy: rotation in radians (roll pitch yaw) -->
    <!-- This visual is 5cm above the link origin -->

    <geometry>
      <!-- The 3D shape — see section 7 for all options -->
      <box size="0.3 0.2 0.1"/>
      <!-- 30cm long, 20cm wide, 10cm tall box -->
    </geometry>

    <material name="blue_material">
      <!-- Visual appearance — see section 8 for details -->
      <color rgba="0.0 0.0 1.0 1.0"/>
      <!-- R G B Alpha: 0.0-1.0 each. Pure blue, fully opaque -->
    </material>
  </visual>

  <!-- ── COLLISION (what PHYSICS uses for contact detection) ──── -->
  <collision>
    <!-- Collision shape should be SIMPLER than visual for performance -->
    <!-- A complex visual mesh can use a simple box for collision -->
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <!-- Must match visual origin if you want physics to align visually -->

    <geometry>
      <box size="0.3 0.2 0.1"/>
      <!-- Same shape here, but could be simpler for complex meshes -->
    </geometry>

    <surface>
    <!-- Physical surface properties -->
      <friction>
        <ode>
          <mu>0.8</mu>
          <!-- Coulomb friction coefficient (μ) -->
          <!-- 0.0 = perfectly slippery (ice) -->
          <!-- 1.0 = high friction (rubber on asphalt) -->
          <!-- >1.0 = very sticky (gecko feet) -->
          <mu2>0.8</mu2>
          <!-- Second friction direction (for anisotropic friction) -->
          <!-- e.g. wheels: low friction sideways, high friction forward -->
        </ode>
      </friction>
      <contact>
        <ode>
          <kp>1e6</kp>
          <!-- Spring stiffness of the contact surface (N/m) -->
          <!-- Higher = harder surface. 1e6 = rigid-ish. 1e4 = soft foam -->
          <kd>100</kd>
          <!-- Damping coefficient — how quickly contact oscillations die out -->
          <!-- Higher = less bouncy. Lower = more springy -->
          <min_depth>0.001</min_depth>
          <!-- Allow 1mm penetration before contact forces apply -->
          <!-- Prevents jitter from very rigid surfaces -->
        </ode>
      </contact>
    </surface>
  </collision>

  <!-- ── INERTIAL (how mass is distributed — needed for physics) ─ -->
  <inertial>
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <!-- Center of mass position relative to link origin -->
    <!-- For a uniform box: center of mass = geometric center -->

    <mass value="2.0"/>
    <!-- Mass in KILOGRAMS -->
    <!-- Typical robot body: 1-10 kg. Wheel: 0.1-0.5 kg -->

    <inertia
      ixx="0.0083" ixy="0.0" ixz="0.0"
      iyy="0.0122" iyz="0.0"
      izz="0.0183"/>
    <!-- The INERTIA TENSOR: 3×3 symmetric matrix describing mass distribution -->
    <!-- Determines how the object ROTATES when forces are applied -->
    <!-- See formulas below for calculating these values -->
  </inertial>

</link>
```

> - **Visual** — the shape Gazebo **renders**. You can make this very detailed (high-poly mesh).
> - **Collision** — the shape used for **physics contact detection**. Should be **simple** (box, cylinder, sphere). Complex collision shapes are very slow.
> - **Inertial** — the **mass distribution**. Without this, Gazebo treats the link as having zero mass — it will glitch and fly around. Always add inertial to non-static links.
> - **origin** — the position/orientation of a sub-element **relative** to the link's own coordinate frame. If you offset the visual but not the collision, they'll be misaligned.
> - **Coulomb friction** (μ) — named after Charles-Augustin de Coulomb. The ratio of friction force to normal force. `Friction = μ × Normal_force`.
> - **kp** (spring constant) — how stiff the contact surface is. Named after **k** = spring constant, **p** = position. High kp → very rigid surface (good for robots on floor).
> - **kd** (damping) — dissipates contact energy. Prevents infinite bouncing. Named after **d** = damping.
> - **inertia tensor** — a symmetric 3×3 matrix. Diagonal elements (ixx, iyy, izz) = resistance to rotation around each axis. Off-diagonal (ixy, ixz, iyz) = coupling between axes (usually 0 for symmetric objects).

## Inertia Tensor Formulas

```
For a SOLID BOX (dimensions: lx × ly × lz, mass: m):
  ixx = (1/12) × m × (ly² + lz²)
  iyy = (1/12) × m × (lx² + lz²)
  izz = (1/12) × m × (lx² + ly²)

For a SOLID CYLINDER (radius: r, length: l, mass: m):
  ixx = iyy = (1/12) × m × (3r² + l²)
  izz        = (1/2)  × m × r²

For a SOLID SPHERE (radius: r, mass: m):
  ixx = iyy = izz = (2/5) × m × r²
```

### Python script to compute inertia:

```python
def box_inertia(mass, lx, ly, lz):
    ixx = (1/12) * mass * (ly**2 + lz**2)
    iyy = (1/12) * mass * (lx**2 + lz**2)
    izz = (1/12) * mass * (lx**2 + ly**2)
    print(f'ixx="{ixx:.6f}" ixy="0" ixz="0"')
    print(f'iyy="{iyy:.6f}" iyz="0"')
    print(f'izz="{izz:.6f}"')

def cylinder_inertia(mass, radius, length):
    ixx = iyy = (1/12) * mass * (3 * radius**2 + length**2)
    izz = (1/2) * mass * radius**2
    print(f'ixx="{ixx:.6f}" ixy="0" ixz="0"')
    print(f'iyy="{iyy:.6f}" iyz="0"')
    print(f'izz="{izz:.6f}"')

# Example: robot body (0.3m × 0.2m × 0.1m, 2kg)
box_inertia(mass=2.0, lx=0.3, ly=0.2, lz=0.1)

# Example: wheel (radius=0.05m, length=0.02m, 0.1kg)
cylinder_inertia(mass=0.1, radius=0.05, length=0.02)
```

> Use this script to **calculate** your inertia values. Never guess them — wrong inertia values cause robots to spin, flip, or vibrate uncontrollably in simulation.


# 6. Joints — Connecting Links Together

A **joint** is the connection between two links.
It defines how one link can move relative to another.

```
             parent link
                 │
             ┌───┴───┐
             │ joint  │  ← defines HOW child moves relative to parent
             └───┬───┘
                 │
             child link
```

## Joint Types

```xml
<!-- ── FIXED: no movement — rigid connection ─────────────────── -->
<joint name="camera_mount" type="fixed">
  <parent link="base_link"/>
  <child  link="camera_link"/>
  <origin xyz="0.15 0 0.08" rpy="0 0 0"/>
  <!-- camera is 15cm forward, 8cm up from base center -->
  <!-- Fixed joints: no axis needed, no limits needed -->
</joint>

<!-- ── CONTINUOUS: rotates freely (no limits) — for wheels ───── -->
<joint name="left_wheel_joint" type="continuous">
  <parent link="base_link"/>
  <child  link="left_wheel"/>
  <origin xyz="0 0.12 0" rpy="-1.5707 0 0"/>
  <!-- Wheel is 12cm to the left. Rotated -90° on X to stand upright -->

  <axis xyz="0 0 1"/>
  <!-- The rotation axis in the CHILD LINK's frame -->
  <!-- xyz="0 0 1" = rotates around its own Z axis (spins like a wheel) -->

  <dynamics damping="0.1" friction="0.05"/>
  <!-- damping: resistance to rotation (like axle friction) -->
  <!-- friction: static friction before the joint starts moving -->
</joint>

<!-- ── REVOLUTE: rotates within limits — for arms, doors ─────── -->
<joint name="arm_joint" type="revolute">
  <parent link="shoulder_link"/>
  <child  link="upper_arm_link"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>  <!-- rotates around Y axis (elbow up/down) -->

  <limit lower="-1.5707" upper="1.5707"
         effort="50.0"   velocity="1.0"/>
  <!-- lower: minimum angle in radians (-90°) -->
  <!-- upper: maximum angle in radians (+90°) -->
  <!-- effort: maximum force/torque in Newton-metres (N·m) -->
  <!-- velocity: maximum angular speed in rad/s -->

  <dynamics damping="0.5" friction="0.1"/>
</joint>

<!-- ── PRISMATIC: slides linearly (no rotation) — for lifts ──── -->
<joint name="lift_joint" type="prismatic">
  <parent link="base_link"/>
  <child  link="platform_link"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>  <!-- slides along Z axis (up/down) -->

  <limit lower="0.0" upper="0.5"
         effort="100.0" velocity="0.5"/>
  <!-- lower/upper: min/max position in METRES (not radians) -->
  <!-- 0 to 0.5m = can extend 50cm upward -->
</joint>

<!-- ── FLOATING: 6 degrees of freedom — for free bodies ──────── -->
<joint name="free_body" type="floating">
  <parent link="world"/>
  <child  link="drone_body"/>
  <!-- No axis or limits needed — moves freely in all 6 DOF -->
</joint>

<!-- ── PLANAR: slides in a plane — for omnidirectional robots ─── -->
<joint name="omni_base" type="planar">
  <parent link="world"/>
  <child  link="base_link"/>
  <axis xyz="0 0 1"/>  <!-- the plane's normal vector -->
  <!-- Moves freely in the XY plane, no Z movement -->
</joint>
```

> - **DOF** = **D**egrees **O**f **F**reedom. The number of independent movements possible.
>   - Fixed joint: 0 DOF. Revolute: 1 DOF (rotation). Prismatic: 1 DOF (translation). Floating: 6 DOF (full 3D freedom).
> - `<axis xyz="0 0 1">` — the rotation/translation axis, expressed in the **child link's local frame**. For a wheel lying flat in XY: spin axis is Z (`0 0 1`). After rotating the joint 90°, it stands upright.
> - `effort` — the maximum **torque** (N·m) for revolute/prismatic joints. Like the motor's power limit.
> - `velocity` — maximum angular/linear speed. Prevents unrealistic instant accelerations.
> - `damping` — resistance to motion (like viscous friction). A joint with high damping feels like moving through honey.
> - `friction` — **static** friction: how much torque is needed to start moving the joint from rest.
> - **rpy** in `<origin>` — the orientation of the joint frame relative to the parent link. This is how you position the child link.

## The Robot Tree Structure

```
Every robot forms a TREE (not a loop):

base_link  ← ROOT (no parent)
├── left_wheel_link   (joint: continuous)
├── right_wheel_link  (joint: continuous)
├── caster_link       (joint: fixed)
│   └── caster_wheel  (joint: continuous)
├── lidar_link        (joint: fixed)
└── camera_link       (joint: fixed)
    └── camera_optical_frame  (joint: fixed)
```

> - URDF requires a **tree** structure — no cycles/loops. Every link (except `base_link`) has exactly one parent.
> - `base_link` is the root — it has no parent joint. All other links connect back to it.
> - The robot can have many **leaf** links (links with no children) — sensors, end effectors, etc.


# 7. Geometry — Shapes You Can Design

## All Available Shapes

```xml
<!-- ── BOX ────────────────────────────────────────────────────── -->
<geometry>
  <box size="lx ly lz"/>
  <!-- lx=length along X, ly=length along Y, lz=height along Z -->
  <!-- All in METRES -->
  <!-- Centered at the link's origin -->
  <!-- Example: <box size="0.3 0.2 0.1"/> = 30×20×10 cm box -->
</geometry>

<!-- ── CYLINDER ──────────────────────────────────────────────── -->
<geometry>
  <cylinder radius="r" length="l"/>
  <!-- r = radius in metres -->
  <!-- l = height/length in metres -->
  <!-- Oriented along Z axis by default (upright cylinder) -->
  <!-- To make a wheel (horizontal disc): rotate joint by 90° on X axis -->
  <!-- Example: <cylinder radius="0.05" length="0.02"/> = wheel shape -->
</geometry>

<!-- ── SPHERE ────────────────────────────────────────────────── -->
<geometry>
  <sphere radius="r"/>
  <!-- Perfect sphere centered at origin -->
  <!-- Example: <sphere radius="0.02"/> = 2cm radius ball -->
  <!-- Often used for caster wheels (frictionless ball) -->
</geometry>

<!-- ── MESH (3D model file) ──────────────────────────────────── -->
<geometry>
  <mesh filename="package://my_robot_pkg/meshes/robot_body.dae"
        scale="1.0 1.0 1.0"/>
  <!-- filename: path to a 3D mesh file -->
  <!--   package://pkg_name/path = looks in installed ROS2 package -->
  <!--   file:///absolute/path   = absolute filesystem path -->
  <!-- scale: resize the mesh. "1 1 1" = original size. "0.001 0.001 0.001" = mm→m -->
  <!-- Supported formats: .dae (Collada), .stl (STereoLithography), .obj -->
</geometry>
```

> - **Box** — the fastest collision shape. Use boxes for collision even when the visual is a mesh.
> - **Cylinder** — great for wheels, pillars, tubes. Remember: default orientation is **vertical** (along Z). Rotate 90° to make a horizontal wheel.
> - **Sphere** — perfect for caster wheels (passive rolling contact points). Very low friction in simulation.
> - **Mesh** — a 3D model designed in CAD software (Blender, SolidWorks, Fusion 360). The most realistic visual but **very expensive** as a collision shape. Always pair with a simple box/cylinder collision.
> - `.dae` — **Collada** format. The best for Gazebo: supports materials, textures, and hierarchies.
> - `.stl` — **ST**ereo**L**ithography. Very common in 3D printing. Supported by Gazebo but no material info.
> - `.obj` — Wavefront OBJ. Also supported. Simpler than Collada.
> - `package://` — ROS2 resource URI. Expands to the installed package's share directory after `colcon build`.

## Shape Comparison

```
Shape       CPU cost    Best used for
──────────────────────────────────────────────
Box         ⭐ lowest   Walls, bodies, flat surfaces
Cylinder    ⭐⭐ low     Wheels, pillars, cans
Sphere      ⭐⭐ low     Casters, balls, rounded corners
Mesh        ⭐⭐⭐⭐ high  Visual only — never for collision
```


# 8. Materials & Visual Appearance

## In URDF (basic colors)

```xml
<visual>
  <geometry>...</geometry>

  <!-- Method 1: named material with color -->
  <material name="robot_blue">
    <color rgba="0.1 0.3 0.8 1.0"/>
    <!-- R G B Alpha: each 0.0-1.0 -->
    <!-- Alpha: 1.0=opaque, 0.5=semi-transparent, 0.0=invisible -->
  </material>

  <!-- Method 2: reference a named material defined elsewhere -->
  <material name="robot_blue"/>
  <!-- If the material was already defined in the file, reuse it by name -->
</visual>
```

## In Gazebo block (full material control)

```xml
<gazebo reference="base_link">
<!-- reference: which link this Gazebo block applies to -->

  <material>Gazebo/Blue</material>
  <!-- Gazebo built-in material names: -->
  <!--   Gazebo/Red       Gazebo/Green      Gazebo/Blue   -->
  <!--   Gazebo/Yellow    Gazebo/Orange     Gazebo/Purple -->
  <!--   Gazebo/White     Gazebo/Black      Gazebo/Grey   -->
  <!--   Gazebo/DarkGrey  Gazebo/SkyBlue    Gazebo/Wood   -->
  <!--   Gazebo/Grass     Gazebo/Asphalt                  -->

  <visual>
    <material>
      <!-- Full OGRE material definition -->
      <!-- OGRE = Object-oriented Graphics Rendering Engine -->
      <!-- Used by Gazebo Classic for all rendering -->
      <ambient>0.1 0.3 0.8 1</ambient>
      <!-- Ambient: color under ambient light (dark areas) -->

      <diffuse>0.1 0.3 0.8 1</diffuse>
      <!-- Diffuse: main surface color under direct light -->
      <!-- This is the "base color" you see most of the time -->

      <specular>0.5 0.5 0.5 1</specular>
      <!-- Specular: highlight/reflection color (shiny spots) -->
      <!-- White specular = metallic/shiny. Black = matte -->

      <emissive>0.0 0.0 0.0 1</emissive>
      <!-- Emissive: glow color (like a LED — self-illuminated) -->
      <!-- Use for indicator lights: <emissive>1 0 0 1</emissive> = red glow -->
    </material>

    <transparency>0.0</transparency>
    <!-- 0.0 = fully opaque. 1.0 = fully transparent -->
    <!-- Different from URDF's rgba alpha! -->

    <cast_shadows>true</cast_shadows>
    <!-- Should this visual cast shadows on other objects? -->
  </visual>

  <self_collide>false</self_collide>
  <!-- false: parts of this model don't collide with each other -->
  <!-- true: enable self-collision (for robot arms that could hit themselves) -->

  <mu1>0.8</mu1>
  <!-- Friction coefficient direction 1 (Gazebo-specific) -->
  <mu2>0.8</mu2>
  <!-- Friction coefficient direction 2 -->

</gazebo>
```

> - **OGRE** = **O**bject-oriented **G**raphics **R**endering **E**ngine. The 3D rendering engine that Gazebo Classic uses internally. Material properties follow OGRE's lighting model.
> - **Ambient** — the base color when no direct light hits the surface. Simulates indirect/scattered light.
> - **Diffuse** — the color seen when a light source directly illuminates the surface. The most important color channel for appearance.
> - **Specular** — the bright highlight seen on shiny surfaces (like reflections). Pure white = mirror-like. Black = completely matte.
> - **Emissive** — makes the surface appear to glow from within. Doesn't actually emit light onto other objects — purely visual.
> - `<gazebo reference="link_name">` — extends a URDF link with Gazebo-specific properties. The URDF `<material>` only works in RViz2; for Gazebo you need this `<gazebo>` block.

## Color Reference (RGBA)

```
Color        R     G     B     A
─────────────────────────────────
Red          1.0   0.0   0.0   1.0
Green        0.0   1.0   0.0   1.0
Blue         0.0   0.0   1.0   1.0
Yellow       1.0   1.0   0.0   1.0
Orange       1.0   0.5   0.0   1.0
Purple       0.5   0.0   0.5   1.0
White        1.0   1.0   1.0   1.0
Black        0.0   0.0   0.0   1.0
Grey         0.5   0.5   0.5   1.0
Dark Grey    0.2   0.2   0.2   1.0
Semi-trans   0.0   0.0   1.0   0.5  ← Blue, 50% transparent
```


# 9. Physics — Mass, Inertia & Collision

## Choosing realistic mass values

```xml
<!-- ── Typical mass values for common robot parts ────────────── -->

<!-- Small ground robot (TurtleBot3-style) -->
<link name="base_link">
  <inertial>
    <mass value="1.3"/>    <!-- 1.3 kg total body -->
    <!-- ...inertia... -->
  </inertial>
</link>

<!-- Drive wheel -->
<link name="left_wheel">
  <inertial>
    <mass value="0.1"/>    <!-- 100g per wheel -->
  </inertial>
</link>

<!-- Caster wheel (passive, low friction) -->
<link name="caster">
  <inertial>
    <mass value="0.05"/>   <!-- 50g caster -->
  </inertial>
</link>

<!-- Battery (heaviest single component usually) -->
<link name="battery">
  <inertial>
    <mass value="0.8"/>    <!-- 800g LiPo battery -->
  </inertial>
</link>
```

## Collision surface tuning

```xml
<gazebo reference="left_wheel">
  <mu1>1.0</mu1>       <!-- high friction perpendicular to wheel axis -->
  <mu2>0.01</mu2>      <!-- very low friction along wheel axis (rolls freely) -->
  <!-- Anisotropic friction: different friction in two directions -->
  <!-- This prevents wheels from sliding sideways while rolling freely forward -->

  <kp>1e6</kp>         <!-- hard wheel (rubber is firm) -->
  <kd>10</kd>          <!-- moderate damping -->
  <minDepth>0.001</minDepth>
</gazebo>

<gazebo reference="caster_wheel">
  <mu1>0.0</mu1>       <!-- frictionless caster -->
  <mu2>0.0</mu2>
  <kp>1e6</kp>
  <kd>10</kd>
</gazebo>
```

> - **Anisotropic friction** — different friction coefficients in different directions. Real wheels have high rolling resistance (little) but very high lateral resistance (they don't slide sideways). `mu1` and `mu2` let you model this.
> - `mu1` — friction in the first direction (Gazebo defines this based on the contact geometry).
> - `mu2` — friction in the second direction (perpendicular to mu1).
> - **Caster wheel** — a passive swiveling wheel at the back/front of a differential drive robot. Zero friction = it rolls and pivots freely, supporting the robot without resisting turns.


# 10. Sensors in SDF/URDF

## Full LiDAR Definition

```xml
<!-- In URDF: first add a link for the LiDAR's physical position -->
<link name="lidar_link">
  <visual>
    <geometry>
      <cylinder radius="0.04" length="0.07"/>  <!-- LiDAR housing visual -->
    </geometry>
    <material name="black"><color rgba="0.1 0.1 0.1 1"/></material>
  </visual>
  <collision>
    <geometry>
      <cylinder radius="0.04" length="0.07"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.2"/>   <!-- 200g LiDAR sensor -->
    <inertia ixx="0.0001" ixy="0" ixz="0"
             iyy="0.0001" iyz="0" izz="0.0001"/>
  </inertial>
</link>

<!-- Fixed joint: LiDAR is rigidly mounted on top of the robot -->
<joint name="lidar_joint" type="fixed">
  <parent link="base_link"/>
  <child  link="lidar_link"/>
  <origin xyz="0 0 0.18" rpy="0 0 0"/>
  <!-- 18cm above base_link origin — on top of robot body -->
</joint>

<!-- Gazebo block: add the actual sensor simulation -->
<gazebo reference="lidar_link">
  <sensor type="ray" name="lidar_sensor">
  <!-- type="ray" = LiDAR (laser ranging) sensor -->

    <pose>0 0 0 0 0 0</pose>
    <!-- Sensor pose relative to the link's origin -->

    <always_on>true</always_on>
    <!-- Keep the sensor active even when simulation is paused -->

    <visualize>true</visualize>
    <!-- Show laser beam rays in Gazebo viewport (useful for debugging) -->
    <!-- Set false in production — rays cost rendering performance -->

    <update_rate>10</update_rate>
    <!-- Publish sensor data 10 times per second (10 Hz) -->

    <ray>
      <scan>
        <horizontal>
          <samples>360</samples>
          <!-- Number of laser beams = angular resolution -->
          <!-- 360 = one beam per degree for a full 360° scan -->
          <!-- 720 = half-degree resolution (more accurate but more data) -->

          <resolution>1</resolution>
          <!-- Sub-sample interpolation factor. 1 = no interpolation -->

          <min_angle>-3.14159265</min_angle>
          <!-- Start angle in radians: -π = -180° -->

          <max_angle>3.14159265</max_angle>
          <!-- End angle in radians: +π = +180° -->
          <!-- Together: full 360° scan -->
        </horizontal>

        <!-- Optional: vertical scan layers (3D LiDAR) -->
        <!--
        <vertical>
          <samples>16</samples>      16 vertical layers (like Velodyne VLP-16)
          <min_angle>-0.2618</min_angle>   -15°
          <max_angle>0.2618</max_angle>    +15°
        </vertical>
        -->
      </scan>

      <range>
        <min>0.12</min>
        <!-- Minimum valid range in metres — closer = invalid (0 or NaN) -->

        <max>8.0</max>
        <!-- Maximum valid range in metres — further = inf -->

        <resolution>0.015</resolution>
        <!-- Range measurement resolution in metres (distance precision) -->
        <!-- 0.015m = 1.5cm precision -->
      </range>

      <noise>
        <type>gaussian</type>
        <!-- Add realistic measurement noise -->
        <!-- "gaussian" = normally distributed noise (most realistic) -->
        <!-- "none" = perfect sensor (unrealistic but useful for testing) -->
        <mean>0.0</mean>       <!-- noise mean: 0 = unbiased -->
        <stddev>0.01</stddev>  <!-- standard deviation: ±1cm noise -->
        <!-- 68% of readings within ±1cm, 95% within ±2cm -->
      </noise>
    </ray>

    <plugin name="lidar_plugin" filename="libgazebo_ros_ray_sensor.so">
    <!-- The ROS2 bridge plugin that publishes LaserScan messages -->

      <ros>
        <remapping>~/out:=/scan</remapping>
        <!-- Remap the plugin's output topic to /scan -->
        <!-- ~/out is the plugin's default topic name -->
        <!-- :=/scan changes it to the standard ROS2 LiDAR topic -->
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
      <!-- What ROS2 message type to publish -->
      <!-- Alternative: sensor_msgs/PointCloud2 for 3D LiDAR -->

      <frame_name>lidar_link</frame_name>
      <!-- Which TF frame to use in message headers -->
      <!-- Must match the link name defined in URDF -->
    </plugin>

  </sensor>
</gazebo>
```

> - **Gaussian noise** — random error following a normal (bell curve) distribution. Real LiDARs have this. Adding noise makes your simulation-trained code more robust on real hardware.
> - **standard deviation** (stddev) — how spread out the noise is. `stddev=0.01` means 68% of readings are within ±1cm of truth. Typical cheap LiDAR: 1-3cm stddev. High-end: <5mm.
> - `<visualize>true</visualize>` — draws the laser rays in the viewport as colored lines. Very useful when debugging sensor coverage but expensive.
> - `<always_on>true</always_on>` — if false, the sensor stops when the simulation is paused or the model is static. Keep true for most cases.
> - **Velodyne VLP-16** — a popular 16-layer 3D LiDAR sensor used in autonomous vehicles. The `<vertical>` block simulates this type.

## Full Camera Definition

```xml
<link name="camera_link">
  <visual>
    <geometry><box size="0.03 0.04 0.03"/></geometry>
    <!-- Small box visual representing the camera body -->
    <material name="dark"><color rgba="0.1 0.1 0.1 1.0"/></material>
  </visual>
  <collision>
    <geometry><box size="0.03 0.04 0.03"/></geometry>
  </collision>
  <inertial>
    <mass value="0.05"/>   <!-- 50g camera -->
    <inertia ixx="0.000001" ixy="0" ixz="0"
             iyy="0.000001" iyz="0" izz="0.000001"/>
  </inertial>
</link>

<joint name="camera_joint" type="fixed">
  <parent link="base_link"/>
  <child  link="camera_link"/>
  <origin xyz="0.15 0 0.1" rpy="0 0 0"/>
  <!-- 15cm forward, 10cm up from robot center -->
</joint>

<!-- Camera looks forward: add an optical frame with correct orientation -->
<!-- (camera optical convention: Z forward, X right, Y down) -->
<joint name="camera_optical_joint" type="fixed">
  <parent link="camera_link"/>
  <child  link="camera_optical_frame"/>
  <origin xyz="0 0 0" rpy="-1.5707 0 -1.5707"/>
  <!-- This rotation converts from ROS frame (X forward, Y left, Z up) -->
  <!-- to camera optical frame (Z forward, X right, Y down) -->
</joint>

<link name="camera_optical_frame"/>
<!-- Empty link — just a coordinate frame for the image data -->

<gazebo reference="camera_link">
  <sensor type="camera" name="camera_sensor">

    <update_rate>30</update_rate>   <!-- 30 fps -->

    <camera name="camera">
      <horizontal_fov>1.3962634</horizontal_fov>
      <!-- Horizontal Field of View in radians -->
      <!-- 1.3962634 rad = 80° — typical webcam/robot camera -->
      <!-- Narrow: 0.5rad (28°) for telephoto. Wide: 2.0rad (115°) for fisheye -->

      <image>
        <width>640</width>    <!-- pixels horizontal -->
        <height>480</height>  <!-- pixels vertical -->
        <!-- VGA resolution: standard starting point -->
        <!-- Higher res = more detail but MUCH more data on /camera/image_raw -->
        <!-- 1280×720 (HD) → 4× the data of 640×360 -->

        <format>R8G8B8</format>
        <!-- Pixel format: R8G8B8 = RGB, 8 bits each = 24-bit color -->
        <!-- Other options: L8 (grayscale), BAYER_BGGR8 (raw bayer) -->
      </image>

      <clip>
        <near>0.1</near>
        <!-- Near clipping plane: objects closer than 10cm are not rendered -->
        <far>100</far>
        <!-- Far clipping plane: objects further than 100m are not rendered -->
        <!-- Increasing far costs GPU performance -->
      </clip>

      <noise>
        <type>gaussian</type>
        <mean>0.0</mean>
        <stddev>0.007</stddev>   <!-- per-pixel noise: subtle grain -->
      </noise>

      <distortion>
      <!-- Lens distortion simulation (barrel/pincushion) -->
        <k1>-0.25</k1>  <!-- radial distortion coefficient 1 -->
        <k2>0.12</k2>   <!-- radial distortion coefficient 2 -->
        <k3>0.0</k3>    <!-- radial distortion coefficient 3 -->
        <p1>-0.0001</p1> <!-- tangential distortion coefficient 1 -->
        <p2>0.0</p2>     <!-- tangential distortion coefficient 2 -->
        <center>0.5 0.5</center>  <!-- distortion center (normalized) -->
      </distortion>
    </camera>

    <plugin name="camera_plugin" filename="libgazebo_ros_camera.so">
      <ros>
        <remapping>image_raw:=/camera/image_raw</remapping>
        <remapping>camera_info:=/camera/camera_info</remapping>
      </ros>
      <camera_name>camera</camera_name>
      <frame_name>camera_optical_frame</frame_name>
      <!-- Must match the optical frame link name defined above -->
    </plugin>

  </sensor>
</gazebo>
```

> - **Field of View (FOV)** — the angular extent of the visible world. Wide FOV = more context, more distortion. Narrow FOV = longer range, less context.
> - **Clipping planes** — near/far boundaries of the rendered scene. Objects outside these bounds are invisible. Near plane prevents z-fighting (flickering when surfaces overlap).
> - **Lens distortion** — real camera lenses distort the image. `k1, k2, k3` are radial distortion coefficients (barrel distortion makes images look rounded). Adding distortion makes sim images more realistic.
> - **camera_optical_frame** — a ROS convention: camera data is published in a frame where **Z points forward, X points right, Y points down**. This differs from the ROS standard (X forward, Y left, Z up). The `-90° rotation` on the joint converts between them.
> - `/camera/camera_info` — camera calibration parameters: focal length, principal point, distortion coefficients. Used by computer vision algorithms to correct distortion.

## Differential Drive Plugin (Motor Simulation)

```xml
<gazebo>
  <plugin name="differential_drive" filename="libgazebo_ros_diff_drive.so">
  <!-- This plugin simulates the differential drive drivetrain -->
  <!-- It reads /cmd_vel and drives the wheels accordingly -->
  <!-- It publishes /odom with the estimated position -->

    <!-- ── Wheel joints ─────────────────────────────────────── -->
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <!-- Must match EXACTLY the joint names defined in your URDF -->

    <!-- ── Robot geometry ──────────────────────────────────── -->
    <wheel_separation>0.24</wheel_separation>
    <!-- Distance between the centers of left and right wheels (metres) -->
    <!-- Critical for correct turning radius calculation -->

    <wheel_diameter>0.1</wheel_diameter>
    <!-- Diameter (not radius!) of the wheels in metres -->
    <!-- Used to convert wheel angular velocity → linear velocity -->

    <!-- ── Velocity limits ──────────────────────────────────── -->
    <max_wheel_torque>20</max_wheel_torque>
    <!-- Maximum motor torque in Newton-metres (N·m) -->

    <max_wheel_acceleration>1.0</max_wheel_acceleration>
    <!-- Maximum wheel angular acceleration (rad/s²) -->
    <!-- Prevents instantaneous velocity changes (unrealistic) -->

    <!-- ── Odometry settings ─────────────────────────────────── -->
    <publish_odom>true</publish_odom>
    <!-- Publish estimated position to /odom -->

    <publish_odom_tf>true</publish_odom_tf>
    <!-- Publish the odom → base_link TF transform -->

    <publish_wheel_tf>false</publish_wheel_tf>
    <!-- Publish wheel joint TF transforms (usually false) -->

    <odometry_frame>odom</odometry_frame>
    <!-- Name of the odometry coordinate frame -->

    <robot_base_frame>base_link</robot_base_frame>
    <!-- Name of the robot base coordinate frame -->
    <!-- Must match your URDF's root link name -->

    <!-- ── ROS2 topics ───────────────────────────────────────── -->
    <ros>
      <remapping>cmd_vel:=/cmd_vel</remapping>
      <remapping>odom:=/odom</remapping>
    </ros>

  </plugin>
</gazebo>
```

> - **differential drive** — the most common mobile robot locomotion. Two driven wheels on the same axis. Speed difference between wheels causes turning. Named after the mathematical **differential** operation.
> - `wheel_separation` — the **wheelbase** (lateral distance between wheel centers). Getting this wrong causes incorrect odometry (the robot thinks it turns less/more than it does).
> - `wheel_diameter` — used in the formula: `linear_speed = (angular_speed × diameter) / 2`. Getting this wrong causes incorrect speed and odometry.
> - `max_wheel_acceleration` — models motor inertia. Real motors can't change speed instantly. This limit makes simulation more realistic and prevents instability.
> - `publish_odom_tf` — if true, the plugin broadcasts the `odom → base_link` transform on `/tf`. Set false if you have a separate odometry node to avoid TF conflicts.


# 12. Xacro — Writing Smarter URDF

**Xacro** (**X**ML **macro**s) is a preprocessor for URDF.
It adds variables, math, conditionals, and reusable macros to XML.

```bash
# Xacro processes your .urdf.xacro file and outputs standard URDF XML
xacro robot.urdf.xacro > robot.urdf

# Or in a launch file (processed at launch time):
robot_description = Command(['xacro ', urdf_file])
```

## Variables (Properties)

```xml
<?xml version="1.0"?>
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
<!-- xmlns:xacro declares the xacro namespace prefix -->
<!-- Every xacro tag starts with xacro: -->

  <!-- ── Define variables ──────────────────────────────────── -->
  <xacro:property name="robot_name"      value="my_robot"/>
  <xacro:property name="base_length"     value="0.30"/>   <!-- metres -->
  <xacro:property name="base_width"      value="0.20"/>
  <xacro:property name="base_height"     value="0.10"/>
  <xacro:property name="wheel_radius"    value="0.05"/>
  <xacro:property name="wheel_thickness" value="0.02"/>
  <xacro:property name="wheel_mass"      value="0.1"/>
  <xacro:property name="base_mass"       value="2.0"/>
  <xacro:property name="wheelbase"       value="0.24"/>   <!-- wheel separation -->

  <!-- ── Use variables with ${} syntax ─────────────────────── -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="${base_length} ${base_width} ${base_height}"/>
        <!-- ${var} inserts the variable's value -->
      </geometry>
    </visual>
    <inertial>
      <mass value="${base_mass}"/>
    </inertial>
  </link>

</robot>
```

> - `xmlns:xacro="..."` — **XML namespace declaration**. Required in the `<robot>` tag. Declares that `xacro:` prefix belongs to the xacro namespace.
> - `<xacro:property>` — defines a **constant**. Like `const` in C++. Set once, use everywhere.
> - `${variable_name}` — **variable substitution**: replaced by the variable's value when xacro runs.
> - Changing `wheel_radius` in one place automatically updates **all** wheels — no need to find and replace throughout the file.

## Math Expressions

```xml
<!-- Xacro supports Python math expressions inside ${} -->

<xacro:property name="pi"            value="3.14159265"/>
<xacro:property name="wheel_radius"  value="0.05"/>
<xacro:property name="base_height"   value="0.10"/>
<xacro:property name="wheelbase"     value="0.24"/>

<!-- Using math: -->
<origin xyz="0 ${wheelbase/2} ${wheel_radius - base_height/2}" rpy="${-pi/2} 0 0"/>
<!--               ↑                ↑                               ↑
           wheelbase/2 = 0.12   wheel height calc              -90° rotation  -->

<!-- More examples: -->
<box size="${2 * wheel_radius} ${2 * wheel_radius} ${wheel_thickness}"/>
<mass value="${wheel_mass * 2}"/>   <!-- could do arithmetic -->
<limit lower="${-pi}" upper="${pi}"/>
```

> - Math inside `${}` is evaluated as **Python expressions**. Any valid Python math works: `+`, `-`, `*`, `/`, `**` (power), `sqrt()`, `sin()`, `cos()`.
> - This is how you compute joint positions relative to geometry automatically — no manual calculation needed.

## Macros (Reusable Templates)

```xml
<!-- ── Define a wheel macro ──────────────────────────────────── -->
<xacro:macro name="wheel" params="prefix x_pos y_pos">
<!-- name: the macro name (used to call it) -->
<!-- params: space-separated list of parameters (like function arguments) -->
<!-- prefix: "left" or "right" — gives unique names -->
<!-- x_pos, y_pos: wheel position relative to base_link -->

  <!-- Link with prefix in name: "left_wheel" or "right_wheel" -->
  <link name="${prefix}_wheel">
    <visual>
      <geometry>
        <cylinder radius="${wheel_radius}" length="${wheel_thickness}"/>
      </geometry>
      <material name="${prefix}_wheel_color">
        <color rgba="0.1 0.1 0.1 1.0"/>  <!-- dark rubber color -->
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="${wheel_radius}" length="${wheel_thickness}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="${wheel_mass}"/>
      <inertia
        ixx="${(1/12) * wheel_mass * (3 * wheel_radius**2 + wheel_thickness**2)}"
        ixy="0" ixz="0"
        iyy="${(1/12) * wheel_mass * (3 * wheel_radius**2 + wheel_thickness**2)}"
        iyz="0"
        izz="${(1/2) * wheel_mass * wheel_radius**2}"/>
      <!-- Inertia calculated from formula automatically! -->
    </inertial>
  </link>

  <!-- Joint connecting wheel to base -->
  <joint name="${prefix}_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child  link="${prefix}_wheel"/>
    <origin xyz="${x_pos} ${y_pos} 0" rpy="${-pi/2} 0 0"/>
    <!-- -pi/2 rotates the cylinder from vertical to horizontal -->
    <axis xyz="0 0 1"/>
    <dynamics damping="0.1" friction="0.05"/>
  </joint>

  <!-- Gazebo physics for this wheel -->
  <gazebo reference="${prefix}_wheel">
    <mu1>1.0</mu1>
    <mu2>0.01</mu2>
    <kp>1e6</kp>
    <kd>10</kd>
    <material>Gazebo/DarkGrey</material>
  </gazebo>

</xacro:macro>


<!-- ── Call the macro (instantiate two wheels) ───────────────── -->
<xacro:wheel prefix="left"  x_pos="0"  y_pos="${ wheelbase/2}"/>
<xacro:wheel prefix="right" x_pos="0"  y_pos="${-wheelbase/2}"/>
<!-- This generates ALL the XML for both wheels from 2 lines! -->
```

> - `<xacro:macro name="X" params="a b c">` — defines a **macro**: a reusable block of XML with parameters. Like a function in programming.
> - `<xacro:X param1="val1" param2="val2"/>` — **calls** the macro, inserting the generated XML at that point.
> - Parameters can be any string — xacro substitutes them with `${param_name}` inside the macro body.
> - Using macros for wheels: instead of copy-pasting 40 lines twice and manually changing "left"/"right" everywhere, you define it once and call it twice.

## Including Other Files

```xml
<!-- Split your robot into multiple files -->

<!-- main robot file: my_robot.urdf.xacro -->
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Include shared properties -->
  <xacro:include filename="$(find my_robot_pkg)/urdf/properties.xacro"/>

  <!-- Include subsystems -->
  <xacro:include filename="$(find my_robot_pkg)/urdf/base.xacro"/>
  <xacro:include filename="$(find my_robot_pkg)/urdf/wheels.xacro"/>
  <xacro:include filename="$(find my_robot_pkg)/urdf/sensors.xacro"/>
  <xacro:include filename="$(find my_robot_pkg)/urdf/gazebo.xacro"/>

</robot>
```

> - `$(find package_name)` — xacro's way to find a ROS2 package's path. Expands to the absolute filesystem path. Different from `${variable}` — uses `$()` not `${}`.
> - Splitting into files makes large robots manageable. A real robot might have: `base.xacro`, `arm.xacro`, `gripper.xacro`, `sensors.xacro`, `gazebo_plugins.xacro`.

## Conditional Logic

```xml
<xacro:property name="use_camera" value="true"/>
<xacro:property name="use_lidar"  value="true"/>

<!-- Include sensor only if property is true -->
<xacro:if value="${use_camera}">
  <xacro:include filename="camera.xacro"/>
</xacro:if>

<xacro:unless value="${use_lidar}">
  <!-- This block appears only when use_lidar is FALSE -->
  <xacro:include filename="no_lidar_placeholder.xacro"/>
</xacro:unless>
```

> - `<xacro:if value="${condition}">` — includes content only if condition evaluates to true.
> - `<xacro:unless value="${condition}">` — the opposite: includes content only if false.
> - Useful for: sensor configurations, robot variants (with/without arm), debug helpers.


# 13. Complete Robot Design — Step by Step

A complete differential drive robot with LiDAR, camera, and all physics.

```xml
<?xml version="1.0"?>
<robot name="burger_bot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- ════════════════════════════════════════════════════════════
       SECTION 1: PROPERTIES (all measurements in one place)
  ════════════════════════════════════════════════════════════ -->
  <xacro:property name="pi"             value="3.14159265"/>

  <!-- Robot body -->
  <xacro:property name="base_length"    value="0.28"/>
  <xacro:property name="base_width"     value="0.16"/>
  <xacro:property name="base_height"    value="0.06"/>
  <xacro:property name="base_mass"      value="1.0"/>

  <!-- Wheels -->
  <xacro:property name="wheel_radius"   value="0.033"/>
  <xacro:property name="wheel_thick"    value="0.018"/>
  <xacro:property name="wheel_mass"     value="0.05"/>
  <xacro:property name="wheelbase"      value="0.16"/>

  <!-- Caster -->
  <xacro:property name="caster_radius"  value="0.015"/>
  <xacro:property name="caster_mass"    value="0.02"/>
  <xacro:property name="caster_x"       value="-0.10"/>

  <!-- Sensors -->
  <xacro:property name="lidar_height"   value="0.15"/>
  <xacro:property name="camera_x"       value="0.12"/>
  <xacro:property name="camera_z"       value="0.06"/>

  <!-- ════════════════════════════════════════════════════════════
       SECTION 2: BASE LINK (robot body)
  ════════════════════════════════════════════════════════════ -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 ${base_height/2}" rpy="0 0 0"/>
      <geometry>
        <box size="${base_length} ${base_width} ${base_height}"/>
      </geometry>
      <material name="robot_body_color">
        <color rgba="0.4 0.4 0.8 1.0"/>   <!-- Blue-grey -->
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 ${base_height/2}" rpy="0 0 0"/>
      <geometry>
        <box size="${base_length} ${base_width} ${base_height}"/>
      </geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 ${base_height/2}" rpy="0 0 0"/>
      <mass value="${base_mass}"/>
      <inertia
        ixx="${(1/12)*base_mass*(base_width**2  + base_height**2)}"
        ixy="0" ixz="0"
        iyy="${(1/12)*base_mass*(base_length**2 + base_height**2)}"
        iyz="0"
        izz="${(1/12)*base_mass*(base_length**2 + base_width**2)}"/>
    </inertial>
  </link>

  <!-- ════════════════════════════════════════════════════════════
       SECTION 3: WHEEL MACRO + INSTANTIATION
  ════════════════════════════════════════════════════════════ -->
  <xacro:macro name="wheel" params="prefix y_sign">

    <link name="${prefix}_wheel">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_thick}"/>
        </geometry>
        <material name="wheel_color">
          <color rgba="0.15 0.15 0.15 1.0"/>
        </material>
      </visual>
      <collision>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_thick}"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="${wheel_mass}"/>
        <inertia
          ixx="${(1/12)*wheel_mass*(3*wheel_radius**2 + wheel_thick**2)}"
          ixy="0" ixz="0"
          iyy="${(1/12)*wheel_mass*(3*wheel_radius**2 + wheel_thick**2)}"
          iyz="0"
          izz="${0.5*wheel_mass*wheel_radius**2}"/>
      </inertial>
    </link>

    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="base_link"/>
      <child  link="${prefix}_wheel"/>
      <origin xyz="0 ${y_sign * wheelbase/2} ${wheel_radius}" rpy="${-pi/2} 0 0"/>
      <axis xyz="0 0 1"/>
      <dynamics damping="0.1" friction="0.0"/>
    </joint>

    <gazebo reference="${prefix}_wheel">
      <mu1>1.0</mu1>
      <mu2>0.01</mu2>
      <kp>1e6</kp>
      <kd>10</kd>
      <material>Gazebo/Black</material>
    </gazebo>

  </xacro:macro>

  <!-- Instantiate left and right wheels -->
  <xacro:wheel prefix="left"  y_sign=" 1"/>
  <xacro:wheel prefix="right" y_sign="-1"/>

  <!-- ════════════════════════════════════════════════════════════
       SECTION 4: CASTER WHEEL (passive ball)
  ════════════════════════════════════════════════════════════ -->
  <link name="caster_link">
    <visual>
      <geometry><sphere radius="${caster_radius}"/></geometry>
      <material name="caster_color">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry><sphere radius="${caster_radius}"/></geometry>
    </collision>
    <inertial>
      <mass value="${caster_mass}"/>
      <inertia
        ixx="${0.4*caster_mass*caster_radius**2}" ixy="0" ixz="0"
        iyy="${0.4*caster_mass*caster_radius**2}" iyz="0"
        izz="${0.4*caster_mass*caster_radius**2}"/>
    </inertial>
  </link>

  <joint name="caster_joint" type="fixed">
    <parent link="base_link"/>
    <child  link="caster_link"/>
    <origin xyz="${caster_x} 0 ${caster_radius}" rpy="0 0 0"/>
  </joint>

  <gazebo reference="caster_link">
    <mu1>0.0</mu1>   <!-- frictionless ball caster -->
    <mu2>0.0</mu2>
    <material>Gazebo/Grey</material>
  </gazebo>

  <!-- ════════════════════════════════════════════════════════════
       SECTION 5: LiDAR SENSOR
  ════════════════════════════════════════════════════════════ -->
  <link name="lidar_link">
    <visual>
      <geometry><cylinder radius="0.04" length="0.06"/></geometry>
      <material name="lidar_color">
        <color rgba="0.05 0.05 0.05 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry><cylinder radius="0.04" length="0.06"/></geometry>
    </collision>
    <inertial>
      <mass value="0.18"/>
      <inertia ixx="0.0001" ixy="0" ixz="0"
               iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <joint name="lidar_joint" type="fixed">
    <parent link="base_link"/>
    <child  link="lidar_link"/>
    <origin xyz="0 0 ${base_height + lidar_height/2}" rpy="0 0 0"/>
  </joint>

  <gazebo reference="lidar_link">
    <sensor type="ray" name="lidar">
      <always_on>true</always_on>
      <visualize>false</visualize>
      <update_rate>10</update_rate>
      <ray>
        <scan>
          <horizontal>
            <samples>360</samples>
            <resolution>1</resolution>
            <min_angle>${-pi}</min_angle>
            <max_angle>${pi}</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.12</min>
          <max>3.5</max>
          <resolution>0.015</resolution>
        </range>
        <noise>
          <type>gaussian</type>
          <mean>0.0</mean>
          <stddev>0.01</stddev>
        </noise>
      </ray>
      <plugin name="lidar_plugin" filename="libgazebo_ros_ray_sensor.so">
        <ros><remapping>~/out:=/scan</remapping></ros>
        <output_type>sensor_msgs/LaserScan</output_type>
        <frame_name>lidar_link</frame_name>
      </plugin>
    </sensor>
  </gazebo>

  <!-- ════════════════════════════════════════════════════════════
       SECTION 6: DIFFERENTIAL DRIVE PLUGIN
  ════════════════════════════════════════════════════════════ -->
  <gazebo>
    <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
      <left_joint>left_wheel_joint</left_joint>
      <right_joint>right_wheel_joint</right_joint>
      <wheel_separation>${wheelbase}</wheel_separation>
      <wheel_diameter>${2 * wheel_radius}</wheel_diameter>
      <max_wheel_torque>20</max_wheel_torque>
      <max_wheel_acceleration>1.0</max_wheel_acceleration>
      <publish_odom>true</publish_odom>
      <publish_odom_tf>true</publish_odom_tf>
      <odometry_frame>odom</odometry_frame>
      <robot_base_frame>base_link</robot_base_frame>
      <ros>
        <remapping>cmd_vel:=/cmd_vel</remapping>
        <remapping>odom:=/odom</remapping>
      </ros>
    </plugin>
  </gazebo>

</robot>
```

Build and visualize:
```bash
# Verify the URDF is valid
check_urdf my_robot.urdf

# Convert xacro → URDF and check
xacro my_robot.urdf.xacro > /tmp/robot.urdf
check_urdf /tmp/robot.urdf

# Launch in Gazebo
ros2 launch my_robot_pkg simulation.launch.py
```

> - `check_urdf` — a ROS2 command-line tool that validates URDF syntax and prints the robot tree. **Always run this after editing your URDF.** It catches missing joints, broken links, and syntax errors.


# 14. Complete World Design — Step by Step

```xml
<?xml version="1.0" ?>
<sdf version="1.6">
<world name="robot_arena">

  <!-- ── PHYSICS ──────────────────────────────────────────────── -->
  <physics type="ode">
    <real_time_update_rate>1000</real_time_update_rate>
    <max_step_size>0.001</max_step_size>
    <real_time_factor>1</real_time_factor>
    <gravity>0 0 -9.81</gravity>
  </physics>

  <!-- ── LIGHTING ─────────────────────────────────────────────── -->
  <include><uri>model://sun</uri></include>

  <!-- Custom directional light -->
  <light type="directional" name="main_light">
    <pose>0 0 20 0 0 0</pose>
    <diffuse>0.9 0.9 0.9 1</diffuse>
    <specular>0.3 0.3 0.3 1</specular>
    <direction>-0.5 0.1 -0.9</direction>
    <!-- direction: x y z vector the light shines toward -->
    <cast_shadows>true</cast_shadows>
  </light>

  <!-- ── GROUND ────────────────────────────────────────────────── -->
  <model name="ground">
    <static>true</static>
    <link name="ground_link">
      <collision name="ground_collision">
        <geometry>
          <plane>
            <normal>0 0 1</normal>   <!-- normal vector pointing up (Z) -->
            <size>50 50</size>       <!-- 50m × 50m ground plane -->
          </plane>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.9</mu>    <!-- concrete-like floor: high friction -->
              <mu2>0.9</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="ground_visual">
        <geometry>
          <plane>
            <normal>0 0 1</normal>
            <size>50 50</size>
          </plane>
        </geometry>
        <material>
          <script>
            <uri>file://media/materials/scripts/gazebo.material</uri>
            <name>Gazebo/Asphalt</name>   <!-- tiled asphalt texture -->
          </script>
        </material>
      </visual>
    </link>
  </model>

  <!-- ── BOUNDARY WALLS ────────────────────────────────────────── -->
  <model name="north_wall">
    <static>true</static>
    <pose>0 5 0.5 0 0 0</pose>
    <link name="link">
      <collision name="c">
        <geometry><box><size>10 0.2 1.0</size></box></geometry>
      </collision>
      <visual name="v">
        <geometry><box><size>10 0.2 1.0</size></box></geometry>
        <material>
          <ambient>0.7 0.7 0.7 1</ambient>
          <diffuse>0.7 0.7 0.7 1</diffuse>
        </material>
      </visual>
    </link>
  </model>

  <!-- South wall (mirror of north) -->
  <model name="south_wall">
    <static>true</static>
    <pose>0 -5 0.5 0 0 0</pose>
    <link name="link">
      <collision name="c">
        <geometry><box><size>10 0.2 1.0</size></box></geometry>
      </collision>
      <visual name="v">
        <geometry><box><size>10 0.2 1.0</size></box></geometry>
        <material><ambient>0.7 0.7 0.7 1</ambient></material>
      </visual>
    </link>
  </model>

  <!-- ── OBSTACLES ─────────────────────────────────────────────── -->
  <model name="pillar_1">
    <static>true</static>
    <pose>2 1 0 0 0 0</pose>
    <link name="link">
      <collision name="c">
        <geometry><cylinder><radius>0.15</radius><length>1.0</length></cylinder></geometry>
      </collision>
      <visual name="v">
        <geometry><cylinder><radius>0.15</radius><length>1.0</length></cylinder></geometry>
        <material><ambient>0.8 0.2 0.2 1</ambient></material>  <!-- red -->
      </visual>
    </link>
  </model>

  <!-- Dynamic box (falls when hit!) -->
  <model name="falling_box">
    <static>false</static>   <!-- dynamic! responds to physics -->
    <pose>0 2 0.5 0 0 0.3</pose>   <!-- slightly rotated so it tips easily -->
    <link name="link">
      <collision name="c">
        <geometry><box><size>0.3 0.3 0.3</size></box></geometry>
        <surface>
          <friction><ode><mu>0.5</mu><mu2>0.5</mu2></ode></friction>
        </surface>
      </collision>
      <visual name="v">
        <geometry><box><size>0.3 0.3 0.3</size></box></geometry>
        <material><ambient>0.2 0.8 0.2 1</ambient></material>  <!-- green -->
      </visual>
      <inertial>
        <mass>0.5</mass>     <!-- 500g box -->
        <inertia ixx="0.0038" ixy="0" ixz="0"
                 iyy="0.0038" iyz="0" izz="0.0038"/>
        <!-- Inertia for a 0.3m cube: (1/6) * 0.5 * 0.3² = 0.0075 ... -->
      </inertial>
    </link>
  </model>

</world>
</sdf>
```

Launch it:
```bash
gazebo my_arena.world
# or
ros2 launch gazebo_ros gazebo.launch.py world:=/path/to/my_arena.world
```


# 15. SDF vs URDF — When to Use Which

| Feature | URDF | SDF |
|---|---|---|
| Robot description |  Yes |  Yes |
| World description |  No |  Yes |
| Used by ROS2 natively |  Yes | ️ Need conversion |
| Used by Gazebo natively | ️ Converted internally |  Yes |
| Supports xacro |  Yes |  No |
| Friction, contacts | ️ Via `<gazebo>` block |  Native |
| Multi-body worlds |  No |  Yes |
| Sensor definitions | ️ Via `<gazebo>` block |  Native |
| Nested models |  No |  Yes |
| Fuel model library |  No |  Yes |

**Use URDF when:** writing a robot for ROS2 (with xacro for reuse).
**Use SDF when:** designing worlds, obstacles, props, or using Gazebo Harmonic.


# 16. Cheat Sheet & Tag Reference

## URDF Tag Reference

| Tag | Purpose | Key attributes |
|---|---|---|
| `<robot>` | Root element | `name` |
| `<link>` | Rigid body part | `name` |
| `<joint>` | Connection between links | `name`, `type` |
| `<visual>` | Rendered shape | — |
| `<collision>` | Physics shape | — |
| `<inertial>` | Mass properties | — |
| `<origin>` | Position+rotation offset | `xyz`, `rpy` |
| `<geometry>` | Shape container | — |
| `<box>` | Box shape | `size="lx ly lz"` |
| `<cylinder>` | Cylinder shape | `radius`, `length` |
| `<sphere>` | Sphere shape | `radius` |
| `<mesh>` | 3D model file | `filename`, `scale` |
| `<material>` | Visual color | `name` |
| `<color>` | RGBA color | `rgba="r g b a"` |
| `<mass>` | Link mass | `value` (kg) |
| `<inertia>` | Inertia tensor | `ixx iyy izz ixy ixz iyz` |
| `<parent>` | Parent link | `link` |
| `<child>` | Child link | `link` |
| `<axis>` | Joint rotation axis | `xyz` |
| `<limit>` | Joint limits | `lower upper effort velocity` |
| `<dynamics>` | Joint friction/damping | `damping friction` |
| `<gazebo>` | Gazebo extension | `reference` |

## SDF Tag Reference

| Tag | Purpose |
|---|---|
| `<sdf>` | Root element |
| `<world>` | The simulation world |
| `<physics>` | Physics engine settings |
| `<gravity>` | Gravity vector `x y z` |
| `<model>` | A model (robot/object) |
| `<static>` | Is it fixed? `true`/`false` |
| `<pose>` | Position+orientation `x y z r p y` |
| `<link>` | Rigid body |
| `<joint>` | Connection |
| `<sensor>` | Sensor definition |
| `<plugin>` | Behavior plugin |
| `<light>` | Light source |
| `<scene>` | Scene rendering settings |
| `<include>` | Include another model |
| `<uri>` | Resource path |

## Xacro Tag Reference

| Tag | Purpose |
|---|---|
| `<xacro:property name="x" value="1.0"/>` | Define variable |
| `${x}` | Use variable |
| `${x + y * 2}` | Math expression |
| `<xacro:macro name="M" params="a b">` | Define macro |
| `<xacro:M a="1" b="2"/>` | Call macro |
| `<xacro:include filename="..."/>` | Include file |
| `$(find pkg)` | Find ROS2 package path |
| `<xacro:if value="${cond}">` | Conditional include |
| `<xacro:unless value="${cond}">` | Inverse conditional |

## Abbreviation Glossary

| Abbreviation | Full form |
|---|---|
| `SDF` | Simulation Description Format |
| `URDF` | Unified Robot Description Format |
| `xacro` | XML Macros |
| `XML` | eXtensible Markup Language |
| `URI` | Uniform Resource Identifier |
| `ODE` | Open Dynamics Engine |
| `DART` | Dynamic Animation and Robotics Toolkit |
| `DOF` | Degrees Of Freedom |
| `FOV` | Field Of View |
| `RGB` | Red Green Blue |
| `RGBA` | Red Green Blue Alpha |
| `STL` | STereoLithography (3D format) |
| `DAE` | Collada Digital Asset Exchange (3D format) |
| `OGRE` | Object-oriented Graphics Rendering Engine |
| `rpy` | Roll Pitch Yaw |
| `mu` (μ) | Coulomb friction coefficient |
| `kp` | Spring stiffness (contact) |
| `kd` | Damping coefficient (contact) |
| `N·m` | Newton-metres (torque unit) |
| `rad/s` | Radians per second |
| `m/s²` | Metres per second squared (acceleration) |
