---
id: 1
title: Create Docusaurus Educational Book
stage: constitution
date: 2025-12-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, docusaurus, education, ai, robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution Create the project constitution for a Docusaurus-based educational book titled "Physical AI & Humanoid Robotics". The book focuses on Embodied Intelligence, bridging digital AI with physical humanoid robots using simulations and real-world tools.

Key principles:
- Use Docusaurus v3+ for static site generation with Markdown/MDX content, React components for interactive elements (e.g., code snippets, diagrams).
- Structure as a multi-module course: Overview + 4 Modules (The Robotic Nervous System with ROS 2, The Digital Twin with Gazebo/Unity, The AI-Robot Brain with NVIDIA Isaac, Vision-Language-Action with LLMs).
- Include a Capstone Project in Module 4.
- Content must be educational, clear, with learning objectives, code examples, diagrams, and hands-on exercises.
- Ensure high-quality: Accurate technical details, proper citations for tools (ROS 2, Gazebo, Unity, NVIDIA Isaac Sim/ROS, Nav2, OpenAI Whisper, LLMs).
- Deploy to GitHub Pages via gh-pages branch.
- All content in English, professional tone suitable for students applying AI to robotics.
- Prioritize modularity, version control, and easy updates.
- No hallucinations: Stick to provided course outline.

## Response snapshot

I've successfully created the project constitution for the "Physical AI & Humanoid Robotics" educational book. The constitution includes 6 core principles: Educational Content Quality, Docusaurus-Based Structure, Technical Accuracy and Non-Hallucination, Modularity and Version Control, Professional Tone and Accessibility, and Deployment and Distribution. The constitution is version 1.0.0 and follows the specified requirements for the educational book project.

## Outcome

- ✅ Impact: Created initial project constitution for Docusaurus-based educational book
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new principles
- 🔁 Next prompts: Can proceed with spec, plan, and tasks creation
- 🧠 Reflection: Constitution successfully captures all specified requirements for the educational book

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A