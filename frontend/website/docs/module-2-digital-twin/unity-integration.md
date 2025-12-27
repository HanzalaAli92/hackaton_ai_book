---
sidebar_position: 3
title: Unity Integration
---

# Unity Integration

In this section, we'll explore Unity as a simulation environment for robotics. Unity provides powerful rendering capabilities and physics simulation that can be used to create high-fidelity digital twins of robotic systems.

## Learning Objectives

By the end of this section, you will be able to:

- Set up Unity for robotics simulation
- Create realistic environments with high-fidelity rendering
- Integrate physics simulation for accurate robot behavior
- Implement sensor simulation in Unity
- Connect Unity simulation with ROS 2 using Unity Robotics Hub

## Introduction to Unity for Robotics

Unity is a powerful game engine that has been adapted for robotics simulation through the Unity Robotics Hub. It provides:

- High-quality real-time rendering for photorealistic simulation
- Physics simulation using NVIDIA PhysX
- Flexible scripting with C#
- Support for various sensors and actuators
- Integration with ROS/ROS 2 through Unity Robotics packages

## Unity Robotics Hub

The Unity Robotics Hub provides essential tools for robotics simulation:

- **ROS-TCP-Connector**: Enables communication between Unity and ROS/ROS 2
- **ROS-TCP-Endpoint**: Handles message serialization and communication
- **Robotics packages**: Pre-built components for common robotic tasks

### Setting up Unity for Robotics

1. Install Unity Hub and Unity 2021.3 LTS or later
2. Install the Unity Robotics Hub
3. Import the ROS-TCP-Connector package
4. Configure network settings for ROS communication

### Basic Unity Scene Setup

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;

public class RobotController : MonoBehaviour
{
    // ROS Connection
    private RosConnection ros;

    // Robot components
    public GameObject robotBase;
    public GameObject[] wheels;

    void Start()
    {
        // Connect to ROS
        ros = GetComponent<RosConnection>();
        ros.RegisterPublisher<Unity.Robotics.ROS.MessageGeneration.geometry_msgs.msg.Twist>("/cmd_vel");

        // Subscribe to sensor data
        ros.Subscribe<Unity.Robotics.ROS.MessageGeneration.sensor_msgs.msg.LaserScan>("/scan", OnLaserScan);
    }

    void OnLaserScan(Unity.Robotics.ROS.MessageGeneration.sensor_msgs.msg.LaserScan scanData)
    {
        // Process sensor data
        Debug.Log("Received laser scan with " + scanData.ranges.Length + " points");
    }

    void Update()
    {
        // Process robot control logic
    }
}
```

## Physics Simulation in Unity

Unity uses NVIDIA PhysX for physics simulation. Key parameters include:

- **Gravity**: Set in the Physics Manager
- **Fixed Timestep**: Controls physics update rate
- **Solver Iterations**: Affects physics accuracy

### Physics Configuration

```csharp
using UnityEngine;

public class PhysicsSetup : MonoBehaviour
{
    void Start()
    {
        // Configure physics parameters
        Physics.gravity = new Vector3(0, -9.81f, 0);
        Time.fixedDeltaTime = 0.02f; // 50 Hz physics update
    }
}
```

## Sensor Simulation in Unity

Unity can simulate various sensors essential for robotics:

### Camera Sensor

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector.ROSGeometry;
using SensorMsgs = Unity.Robotics.ROS.MessageGeneration;

public class CameraSensor : MonoBehaviour
{
    public Camera cameraComponent;
    private RosConnection ros;
    private int sequenceNumber = 0;

    void Start()
    {
        ros = GetComponent<RosConnection>();
    }

    void Update()
    {
        if (Time.frameCount % 30 == 0) // Publish every 30 frames
        {
            PublishImage();
        }
    }

    void PublishImage()
    {
        RenderTexture currentRT = RenderTexture.active;
        RenderTexture.active = cameraComponent.targetTexture;

        cameraComponent.Render();

        Texture2D imageTex = new Texture2D(cameraComponent.targetTexture.width,
                                          cameraComponent.targetTexture.height);
        imageTex.ReadPixels(new Rect(0, 0, cameraComponent.targetTexture.width,
                                    cameraComponent.targetTexture.height), 0, 0);
        imageTex.Apply();

        byte[] imageBytes = imageTex.EncodeToPNG();
        Destroy(imageTex);
        RenderTexture.active = currentRT;

        // Create and publish ROS message
        var imageMsg = new SensorMsgs.sensor_msgs.msg.Image();
        imageMsg.data = imageBytes;
        imageMsg.width = (uint)cameraComponent.targetTexture.width;
        imageMsg.height = (uint)cameraComponent.targetTexture.height;
        imageMsg.encoding = "rgb8";
        imageMsg.is_bigendian = 0;
        imageMsg.step = (uint)(3 * cameraComponent.targetTexture.width); // 3 bytes per pixel

        ros.Publish("/camera/image_raw", imageMsg);
    }
}
```

### LiDAR Sensor Simulation

```csharp
using UnityEngine;
using System.Collections.Generic;
using SensorMsgs = Unity.Robotics.ROS.MessageGeneration;

public class LidarSensor : MonoBehaviour
{
    public int resolution = 360; // Points per 360 degree scan
    public float maxRange = 10.0f;
    public float minRange = 0.1f;
    private RosConnection ros;

    void Start()
    {
        ros = GetComponent<RosConnection>();
    }

    void Update()
    {
        if (Time.time % 0.1f < Time.deltaTime) // Publish at 10Hz
        {
            SimulateLidarScan();
        }
    }

    void SimulateLidarScan()
    {
        List<float> ranges = new List<float>();

        for (int i = 0; i < resolution; i++)
        {
            float angle = Mathf.Deg2Rad * (i * 360.0f / resolution);
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));
            direction = transform.TransformDirection(direction);

            RaycastHit hit;
            if (Physics.Raycast(transform.position, direction, out hit, maxRange))
            {
                ranges.Add(hit.distance);
            }
            else
            {
                ranges.Add(maxRange);
            }
        }

        // Create and publish ROS LaserScan message
        var scanMsg = new SensorMsgs.sensor_msgs.msg.LaserScan();
        scanMsg.ranges = ranges.ToArray();
        scanMsg.angle_min = -Mathf.PI;
        scanMsg.angle_max = Mathf.PI;
        scanMsg.angle_increment = 2 * Mathf.PI / resolution;
        scanMsg.range_min = minRange;
        scanMsg.range_max = maxRange;
        scanMsg.time_increment = 0.0f; // Not simulated
        scanMsg.scan_time = 0.1f; // 10Hz

        ros.Publish("/scan", scanMsg);
    }
}
```

## High-Fidelity Rendering

Unity excels at high-fidelity rendering with features like:

- **PBR Materials**: Physically-based rendering for realistic surfaces
- **Lighting**: Realistic lighting with shadows and reflections
- **Post-processing**: Effects like bloom, depth of field, and color grading
- **Occlusion culling**: Optimizes rendering performance

### Material Setup for Realism

```csharp
using UnityEngine;

public class MaterialSetup : MonoBehaviour
{
    public Material[] robotMaterials;

    void Start()
    {
        foreach (Material mat in robotMaterials)
        {
            // Configure PBR properties
            mat.SetFloat("_Metallic", 0.7f);
            mat.SetFloat("_Smoothness", 0.5f);
        }
    }
}
```

## ROS 2 Integration

Unity connects to ROS 2 through the ROS-TCP-Connector:

### Publisher Example

```csharp
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROS.MessageGeneration;
using UnityEngine;

public class UnityPublisher : MonoBehaviour
{
    private RosConnection ros;

    void Start()
    {
        ros = GetComponent<RosConnection>();
        ros.RegisterPublisher<geometry_msgs.msg.Twist>("/cmd_vel");
    }

    public void SendVelocityCommand(float linear, float angular)
    {
        var twistMsg = new geometry_msgs.msg.Twist();
        twistMsg.linear = new geometry_msgs.msg.Vector3 { x = linear };
        twistMsg.angular = new geometry_msgs.msg.Vector3 { z = angular };

        ros.Publish("/cmd_vel", twistMsg);
    }
}
```

### Subscriber Example

```csharp
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROS.MessageGeneration;
using UnityEngine;

public class UnitySubscriber : MonoBehaviour
{
    private RosConnection ros;

    void Start()
    {
        ros = GetComponent<RosConnection>();
        ros.Subscribe<sensor_msgs.msg.JointState>("/joint_states", OnJointState);
    }

    void OnJointState(sensor_msgs.msg.JointState jointState)
    {
        // Process joint state data
        for (int i = 0; i < jointState.name.Count; i++)
        {
            Debug.Log($"Joint {jointState.name[i]}: {jointState.position[i]}");
        }
    }
}
```

## Practical Exercise

Create a Unity scene with a wheeled robot that includes:

1. Realistic environment with lighting and materials
2. LiDAR sensor simulation
3. RGB camera sensor simulation
4. ROS 2 integration for control and sensing

## Summary

In this section, we covered:

- Setting up Unity for robotics simulation
- Physics simulation with PhysX
- Sensor simulation in Unity
- High-fidelity rendering capabilities
- Integration with ROS 2 for robot control

Unity provides a powerful platform for high-fidelity robotics simulation with photorealistic rendering and accurate physics.