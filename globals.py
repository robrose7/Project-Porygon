import pygame
import constants
import numpy as np
import flags
import pickle

pygame.init()

window = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
player_turn = True
player_battle_message = ""
enemy_battle_message = ""
player_supereffective = False
enemy_supereffective = False
player_has_won = False
player_has_lost = False
selected_move_index = 0
master_move_list = []
master_pokemon_list = []
win_record = np.zeros(12)
loss_record = np.zeros(12)
move_frequency = np.zeros(4)

win = 0
loss = 0

### Model Variables

num_of_episodes = 100
total_episode_reward = 0
current_move_reward = 0

if flags.pretrained_flag:
    epsilon = 0
else:
    epsilon = 1.0

epsilon_decay_rate = 0.99
learning_rate = 0.01
discount_rate = 0.99

