# ict002python

# 2D Obstacle-Dodging Game with Pygame

This is a 2D side-scrolling game developed as part of a university project, built using Python and the Pygame library. The player chooses a character and survive by dodging obstacles that approach from the ground and fall from the sky.

## Gameplay & Features

* **Character Selection:** Players can choose their character at the start of the game.
* **Obstacles:** Dodge two types of obstacles:
    * Ground-based obstacles that require the player to **jump**.
    * Falling obstacles from the sky that require the player to **avoid**.
* **Core Game Mechanics:**
    * Implemented player controls for jumping and ducking using keyboard inputs.
    * Developed collision detection logic between the player and various obstacles.
    * Managed game states, including a scoring system and player health.

## Controls

* `←` / `→` **Arrow Keys**: Move Character
* `Spacebar`: Jump
* `Shift Key`: Duck

## How to Run

1.  Make sure you have **Python** and **Pygame** installed on your system.
2.  Clone or download this repository to your local machine.
    ```bash
    git clone [https://github.com/liverblu/ict002python.git](https://github.com/liverblu/ict002python.git)
    ```
3.  Navigate to the project directory in your terminal.
    ```bash
    cd ict002python
    ```
4.  Run the main game file.
    ```bash
    python main.py  
    ```
    *(Note: Based on your file list, the main file might be named differently, e.g., `pygame_character_choice 해결.py`. Please update the filename accordingly.)*

## Project Purpose

This project was developed to apply fundamental programming concepts, including:
* **Object-Oriented Programming (OOP):** Designing and managing separate classes for the Player, Obstacles, and other game elements.
* **Event Handling:** Processing user inputs and in-game events within the main game loop.
* **Game Logic:** Implementing core logic for scoring, physics, and state management.
