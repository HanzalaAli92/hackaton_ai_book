---
sidebar_position: 2
title: Gazebo Simulation
---

# Gazebo Simulation

In this section, we'll explore Gazebo, a physics-based simulation environment that enables realistic modeling of robotic systems. Gazebo provides high-fidelity physics simulation, sensor simulation, and rendering capabilities essential for robotics development.

## Learning Objectives

By the end of this section, you will be able to:

- Set up Gazebo simulation environments
- Configure physics engines for accurate simulation
- Implement collision detection and response
- Simulate various sensor types
- Integrate Gazebo with ROS 2 for robot control

## Introduction to Gazebo

Gazebo is a 3D simulation environment for robotics that provides:
- Accurate physics simulation using engines like ODE, Bullet, and Simbody
- High-quality rendering for realistic visualization
- Support for various sensors (LiDAR, cameras, IMUs, etc.)
- Integration with ROS/ROS 2 for robot control and simulation

## Gazebo World Structure

A Gazebo simulation consists of:
- **World file**: Defines the environment, physics parameters, and objects
- **Models**: Robot and object definitions in SDF (Simulation Description Format)
- **Plugins**: Custom code that extends Gazebo's functionality
- **Controllers**: ROS-based nodes that control robots in simulation

### Basic World File Example

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="default">
    <!-- Include the sun -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Include the ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Physics engine configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>

    <!-- Define a simple box -->
    <model name="box">
      <pose>0 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
            <diffuse>0.5 0.5 0.5 1</diffuse>
          </material>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

## Physics Simulation in Gazebo

Gazebo uses physics engines to simulate real-world physics. Key parameters include:

- **Gravity**: Typically set to -9.8 m/s² for Earth-like gravity
- **Time step**: Smaller steps increase accuracy but decrease performance
- **Real-time factor**: Controls simulation speed relative to real time

### Physics Configuration

```xml
<physics type="ode">
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>
  <gravity>0 0 -9.8</gravity>
  <ode>
    <solver>
      <type>quick</type>
      <iters>10</iters>
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

## Collision Detection and Response

Gazebo provides realistic collision detection and response through:

- **Collision geometry**: Defines the shape for collision detection
- **Surface properties**: Friction, restitution, and other contact properties
- **Contact sensors**: Detect when collisions occur

### Collision Model Example

```xml
<link name="link">
  <collision name="collision">
    <geometry>
      <mesh>
        <uri>model://my_robot/meshes/link.dae</uri>
      </mesh>
    </geometry>
    <surface>
      <friction>
        <ode>
          <mu>1.0</mu>
          <mu2>1.0</mu2>
        </ode>
      </friction>
      <bounce>
        <restitution_coefficient>0.1</restitution_coefficient>
        <threshold>100000</threshold>
      </bounce>
      <contact>
        <ode>
          <soft_cfm>0</soft_cfm>
          <soft_erp>0.2</soft_erp>
          <kp>1e+13</kp>
          <kd>1</kd>
          <max_vel>0.01</max_vel>
          <min_depth>0</min_depth>
        </ode>
      </contact>
    </surface>
  </collision>
</link>
```

## Sensor Simulation in Gazebo

Gazebo can simulate various sensors essential for robotics:

- **LiDAR**: Simulates laser range finders
- **Cameras**: RGB, depth, and stereo camera simulation
- **IMUs**: Inertial measurement units
- **Force/Torque sensors**: Measure forces and torques at joints

### LiDAR Sensor Example

```xml
<sensor name="lidar" type="ray">
  <pose>0.1 0 0.1 0 0 0</pose>
  <ray>
    <scan>
      <horizontal>
        <samples>720</samples>
        <resolution>1</resolution>
        <min_angle>-1.570796</min_angle>
        <max_angle>1.570796</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>30.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
    <ros>
      <namespace>/lidar</namespace>
      <remapping>~/out:=scan</remapping>
    </ros>
    <output_type>sensor_msgs/LaserScan</output_type>
  </plugin>
</sensor>
```

## ROS 2 Integration

Gazebo integrates with ROS 2 through plugins that enable communication between simulation and ROS 2 nodes:

- **gazebo_ros_pkgs**: Provides ROS 2 interfaces for Gazebo
- **Controllers**: Use ROS 2 messages to control simulated robots
- **Sensors**: Publish sensor data as ROS 2 messages

### Example ROS 2 Controller Integration

```xml
<plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
  <ros>
    <namespace>/robot</namespace>
  </ros>
  <left_joint>left_wheel_joint</left_joint>
  <right_joint>right_wheel_joint</right_joint>
  <wheel_separation>0.3</wheel_separation>
  <wheel_diameter>0.15</wheel_diameter>
  <command_topic>cmd_vel</command_topic>
  <odometry_topic>odom</odometry_topic>
  <odometry_frame>odom</odometry_frame>
  <robot_base_frame>base_link</robot_base_frame>
</plugin>
```

## Practical Exercise

Create a simple Gazebo world with a differential drive robot that includes:

1. A basic robot model with wheels
2. LiDAR sensor for environment mapping
3. Camera sensor for visual perception
4. ROS 2 integration for control and sensing

## Summary

In this section, we covered:

- Basic structure of Gazebo world files
- Physics simulation configuration
- Collision detection and response
- Sensor simulation in Gazebo
- Integration with ROS 2 for robot control

Gazebo provides a powerful platform for simulating robotic systems, allowing for testing and validation before physical deployment.