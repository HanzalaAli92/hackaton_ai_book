---
sidebar_position: 2
title: Voice-to-Action
---

# Voice-to-Action

In this section, we'll explore voice-to-action systems that enable robots to understand and respond to spoken commands. We'll learn how to process voice commands using speech recognition systems and translate them into robot actions.

## Learning Objectives

By the end of this section, you will be able to:

- Implement speech recognition systems for robot control
- Process natural language commands for robotic tasks
- Create voice command grammars for robot interaction
- Integrate speech recognition with robot action planning
- Handle speech recognition errors and uncertainties

## Introduction to Voice-to-Action Systems

Voice-to-action systems enable natural human-robot interaction by allowing users to control robots using spoken commands. These systems typically involve:

1. **Speech Recognition**: Converting speech to text
2. **Natural Language Processing**: Understanding the meaning of commands
3. **Action Mapping**: Translating commands to robot actions
4. **Execution**: Performing the requested actions

## Speech Recognition Systems

### OpenAI Whisper

OpenAI Whisper is a state-of-the-art speech recognition model that can be used for voice-to-action systems.

#### Installing Whisper

```bash
pip install openai-whisper
```

#### Basic Whisper Usage

```python
import whisper
import torch

def transcribe_speech(audio_file_path):
    """
    Transcribe speech using OpenAI Whisper
    """
    # Load the model
    model = whisper.load_model("base")  # Options: tiny, base, small, medium, large

    # Transcribe the audio
    result = model.transcribe(audio_file_path)

    return result["text"]

# Example usage
transcribed_text = transcribe_speech("command.wav")
print(f"Transcribed: {transcribed_text}")
```

### Real-time Speech Recognition

For real-time applications, we need to continuously process audio input:

```python
import pyaudio
import wave
import whisper
import threading
import queue
import numpy as np

class RealTimeSpeechRecognizer:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)
        self.audio_queue = queue.Queue()
        self.recording = False

        # Audio parameters
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.record_seconds = 3  # Record 3-second chunks

    def start_recording(self):
        """
        Start recording audio in a separate thread
        """
        self.recording = True
        recording_thread = threading.Thread(target=self.record_audio)
        recording_thread.start()

    def record_audio(self):
        """
        Continuously record audio and place chunks in queue
        """
        p = pyaudio.PyAudio()

        stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        while self.recording:
            frames = []
            for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
                data = stream.read(self.chunk)
                frames.append(data)

            # Convert to numpy array and put in queue
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
            self.audio_queue.put(audio_data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def process_audio(self):
        """
        Process audio chunks from the queue
        """
        while self.recording or not self.audio_queue.empty():
            try:
                audio_data = self.audio_queue.get(timeout=1)

                # Convert to float32 and normalize
                audio_float = audio_data.astype(np.float32) / 32768.0

                # Transcribe the audio
                result = self.model.transcribe(audio_float)

                if result["text"].strip():  # Only process non-empty transcriptions
                    self.handle_command(result["text"])

            except queue.Empty:
                continue

    def handle_command(self, command_text):
        """
        Handle the transcribed command
        """
        print(f"Recognized command: {command_text}")
        # Process the command (see next section)
        self.parse_and_execute_command(command_text)

    def stop_recording(self):
        """
        Stop recording and processing
        """
        self.recording = False
```

## Natural Language Processing for Commands

### Command Parsing

We need to parse natural language commands to extract robot actions:

```python
import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class RobotCommand:
    action: str
    parameters: dict
    confidence: float

class CommandParser:
    def __init__(self):
        # Define command patterns
        self.command_patterns = {
            'move': [
                r'move\s+(?P<direction>forward|backward|left|right|up|down)\s*(?P<distance>\d+\.?\d*)?\s*(?P<unit>m|cm|in)?',
                r'go\s+(?P<direction>forward|backward|left|right|up|down)\s*(?P<distance>\d+\.?\d*)?\s*(?P<unit>m|cm|in)?',
                r'walk\s+(?P<direction>forward|backward|left|right|up|down)\s*(?P<distance>\d+\.?\d*)?\s*(?P<unit>m|cm|in)?'
            ],
            'turn': [
                r'turn\s+(?P<direction>left|right|around)\s*(?P<angle>\d+\.?\d*)?\s*degrees?',
                r'rotate\s+(?P<direction>left|right|clockwise|counterclockwise)\s*(?P<angle>\d+\.?\d*)?\s*degrees?',
                r'pivot\s+(?P<direction>left|right)\s*(?P<angle>\d+\.?\d*)?\s*degrees?'
            ],
            'grasp': [
                r'pick\s+up\s+(?P<object>.+)',
                r'grasp\s+(?P<object>.+)',
                r'grab\s+(?P<object>.+)',
                r'hold\s+(?P<object>.+)'
            ],
            'navigate': [
                r'go\s+to\s+(?P<location>.+)',
                r'go\s+to\s+the\s+(?P<location>.+)',
                r'go\s+to\s+the\s+(?P<location>.+)\s+(?P<room>room|area|zone|location)',
                r'go\s+to\s+(?P<location>.+)\s+(?P<room>room|area|zone|location)'
            ],
            'stop': [
                r'stop',
                r'hold\s+on',
                r'wait',
                r'pause'
            ],
            'find': [
                r'find\s+(?P<object>.+)',
                r'look\s+for\s+(?P<object>.+)',
                r'locate\s+(?P<object>.+)',
                r'search\s+for\s+(?P<object>.+)'
            ]
        }

    def parse_command(self, text: str) -> Optional[RobotCommand]:
        """
        Parse a natural language command
        """
        text = text.lower().strip()

        for action, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    params = match.groupdict()

                    # Convert distance to meters if specified
                    if 'distance' in params and params['distance']:
                        distance = float(params['distance'])
                        unit = params.get('unit', 'm')

                        # Convert to meters
                        if unit == 'cm':
                            distance = distance / 100.0
                        elif unit == 'in':
                            distance = distance * 0.0254

                        params['distance'] = distance
                    elif 'distance' not in params:
                        params['distance'] = 1.0  # Default distance

                    # Convert angle if specified
                    if 'angle' in params and params['angle']:
                        params['angle'] = float(params['angle'])
                    elif 'angle' not in params:
                        params['angle'] = 90.0  # Default angle

                    return RobotCommand(
                        action=action,
                        parameters=params,
                        confidence=0.9  # Default confidence
                    )

        return None  # Command not recognized

# Example usage
parser = CommandParser()
command = parser.parse_command("move forward 2 meters")
if command:
    print(f"Action: {command.action}, Params: {command.parameters}")
```

### Intent Recognition with Machine Learning

For more sophisticated command understanding, we can use machine learning models:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

class MLCommandClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        self.is_trained = False

    def train(self, commands, labels):
        """
        Train the classifier with example commands and their labels
        """
        self.pipeline.fit(commands, labels)
        self.is_trained = True

    def predict(self, command_text):
        """
        Predict the intent of a command
        """
        if not self.is_trained:
            return None

        prediction = self.pipeline.predict([command_text])[0]
        confidence = max(self.pipeline.predict_proba([command_text])[0])

        return prediction, confidence

    def save_model(self, filepath):
        """
        Save the trained model
        """
        joblib.dump(self.pipeline, filepath)

    def load_model(self, filepath):
        """
        Load a trained model
        """
        self.pipeline = joblib.load(filepath)
        self.is_trained = True

# Example training data
training_commands = [
    "move forward", "go forward", "walk forward", "move ahead", "go ahead",
    "turn left", "rotate left", "turn to the left", "pivot left",
    "turn right", "rotate right", "turn to the right", "pivot right",
    "pick up the object", "grasp the item", "grab the thing", "hold the object",
    "go to kitchen", "go to the kitchen", "navigate to kitchen", "move to kitchen",
    "stop", "halt", "wait", "pause", "freeze"
]

training_labels = [
    "move_forward", "move_forward", "move_forward", "move_forward", "move_forward",
    "turn_left", "turn_left", "turn_left", "turn_left",
    "turn_right", "turn_right", "turn_right", "turn_right",
    "grasp", "grasp", "grasp", "grasp",
    "navigate", "navigate", "navigate", "navigate",
    "stop", "stop", "stop", "stop", "stop"
]

# Train the classifier
classifier = MLCommandClassifier()
classifier.train(training_commands, training_labels)
```

## Voice Command Grammar

Creating a formal grammar helps ensure consistent command interpretation:

```python
import pyparsing as pp

class VoiceCommandGrammar:
    def __init__(self):
        # Define basic elements
        self.direction = pp.oneOf("forward backward left right up down")
        self.turn_direction = pp.oneOf("left right around clockwise counterclockwise")
        self.location = pp.oneOf("kitchen bedroom bathroom office living_room")
        self.object = pp.Word(pp.alphas + "_")

        # Distance with optional unit
        number = pp.pyparsing_common.number
        unit = pp.oneOf("m cm inches feet")
        distance = pp.Group(number + pp.Optional(unit, default="m"))

        # Define command patterns
        self.move_command = (
            pp.Keyword("move") | pp.Keyword("go") | pp.Keyword("walk")
        ) + self.direction + pp.Optional(distance)("distance")

        self.turn_command = (
            pp.Keyword("turn") | pp.Keyword("rotate") | pp.Keyword("pivot")
        ) + self.turn_direction + pp.Optional(distance)("angle")

        self.grasp_command = (
            pp.Keyword("pick up") | pp.Keyword("grasp") |
            pp.Keyword("grab") | pp.Keyword("hold")
        ) + self.object

        self.navigate_command = (
            pp.Keyword("go to") | pp.Keyword("navigate to") |
            pp.Keyword("move to")
        ) + self.location

        self.stop_command = pp.Keyword("stop") | pp.Keyword("pause") | pp.Keyword("wait")

        # Combine all commands
        self.grammar = (
            self.move_command |
            self.turn_command |
            self.grasp_command |
            self.navigate_command |
            self.stop_command
        )

    def parse(self, command_text):
        """
        Parse a command using the grammar
        """
        try:
            result = self.grammar.parseString(command_text, parseAll=True)
            return self._convert_to_command(result)
        except pp.ParseException:
            return None

    def _convert_to_command(self, parsed_result):
        """
        Convert parsed result to command structure
        """
        # Implementation would convert parsed tokens to structured command
        pass
```

## Integration with Robot Control

### Action Execution

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from std_msgs.msg import String
import math

class VoiceActionExecutor(Node):
    def __init__(self):
        super().__init__('voice_action_executor')

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.status_pub = self.create_publisher(String, '/voice_status', 10)

        # Robot parameters
        self.linear_speed = 0.5  # m/s
        self.angular_speed = 0.5  # rad/s
        self.wheel_radius = 0.1  # meters
        self.axle_length = 0.4   # meters (for differential drive)

        # Command queue
        self.command_queue = []
        self.current_command = None

        # Timer for command execution
        self.command_timer = self.create_timer(0.1, self.execute_command)

    def execute_command(self, command: RobotCommand):
        """
        Execute a parsed robot command
        """
        if command.action == 'move':
            self.execute_move_command(command)
        elif command.action == 'turn':
            self.execute_turn_command(command)
        elif command.action == 'grasp':
            self.execute_grasp_command(command)
        elif command.action == 'navigate':
            self.execute_navigate_command(command)
        elif command.action == 'stop':
            self.execute_stop_command(command)
        elif command.action == 'find':
            self.execute_find_command(command)

    def execute_move_command(self, command: RobotCommand):
        """
        Execute a move command
        """
        direction = command.parameters.get('direction', 'forward')
        distance = command.parameters.get('distance', 1.0)

        # Create velocity command
        vel_msg = Twist()

        if direction in ['forward', 'up']:
            vel_msg.linear.x = self.linear_speed
        elif direction == 'backward':
            vel_msg.linear.x = -self.linear_speed
        elif direction == 'left':
            vel_msg.linear.y = self.linear_speed
        elif direction == 'right':
            vel_msg.linear.y = -self.linear_speed
        elif direction == 'down':
            vel_msg.linear.z = -self.linear_speed

        # Calculate duration based on distance and speed
        duration = distance / abs(vel_msg.linear.x) if vel_msg.linear.x != 0 else 0
        if vel_msg.linear.y != 0:
            duration = distance / abs(vel_msg.linear.y)
        if vel_msg.linear.z != 0:
            duration = distance / abs(vel_msg.linear.z)

        # Execute the movement
        self.execute_timed_command(vel_msg, duration)

    def execute_turn_command(self, command: RobotCommand):
        """
        Execute a turn command
        """
        direction = command.parameters.get('direction', 'left')
        angle = command.parameters.get('angle', 90.0)  # degrees

        # Convert to radians
        angle_rad = math.radians(angle)

        # Calculate angular velocity and duration
        vel_msg = Twist()

        if direction in ['left', 'counterclockwise']:
            vel_msg.angular.z = self.angular_speed
        elif direction in ['right', 'clockwise']:
            vel_msg.angular.z = -self.angular_speed
        elif direction == 'around':
            # Full rotation
            angle_rad = 2 * math.pi
            vel_msg.angular.z = self.angular_speed

        # Calculate duration for turn
        duration = angle_rad / abs(vel_msg.angular.z)

        # Execute the turn
        self.execute_timed_command(vel_msg, duration)

    def execute_timed_command(self, vel_msg, duration):
        """
        Execute a velocity command for a specific duration
        """
        start_time = self.get_clock().now()
        end_time = start_time + rclpy.time.Duration(seconds=duration)

        while self.get_clock().now() < end_time:
            self.cmd_vel_pub.publish(vel_msg)
            # In a real implementation, this would be handled by a timer

        # Stop the robot
        stop_msg = Twist()
        self.cmd_vel_pub.publish(stop_msg)

    def execute_stop_command(self, command: RobotCommand):
        """
        Execute a stop command
        """
        stop_msg = Twist()
        self.cmd_vel_pub.publish(stop_msg)

        status_msg = String()
        status_msg.data = "Robot stopped by voice command"
        self.status_pub.publish(status_msg)

    def execute_grasp_command(self, command: RobotCommand):
        """
        Execute a grasp command
        """
        object_name = command.parameters.get('object', 'object')

        # This would interface with a gripper control system
        # For now, just publish status
        status_msg = String()
        status_msg.data = f"Attempting to grasp {object_name}"
        self.status_pub.publish(status_msg)

    def execute_navigate_command(self, command: RobotCommand):
        """
        Execute a navigation command
        """
        location = command.parameters.get('location', 'unknown')

        # This would interface with a navigation system
        # For now, just publish status
        status_msg = String()
        status_msg.data = f"Navigating to {location}"
        self.status_pub.publish(status_msg)

    def execute_find_command(self, command: RobotCommand):
        """
        Execute a find command
        """
        object_name = command.parameters.get('object', 'object')

        # This would interface with a perception system
        # For now, just publish status
        status_msg = String()
        status_msg.data = f"Searching for {object_name}"
        self.status_pub.publish(status_msg)
```

## Error Handling and Robustness

### Confidence-based Execution

```python
class RobustVoiceController:
    def __init__(self, min_confidence=0.7):
        self.min_confidence = min_confidence
        self.parser = CommandParser()
        self.executor = VoiceActionExecutor()

    def process_voice_command(self, command_text):
        """
        Process a voice command with confidence checking
        """
        # Parse the command
        parsed_command = self.parser.parse_command(command_text)

        if parsed_command is None:
            self.speak_response("I didn't understand that command.")
            return False

        # Check confidence
        if parsed_command.confidence < self.min_confidence:
            self.speak_response(f"I'm not confident I understood: {command_text}. Could you repeat that?")
            return False

        # Execute the command
        try:
            self.executor.execute_command(parsed_command)
            self.speak_response(f"Executing: {parsed_command.action} command")
            return True
        except Exception as e:
            self.speak_response(f"Error executing command: {str(e)}")
            return False

    def speak_response(self, text):
        """
        Speak a response (implementation depends on TTS system used)
        """
        # This would interface with a text-to-speech system
        print(f"Robot says: {text}")
```

## Practical Exercise

Implement a voice-to-action system that:

1. Records audio from a microphone
2. Uses OpenAI Whisper for speech recognition
3. Parses natural language commands using regex patterns
4. Executes commands on a simulated robot
5. Handles errors and uncertainties gracefully

## Summary

In this section, we covered:

- Speech recognition using OpenAI Whisper
- Natural language processing for command understanding
- Creating command grammars for consistent interpretation
- Integrating voice commands with robot control
- Error handling and robustness in voice-to-action systems

Voice-to-action systems provide a natural interface for human-robot interaction, enabling intuitive control through spoken commands.