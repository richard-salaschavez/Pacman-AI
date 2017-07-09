# Pacman-AI
Implementation of different AI's to play pacman

To run ai: 

simply navigate to home directory and type in the following example command:

python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic

The available agents can be called with the flag -p and they are:
– MinimaxAgent
– AlphaBetaAgent
– ExpectimaxAgent

-a Allows you to specify agent specific arguments. For instance, for any agent that is a subclass of
MultiAgentSearchAgent, you can specify the depth that you limit your search tree by typing -a
depth=3

-l Allows you to select a map for playing Pacman, e.g., -l smallClassic. There are 9 playable
maps, listed.

– minimaxClassic
– trappedClassic
– testClassic
– smallClassic
– capsuleClassic
– openClassic
– contestClassic
– mediumClassic
– originalClassic




