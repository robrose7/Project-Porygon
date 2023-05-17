import random
import pygame
from modules.brain import Brain;
import modules.smeargle as sm
import modules.player_interface_manager as pim
import modules.turn_manager as tm
import pickle
import numpy as np
import initializer

# # # - Globals
import globals

# # # - Flags
from flags import ai_flag

# Initialize Pygame
pygame.init()

brain = Brain()

# Set up the clock
clock = pygame.time.Clock()

def reset():

    global player_pokemon, enemy_pokemon, initial_draw
    player_pokemon, enemy_pokemon, globals.master_pokemon_list, globals.master_move_list = initializer.initialize_pokemon()
    globals.player_has_lost = False
    globals.player_has_won = False
    globals.enemy_battle_message = ""
    globals.player_battle_message = ""
    initial_draw = False
    globals.total_episode_reward = 0
    globals.current_move_reward = 0    

def draw_battle():
    # Grabs all data and sends it to smeargle
    sm.draw_battle(window=globals.window,
        win=globals.win,
        loss=globals.loss,
        total_episode_reward=globals.total_episode_reward,
        current_move_reward=globals.current_move_reward,
        ai_flag=ai_flag,
        enemy_pokemon=enemy_pokemon,
        player_pokemon=player_pokemon,
        player_battle_message=globals.player_battle_message,
        enemy_battle_message=globals.enemy_battle_message,
        player_supereffective=globals.player_supereffective,
        enemy_supereffective=globals.enemy_supereffective,
        selected_move_index=globals.selected_move_index,
        win_record=globals.win_record,
        loss_record=globals.loss_record,
        master_pokemon_list=globals.master_pokemon_list,
        move_frequency=globals.move_frequency
    )

player_pokemon, enemy_pokemon, globals.master_pokemon_list, globals.master_move_list = initializer.initialize_pokemon()
initial_draw = True
running = True

while running:

    for e in range(globals.num_of_episodes):

        if initial_draw:
            draw_battle()
            initial_draw = False

        if ai_flag:

            reward, globals.player_has_won, globals.player_has_lost, globals.player_battle_message, globals.enemy_battle_message, globals.player_supereffective, globals.enemy_supereffective, player_damage_dealt, enemy_damage_dealt = brain.run_episode(player_pokemon, enemy_pokemon, globals.epsilon)
            globals.total_episode_reward += reward
            draw_battle()


        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    with open('q_table.pkl', 'wb') as f:
                        pickle.dump(brain.q_table, f)

            # Options for player turn
            if globals.player_turn == True and not ai_flag:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pim.navigate_menu("left")
                    elif event.key == pygame.K_UP:
                        pim.navigate_menu("up")
                    elif event.key == pygame.K_RIGHT:
                        pim.navigate_menu("right")
                    elif event.key == pygame.K_DOWN:
                        pim.navigate_menu("down")
                    elif event.key == pygame.K_RETURN:
                        tm.submit_turn(player_pokemon.moves[globals.selected_move_index], player_pokemon, enemy_pokemon)

                    draw_battle()

        if globals.player_has_won:
            if not ai_flag:
                sm.draw_win(globals.window)
            
            globals.win_record[enemy_pokemon.id] += 1
            pygame.display.update()
            pygame.time.wait(1)
            globals.win += 1
            globals.epsilon *= globals.epsilon_decay_rate
            reset()

        if globals.player_has_lost:
            if not ai_flag:
                sm.draw_lose(globals.window)

            globals.loss_record[enemy_pokemon.id] += 1
            pygame.display.update()
            pygame.time.wait(1)
            globals.loss += 1
            globals.epsilon *= globals.epsilon_decay_rate
            reset()

        # Update the display
        pygame.display.update()

        # Set the frame rate
        clock.tick(60)

# Quit Pygame
pygame.quit()


### Week 2 TODO:
# Add Pokemon Import and Moveset from CSV (Code Moves to ID) - DONE
# Add Stat Tracker for each pokemon (Temporary) - DONE
# Add Secondary Typing
# Add Pokemon Teams
# Add Switch Functionality
# Rework Enemy AI Using Conditionals and Decision Making Tree
# Maybe TODO: Flag to be easy - medium - hard

### Functionality Todo
# Add correct stat values based off base stats -- Done
# Add correct base move damage calculation -- Done
# Add Physical/Special -- Done 
# Add Typing -- DONE
# Add Type multiplier logic -- DONE
# Add Level -- DONE
# Add typing to q_table shape -- DONE

### Visual Todo
# Maybe: Add status conditions
# Maybe: Add HP bar instead of text -- DONE
# Maybe: Add Images

### Extra Todo
# Refactor Into Individual Classes -- Done
# Add secondary typings
# Add Speed and Speed calc for turn order

