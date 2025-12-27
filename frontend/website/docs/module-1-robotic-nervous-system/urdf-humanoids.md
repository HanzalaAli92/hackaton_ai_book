---
sidebar_position: 4
title: URDF for Humanoids
---

# URDF for Humanoids

In this section, we'll explore Unified Robot Description Format (URDF) and how it's used to model humanoid robots. URDF is an XML format for representing a robot model, including its physical and kinematic properties.

## Learning Objectives

By the end of this section, you will be able to:

- Create URDF files for humanoid robots
- Define robot links and joints
- Specify visual and collision properties
- Understand kinematic chains for humanoid structures

## Introduction to URDF

Unified Robot Description Format (URDF) is an XML format used in ROS to describe robot models. It specifies the physical structure of a robot, including its links, joints, and other properties necessary for simulation and control.

### Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot">
  <!-- Define links -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Define joints -->
  <joint name="joint_name" type="revolute">
    <parent link="base_link"/>
    <child link="child_link"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="1000" velocity="1"/>
  </joint>
</robot>
```

## Links in URDF

A link represents a rigid part of the robot. Each link can have:

- **Visual**: How the link appears in visualization
- **Collision**: How the link interacts in collision detection
- **Inertial**: Physical properties for physics simulation

### Link Example for Humanoid Robot

```xml
<link name="torso">
  <visual>
    <geometry>
      <box size="0.2 0.1 0.4"/>
    </geometry>
    <material name="light_grey">
      <color rgba="0.7 0.7 0.7 1"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.2 0.1 0.4"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="2.0"/>
    <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.02"/>
  </inertial>
</link>
```

## Joints in URDF

Joints connect links and define the relationship between them. Common joint types:

- **Revolute**: Rotational joint with limited range
- **Continuous**: Rotational joint without limits
- **Prismatic**: Linear sliding joint
- **Fixed**: No movement between links

### Joint Example for Humanoid Robot

```xml
<joint name="torso_head_joint" type="revolute">
  <parent link="torso"/>
  <child link="head"/>
  <origin xyz="0 0 0.2" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="30" velocity="1.0"/>
</joint>
```

## Complete Humanoid Robot URDF Example

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.4"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.02"/>
    </inertial>
  </link>

  <!-- Head -->
  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="skin_color">
        <color rgba="1.0 0.8 0.6 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.0033" ixy="0.0" ixz="0.0" iyy="0.0033" iyz="0.0" izz="0.0033"/>
    </inertial>
  </link>

  <!-- Joint connecting torso to head -->
  <joint name="torso_head_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.25" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="10" velocity="1.0"/>
  </joint>

  <!-- Left Arm -->
  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Joint connecting torso to left arm -->
  <joint name="torso_left_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.15 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
  </joint>
</robot>
```

## URDF for Bipedal Locomotion

Humanoid robots designed for bipedal locomotion have specific kinematic chains that enable walking. These typically include:

- **Leg chains**: Hip, knee, and ankle joints
- **Arm chains**: Shoulder, elbow, and wrist joints for balance
- **Trunk**: Torso with head for perception and upper body control

### Visualizing URDF Models

URDF models can be visualized in various tools:

- **RViz**: ROS visualization tool
- **Gazebo**: Physics simulation environment
- **Blender**: With URDF import plugins

## Practical Exercise

Create a simplified URDF model for a humanoid robot with at least 12 degrees of freedom (DOF) suitable for bipedal walking.

## Summary

In this section, we covered:

- Basic structure of URDF files
- Defining links with visual, collision, and inertial properties
- Creating joints to connect robot parts
- Designing humanoid-specific structures
- Examples of complete humanoid URDF models

URDF forms the foundation for modeling humanoid robots in ROS, enabling simulation, visualization, and control of complex robotic systems.