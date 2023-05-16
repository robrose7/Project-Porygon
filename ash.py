
import random
import numpy as np


class Ash: 
    def __init__(self) -> None:
        pass
        
    def choose_move(self, epsilon, q_table, state):
        # Start the brain here
        if np.random.rand() < epsilon:
            action = np.random.randint(4)
        else:
            q_values = q_table[state.player_hp, state.enemy_hp, state.player_type, state.enemy_type, :]
            action = np.argmax(q_values)
        return action
