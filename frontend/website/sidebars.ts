import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar structure for the Physical AI & Humanoid Robotics course
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-robotic-nervous-system/index',
        'module-1-robotic-nervous-system/ros2-nodes-topics',
        'module-1-robotic-nervous-system/rclpy-bridge',
        'module-1-robotic-nervous-system/urdf-humanoids',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-digital-twin/index',
        'module-2-digital-twin/gazebo-simulation',
        'module-2-digital-twin/unity-integration',
        'module-2-digital-twin/sensors-data',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module-3-ai-robot-brain/index',
        'module-3-ai-robot-brain/isaac-sim',
        'module-3-ai-robot-brain/vslam-navigation',
        'module-3-ai-robot-brain/nav2-bipedal',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-4-vision-language-action/index',
        'module-4-vision-language-action/voice-to-action',
        'module-4-vision-language-action/cognitive-planning',
        'module-4-vision-language-action/capstone-project',
      ],
    },
  ],
};

export default sidebars;
