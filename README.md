# AI Plays Snake Game Using Reinforcement Learning (Deep Q-Learning)

Welcome to the **AI Plays Snake Game** project! This repository demonstrates how an AI agent learns to play the classic Snake game using Reinforcement Learning, specifically the Deep Q-Learning (DQN) algorithm.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Algorithm Explanation](#algorithm-explanation)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
This project utilizes Deep Q-Learning, a type of reinforcement learning, to train an AI agent to play the Snake game. The agent interacts with the game environment, learns from its actions, and improves over time by optimizing its policy to maximize the reward.

The Snake game environment includes:
- A grid where the snake moves.
- A food item that the snake needs to consume to grow.
- Walls and the snake's own body, which must be avoided.

The AI agent learns by trial and error and uses its experiences to improve its decision-making.

## Features
- **Custom Snake Game Environment**: Built using Python with the Pygame library.
- **Deep Q-Learning Implementation**: Efficient training with experience replay and neural networks.
- **Visualization**: Real-time display of the game and AI performance.
- **Checkpoints**: Save and load trained models.

## Algorithm Explanation
### Deep Q-Learning (DQN)
Deep Q-Learning combines Q-learning with deep neural networks to approximate the Q-value function for large state-action spaces.

#### Key Components:
1. **Environment**:
   - The Snake game environment provides states, rewards, and transitions based on the agent's actions.

2. **State Representation**:
   - The state includes information about the snake's position, food location, and potential obstacles.

3. **Action Space**:
   - The agent can choose from four actions: move up, down, left, or right.

4. **Reward Function**:
   - Positive reward for eating food.
   - Negative reward for collisions (game over).
   - Small negative reward for each step to encourage shorter solutions.

5. **Deep Q-Network (DQN)**:
   - A neural network approximates the Q-value for each state-action pair.
   - Input: Current state.
   - Output: Q-values for all possible actions.

6. **Experience Replay**:
   - Stores past experiences (state, action, reward, next state) in a replay buffer.
   - Samples mini-batches from the buffer for training to break temporal correlations.

7. **Target Network**:
   - A separate network updated periodically to stabilize training.

#### Training Steps:
1. Initialize the replay buffer and neural network.
2. For each episode:
   - Reset the game environment.
   - Observe the initial state.
   - For each step in the episode:
     - Choose an action using an epsilon-greedy policy.
     - Perform the action and observe the reward and next state.
     - Store the experience in the replay buffer.
     - Sample a mini-batch from the buffer and update the Q-network using the Bellman equation:
       \[
       Q(s, a) \leftarrow Q(s, a) + \alpha \big[r + \gamma \max_a' Q'(s', a') - Q(s, a)\big]
       \]
3. Update the target network periodically.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-snake-game.git
   cd ai-snake-game
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Train the AI agent:
   ```bash
   python train.py
   ```
2. Play the game with the trained AI:
   ```bash
   python play.py
   ```
3. Visualize training performance:
   ```bash
   python visualize_training.py
   ```

## Results
The AI agent starts by making random moves but gradually learns to optimize its actions, achieving higher scores over time. Training results are logged and can be visualized to observe the improvement in performance.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to enhance the project.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
