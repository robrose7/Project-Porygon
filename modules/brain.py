import numpy as np
import pygame
import flags
import pickle

from interfaces.model_state import ModelState
import modules.turn_manager as tm

from globals import move_frequency
from globals import learning_rate
from globals import discount_rate

pygame.init()

class Brain: 
    def __init__(self) -> None:
        self.state = None
        self.next_state = None
        self.q_table = self.load_table()
    
    def choose_move(self, epsilon):
        # Q - Table Policy
        if np.random.rand() < epsilon:
            action = np.random.randint(4)
        else:
            q_values = self.q_table[self.state.player_hp, self.state.enemy_hp, self.state.player_type, self.state.enemy_type, :]
            action = np.argmax(q_values)
        return action

    def run_episode(self, player_pokemon, enemy_pokemon, epsilon):

        pygame.time.wait(1)
        self.state = self.get_current_state(player_pokemon, enemy_pokemon)
        move_choice = self.choose_move(epsilon=epsilon)
        move_frequency[move_choice] += 1
        active_move = player_pokemon.moves[move_choice]

        self.next_state, reward, player_has_won, player_has_lost, player_battle_message, enemy_battle_message, player_supereffective, enemy_supereffective, player_damage_dealt, enemy_damage_dealt = tm.submit_turn(active_move, player_pokemon, enemy_pokemon)

        # Update Q Table with State and Next State
        self.q_table[self.state.player_hp, self.state.enemy_hp, self.state.player_type, self.state.enemy_type, move_choice] = self.q_table[self.state.player_hp, self.state.enemy_hp, self.state.player_type, self.state.enemy_type, move_choice] + \
        learning_rate * (reward + discount_rate * np.max(self.q_table[self.next_state.player_hp, self.next_state.enemy_hp, self.next_state.player_type, self.next_state.enemy_type, :]) 
        - self.q_table[self.state.player_hp, self.state.enemy_hp, self.state.player_type, self.state.enemy_type, move_choice])

        # Overwrite state
        self.state = self.next_state

        return reward, player_has_won, player_has_lost, player_battle_message, enemy_battle_message, player_supereffective, enemy_supereffective, player_damage_dealt, enemy_damage_dealt

    def get_current_state(self, player_pokemon, enemy_pokemon):

        # 0 - 99
        player_hp_percent = ((player_pokemon.stats.hp / player_pokemon.stats.max_hp) * 100) - 1
        enemy_hp_percent = ((enemy_pokemon.stats.hp / enemy_pokemon.stats.max_hp) * 100) - 1

        state = ModelState(player_hp_percent, enemy_hp_percent, player_pokemon.type, enemy_pokemon.type)
        return state

    def load_table(self):
        if flags.pretrained_flag:
            with open('models/pb.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            return np.zeros((100, 100, 18, 18, 4))

