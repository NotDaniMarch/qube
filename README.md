# Qube - Quantum Energy Cube

### Core Concept
I would like to create a quantum puzzle game. The game mechanic will involve quantum
concepts: superposition, measurement and interference. The playable character
respresents a qubit and can use superpowers equivalent to H, Z, and X gates to overcome
obstacles. This is supposed to be a fun way to make you think and get initial intuition for
quantum computing.
You are in a room with obstacles, and you need to get from place A to place B. You are a
cube that has low enegry (dark color) or high energy (bright color). The obstacles come in
the form of pads that you have to stand on to move/remove walls, doors letting only one
energy level through, and killing blocks that end the game or remove a twin cube. You can
split into two energy level players, control them together, and go back into just one state
either voluntarily (choose the instance to keep) or involuntarily (random instance is
chosen) when an observation block is touched.

### Thematic Focus
The theme of the game is exploring quantum mechanics through interactive problemsolving. The theme is integrated into gameplay by representing the player as a qubit and
allowing players to apply gates to overcome obstacles.
The purpose and social good of the game is to:
• Encourage reasoning and abstract thinking.
• Give quantum mechanics intuition for beginners, which is otherwise highly abstract
and mathematical.
• Entertain and possibly inspire interest in quantum computing.

### Quantum Dimension
The main quantum concepts:
• Player splitting is superposition of low and high energy states.
• Choosing a particular cube to keep is the equvalent of applying Z gate for
interference before applying Hadamard gate again.
• The observation block chooses random instance of player to stay which describes
the observation concept and measurement.
This makes the implementation conceptual (the quantum concepts are represented in
different and interacive form), state-based (the player state is manipulated), and gatebased (the players can apply X, H, and Z gates).
How it goes beyond classical probabilistical model:
• Superposition (player splitting) allows simultaneous exploration of multiple paths.
• Interference can give deterministic outcomes through phase manipulation, not just
complete randomness.
• Correlation between player instances allows puzzle mechanics that cannot be
achieved with independent random events.

### Game Mechanics and Rules
Players can switch to high energy or low energy state, which is visually shown by brightness
of the player. This mechanic allows players to pass through doors and activate pads which
require a certain energy level.
Players can split into two cubes (low and high energy) and control them together to perform
more complex tasks such as activating two corresponding pads at the same time. The
same way two cubes can be reduced to one. The player can choose which cube to leave
and which to keep, but if the player touches an observation block, then one player instance
is randomly selected to stay.
There are killing blocks. If player touches it, the game will stop or if it’s only an instance of
player it gets removed.

### Winning and Losing Conditions
The game ends in success if the player or its instance reaches the destination B. If the
destination is not reachable anymore (e.g. result of observation) then it can be considered
as losing and the player can press reset button. If the player (not in superposition) touches
the killing block it’s also a loss.

### Platform and Tools
I plan to code the game in Python (Pygame), the full playable version. The minimum
expected content is a single level that encompasses all game features and quantum
concepts involved.
