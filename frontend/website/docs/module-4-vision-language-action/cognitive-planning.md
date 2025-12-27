---
sidebar_position: 3
title: Cognitive Planning with LLMs
---

# Cognitive Planning with LLMs

In this section, we'll explore how Large Language Models (LLMs) can be used for cognitive planning in robotics. We'll learn how to leverage LLMs for high-level task planning, reasoning, and decision-making in robotic systems.

## Learning Objectives

By the end of this section, you will be able to:

- Integrate LLMs with robotic systems for cognitive planning
- Design prompts for effective robot task planning
- Implement multi-step planning with LLMs
- Handle reasoning and decision-making using LLMs
- Create vision-language-action integration with LLMs

## Introduction to LLM-based Cognitive Planning

Large Language Models (LLMs) offer unprecedented capabilities for cognitive planning in robotics. Unlike traditional rule-based planners, LLMs can:

- Understand natural language instructions
- Perform complex reasoning and planning
- Handle ambiguous or incomplete information
- Generalize to novel situations
- Incorporate world knowledge

### Cognitive Planning Architecture

The LLM-based cognitive planning system typically includes:

1. **Perception Interface**: Converting sensor data to natural language
2. **LLM Planner**: High-level task planning and reasoning
3. **Action Generator**: Converting plans to robot commands
4. **Execution Monitor**: Tracking plan execution and adapting

## Setting up LLM Integration

### OpenAI GPT Integration

```python
import openai
import json
from typing import Dict, List, Any
import asyncio

class LLMPlanner:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.conversation_history = []

    def set_robot_capabilities(self, capabilities: Dict[str, Any]):
        """
        Define robot capabilities for the LLM to understand
        """
        self.capabilities = capabilities

    async def generate_plan(self, task_description: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a plan for a given task using LLM
        """
        # Create a detailed prompt
        prompt = self._create_planning_prompt(task_description, current_state)

        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        plan_text = response.choices[0].message.content
        return self._parse_plan(plan_text)

    def _create_planning_prompt(self, task_description: str, current_state: Dict[str, Any]) -> str:
        """
        Create a detailed prompt for the LLM
        """
        prompt = f"""
        Task: {task_description}

        Current Robot State:
        {json.dumps(current_state, indent=2)}

        Robot Capabilities:
        {json.dumps(self.capabilities, indent=2)}

        Please generate a detailed plan to complete this task. The plan should be structured as follows:
        1. Analyze the current situation
        2. Break down the task into subtasks
        3. Consider potential obstacles or challenges
        4. Generate a sequence of actions to complete the task
        5. Include safety considerations

        Format the response as a structured JSON object with these fields:
        {{
            "analysis": "Analysis of the situation",
            "subtasks": ["list", "of", "subtasks"],
            "plan": [
                {{
                    "action": "action_name",
                    "parameters": {{"param1": "value1"}},
                    "reasoning": "Why this action is needed"
                }}
            ],
            "safety_considerations": ["list", "of", "safety", "considerations"],
            "confidence": 0.0-1.0
        }}
        """
        return prompt

    def _get_system_prompt(self) -> str:
        """
        System prompt to guide the LLM's behavior
        """
        return """
        You are an expert robot cognitive planner. Your role is to generate detailed, safe, and executable plans for robots.
        Consider the robot's capabilities, current state, and environment when creating plans.
        Always prioritize safety and feasibility.
        Break complex tasks into simple, executable steps.
        If you're uncertain about any aspect, indicate this in your plan.
        """

    def _parse_plan(self, plan_text: str) -> Dict[str, Any]:
        """
        Parse the LLM's response into a structured plan
        """
        try:
            # Try to extract JSON from the response
            start = plan_text.find('{')
            end = plan_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = plan_text[start:end]
                plan = json.loads(json_str)
                return plan
        except json.JSONDecodeError:
            pass

        # If JSON parsing fails, return the raw text with an error flag
        return {
            "raw_response": plan_text,
            "error": "Could not parse plan as JSON"
        }
```

### Hugging Face Transformers Integration

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

class LocalLLMPlanner:
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_plan_local(self, task_description: str, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a plan using a local LLM
        """
        prompt = self._create_local_planning_prompt(task_description, current_state)

        inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024)

        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=inputs.shape[1] + 200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract the generated plan part
        plan_start = response.find("Plan:") if "Plan:" in response else len(prompt)
        plan_text = response[plan_start:]

        return self._parse_plan(plan_text)

    def _create_local_planning_prompt(self, task_description: str, current_state: Dict[str, Any]) -> str:
        """
        Create a prompt suitable for local models
        """
        return f"""
        Task: {task_description}

        Current State: {json.dumps(current_state)}

        Generate a detailed plan to complete this task:

        Plan:
        """
```

## Task Decomposition and Planning

### Multi-step Task Planning

```python
class MultiStepPlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.execution_history = []

    async def decompose_task(self, high_level_task: str, environment_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Decompose a high-level task into executable subtasks
        """
        # First, get the overall plan
        overall_plan = await self.llm_planner.generate_plan(high_level_task, environment_state)

        if "error" in overall_plan:
            return [{"action": "error", "message": overall_plan["error"]}]

        # Extract subtasks
        subtasks = overall_plan.get("subtasks", [])
        detailed_plan = overall_plan.get("plan", [])

        # If subtasks exist but no detailed plan, create detailed plan for each subtask
        if subtasks and not detailed_plan:
            detailed_plan = []
            for subtask in subtasks:
                subtask_plan = await self.llm_planner.generate_plan(subtask, environment_state)
                if "plan" in subtask_plan:
                    detailed_plan.extend(subtask_plan["plan"])

        return detailed_plan

    def validate_plan(self, plan: List[Dict[str, Any]], robot_capabilities: Dict[str, Any]) -> bool:
        """
        Validate that the plan is executable given robot capabilities
        """
        for step in plan:
            action = step.get("action")
            if action not in robot_capabilities.get("actions", []):
                print(f"Invalid action: {action}")
                return False

            required_params = robot_capabilities.get("action_params", {}).get(action, [])
            params = step.get("parameters", {})

            # Check if all required parameters are present
            for param in required_params:
                if param not in params:
                    print(f"Missing required parameter {param} for action {action}")
                    return False

        return True
```

### Context-Aware Planning

```python
class ContextAwarePlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.context_history = []

    async def plan_with_context(self, task: str, current_state: Dict[str, Any],
                              environment_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a plan considering context and history
        """
        # Create a rich context with history
        context = {
            "current_state": current_state,
            "environment_context": environment_context,
            "recent_actions": self.context_history[-5:],  # Last 5 actions
            "successful_patterns": self._get_successful_patterns()
        }

        # Enhance the task description with context
        contextual_task = self._enhance_task_with_context(task, context)

        # Generate plan
        plan = await self.llm_planner.generate_plan(contextual_task, current_state)

        # Update context history
        self.context_history.append({
            "task": task,
            "plan": plan,
            "timestamp": self._get_current_time()
        })

        return plan

    def _enhance_task_with_context(self, task: str, context: Dict[str, Any]) -> str:
        """
        Enhance task description with contextual information
        """
        enhanced_task = f"""
        Task: {task}

        Context:
        - Current time: {context.get('current_state', {}).get('timestamp', 'unknown')}
        - Environment: {context.get('environment_context', {})}
        - Recent actions: {[action['task'] for action in context.get('recent_actions', [])]}
        - Known successful patterns: {context.get('successful_patterns', [])}

        Consider the context when planning.
        """
        return enhanced_task

    def _get_successful_patterns(self) -> List[str]:
        """
        Extract successful patterns from execution history
        """
        # This would analyze past successful executions
        # For now, return some example patterns
        return [
            "navigation followed by manipulation",
            "perception before action",
            "verification after critical actions"
        ]

    def _get_current_time(self) -> str:
        """
        Get current timestamp
        """
        import datetime
        return datetime.datetime.now().isoformat()
```

## Vision-Language Integration

### Scene Understanding

```python
import base64
from io import BytesIO
from PIL import Image

class VisionLanguagePlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner

    async def plan_from_vision(self, task: str, image_data: bytes,
                             current_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a plan based on visual input and task
        """
        # Encode image for API
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # Create a detailed prompt with image
        prompt = f"""
        Task: {task}

        Current State: {json.dumps(current_state)}

        Visual Scene: [Image provided]

        Analyze the visual scene and generate a plan to complete the task.
        Consider the objects, their positions, and relationships in the scene.
        """

        # For GPT-4 Vision API, this would be different
        # This is a simplified example
        vision_enhanced_plan = await self.llm_planner.generate_plan(prompt, current_state)

        return vision_enhanced_plan

    def describe_scene(self, image_data: bytes) -> str:
        """
        Generate a text description of the scene
        """
        # This would use a vision model to describe the scene
        # For now, return a placeholder
        return "The scene contains various objects in a room. The robot needs to navigate to complete its task."
```

## Safety and Verification

### Plan Safety Checking

```python
class SafePlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.safety_rules = [
            "Avoid collisions with obstacles",
            "Respect human safety zones",
            "Maintain stability during movement",
            "Verify grasp success before lifting",
            "Check for adequate lighting before navigation"
        ]

    async def verify_plan_safety(self, plan: List[Dict[str, Any]],
                               environment_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify that a plan is safe to execute
        """
        safety_check_prompt = f"""
        Plan to verify: {json.dumps(plan, indent=2)}

        Environment state: {json.dumps(environment_state, indent=2)}

        Safety rules: {self.safety_rules}

        Please analyze the plan for safety concerns and suggest modifications if needed.

        Return a response in this JSON format:
        {{
            "is_safe": true/false,
            "safety_concerns": ["list", "of", "concerns"],
            "suggested_modifications": ["list", "of", "modifications"],
            "risk_assessment": "low/medium/high"
        }}
        """

        safety_analysis = await self.llm_planner.generate_plan(
            safety_check_prompt,
            environment_state
        )

        return safety_analysis

    def apply_safety_modifications(self, plan: List[Dict[str, Any]],
                                 modifications: List[str]) -> List[Dict[str, Any]]:
        """
        Apply safety modifications to a plan
        """
        # Apply modifications based on safety analysis
        modified_plan = plan.copy()

        for modification in modifications:
            if "add perception step" in modification.lower():
                # Insert perception steps before critical actions
                modified_plan = self._insert_perception_steps(modified_plan)
            elif "reduce speed" in modification.lower():
                # Reduce speeds for safer execution
                modified_plan = self._reduce_speeds(modified_plan)

        return modified_plan

    def _insert_perception_steps(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Insert perception steps before critical actions
        """
        new_plan = []
        for i, step in enumerate(plan):
            new_plan.append(step)

            # Add perception step before navigation or manipulation
            if step.get("action") in ["navigate", "move", "grasp", "pick_up"]:
                perception_step = {
                    "action": "perceive_environment",
                    "parameters": {"target": step.get("parameters", {}).get("target")},
                    "reasoning": "Verify environment before executing action"
                }
                new_plan.insert(i + 1, perception_step)

        return new_plan

    def _reduce_speeds(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Reduce speeds in navigation actions for safety
        """
        for step in plan:
            if step.get("action") in ["move", "navigate"]:
                params = step.get("parameters", {})
                if "speed" in params:
                    params["speed"] = params["speed"] * 0.7  # Reduce speed by 30%

        return plan
```

## Real-time Adaptation

### Plan Monitoring and Adaptation

```python
import asyncio
from dataclasses import dataclass
from enum import Enum

class ExecutionStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    INTERRUPTED = "interrupted"

@dataclass
class ExecutionResult:
    status: ExecutionStatus
    details: str
    new_state: Dict[str, Any]

class AdaptivePlanner:
    def __init__(self, llm_planner: LLMPlanner):
        self.llm_planner = llm_planner
        self.current_plan = []
        self.plan_index = 0

    async def execute_plan_with_adaptation(self, plan: List[Dict[str, Any]],
                                        initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a plan with real-time adaptation
        """
        current_state = initial_state.copy()
        execution_log = []

        for i, step in enumerate(plan):
            print(f"Executing step {i+1}/{len(plan)}: {step.get('action')}")

            # Execute the step
            result = await self._execute_single_step(step, current_state)
            execution_log.append({
                "step": step,
                "result": result,
                "timestamp": self._get_current_time()
            })

            # Update current state
            current_state.update(result.new_state)

            # Check if execution was successful
            if result.status == ExecutionStatus.FAILURE:
                # Handle failure - replan or skip
                adapted_plan = await self._handle_execution_failure(
                    plan, i, result, current_state
                )
                if adapted_plan:
                    # Continue with adapted plan
                    remaining_plan = adapted_plan[i:]
                    final_result = await self.execute_plan_with_adaptation(
                        remaining_plan, current_state
                    )
                    execution_log.extend(final_result.get("log", []))
                    break
            elif result.status == ExecutionStatus.INTERRUPTED:
                # Handle interruption - maybe emergency stop
                break

        return {
            "final_state": current_state,
            "execution_log": execution_log,
            "success": all(log["result"].status != ExecutionStatus.FAILURE
                          for log in execution_log)
        }

    async def _execute_single_step(self, step: Dict[str, Any],
                                 current_state: Dict[str, Any]) -> ExecutionResult:
        """
        Execute a single step of the plan
        """
        action = step.get("action")
        parameters = step.get("parameters", {})

        # This would interface with the actual robot
        # For simulation, return a result
        if action == "navigate":
            # Simulate navigation
            success = self._simulate_navigation(parameters, current_state)
            if success:
                return ExecutionResult(
                    status=ExecutionStatus.SUCCESS,
                    details="Navigation completed successfully",
                    new_state={"position": parameters.get("target_position", current_state.get("position"))}
                )
            else:
                return ExecutionResult(
                    status=ExecutionStatus.FAILURE,
                    details="Navigation failed - obstacle detected",
                    new_state=current_state
                )
        else:
            # For other actions, simulate success
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                details=f"{action} completed successfully",
                new_state=current_state
            )

    async def _handle_execution_failure(self, original_plan: List[Dict[str, Any]],
                                     failed_step_index: int,
                                     failure_result: ExecutionResult,
                                     current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle execution failure by replanning
        """
        remaining_tasks = original_plan[failed_step_index+1:]

        if not remaining_tasks:
            return []  # No more tasks to plan

        # Create a replanning prompt
        replan_prompt = f"""
        Original plan: {json.dumps(original_plan)}

        Failed at step: {original_plan[failed_step_index]}
        Failure reason: {failure_result.details}
        Current state: {json.dumps(current_state)}
        Remaining tasks: {json.dumps(remaining_tasks)}

        Please generate a new plan that accounts for the failure and completes the remaining tasks.
        """

        try:
            new_plan = await self.llm_planner.generate_plan(replan_prompt, current_state)
            if "plan" in new_plan:
                return new_plan["plan"]
        except Exception as e:
            print(f"Replanning failed: {e}")

        return []  # Return empty plan if replanning fails

    def _simulate_navigation(self, parameters: Dict[str, Any], current_state: Dict[str, Any]) -> bool:
        """
        Simulate navigation success/failure
        """
        import random
        # 90% success rate for simulation
        return random.random() > 0.1

    def _get_current_time(self) -> str:
        """
        Get current timestamp
        """
        import datetime
        return datetime.datetime.now().isoformat()
```

## Integration Example

### Complete Cognitive Planning System

```python
class CognitivePlanningSystem:
    def __init__(self, api_key: str):
        # Initialize components
        self.llm_planner = LLMPlanner(api_key)
        self.multi_step_planner = MultiStepPlanner(self.llm_planner)
        self.context_aware_planner = ContextAwarePlanner(self.llm_planner)
        self.vision_language_planner = VisionLanguagePlanner(self.llm_planner)
        self.safe_planner = SafePlanner(self.llm_planner)
        self.adaptive_planner = AdaptivePlanner(self.llm_planner)

        # Define robot capabilities
        self.robot_capabilities = {
            "actions": ["move", "navigate", "grasp", "perceive", "speak"],
            "action_params": {
                "move": ["direction", "distance"],
                "navigate": ["target_position", "speed"],
                "grasp": ["object", "position"],
                "perceive": ["target", "modality"],
                "speak": ["text"]
            }
        }
        self.llm_planner.set_robot_capabilities(self.robot_capabilities)

    async def execute_task(self, task_description: str, environment_state: Dict[str, Any]):
        """
        Execute a complete task using cognitive planning
        """
        print(f"Starting cognitive planning for: {task_description}")

        # 1. Decompose the task
        print("Decomposing task...")
        plan = await self.multi_step_planner.decompose_task(task_description, environment_state)

        # 2. Validate the plan
        print("Validating plan...")
        is_valid = self.multi_step_planner.validate_plan(plan, self.robot_capabilities)
        if not is_valid:
            raise ValueError("Plan validation failed")

        # 3. Check safety
        print("Checking safety...")
        safety_analysis = await self.safe_planner.verify_plan_safety(plan, environment_state)

        if not safety_analysis.get("is_safe", True):
            print(f"Plan has safety concerns: {safety_analysis.get('safety_concerns')}")
            # Apply modifications
            modifications = safety_analysis.get("suggested_modifications", [])
            plan = self.safe_planner.apply_safety_modifications(plan, modifications)

        # 4. Execute with adaptation
        print("Executing plan with adaptation...")
        execution_result = await self.adaptive_planner.execute_plan_with_adaptation(
            plan, environment_state
        )

        return execution_result

# Example usage
async def main():
    # Initialize the system (you would need a real API key)
    # system = CognitivePlanningSystem("your-api-key")

    # Define a sample task
    task = "Navigate to the kitchen and pick up the red cup from the table"

    # Define initial state
    initial_state = {
        "position": {"x": 0, "y": 0, "z": 0},
        "orientation": 0,
        "battery_level": 0.8,
        "gripper_status": "open"
    }

    # Execute the task (this would require a real API key)
    # result = await system.execute_task(task, initial_state)
    # print(f"Task execution result: {result}")

if __name__ == "__main__":
    # asyncio.run(main())
    pass
```

## Practical Exercise

Implement a cognitive planning system that:

1. Takes a natural language task description
2. Uses an LLM to generate a detailed execution plan
3. Validates the plan for safety and feasibility
4. Executes the plan with real-time adaptation
5. Handles failures by replanning

## Summary

In this section, we covered:

- LLM integration for cognitive planning
- Multi-step task decomposition
- Context-aware planning with history
- Vision-language integration for scene understanding
- Safety verification and plan adaptation
- Real-time execution with failure handling

LLM-based cognitive planning enables robots to handle complex, natural language tasks by leveraging the reasoning and planning capabilities of large language models.