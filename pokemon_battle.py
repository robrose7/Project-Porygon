import csv
import copy
import random
import pygame;
from ash import Ash
from brain import Brain
from pokemon import Pokemon
from smeargle import Smeargle
from move import Move
from stats import Stats
from brainState import BrainState
import pickle
import numpy as np
import constants
import player_interface_manager as pim

# Initialize Pygame
pygame.init()

# Set up the window dimensions
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

# Handles all drawing
smeargle = Smeargle(window)

# Flags
ai_flag = True
pretrained_flag = False
multi_pokemon_flag = False
all_pokemon_flag = False
single_pokemon_index = 2

# (WIP) Flags
observable_flag = False
teams_flag = False
stat_tracker_flag = True

# model variables
trainer = Ash()
brain = Brain()
num_of_episodes = 100
model = brain.initialize_brain()
total_episode_reward = 0
current_move_reward = 0

if pretrained_flag:
    with open('q_table.pkl', 'rb') as f:
        q_table = pickle.load(f)
else:
    q_table = np.zeros((100, 100, 18, 18, 4))

# Epsilon value = rate at which we randomly explore compared to educated decision
if pretrained_flag:
    epsilon = 1.0
else:
    epsilon = 1.0

# knobs and dials
epsilon_decay_rate = 0.99
learning_rate = 0.01
discount_rate = 0.99

# in milliseconds
TURN_BUFFER = 1 if ai_flag else 100
if observable_flag:
    TURN_BUFFER = 2000

NEW_GAME_BUFFER = 1 if ai_flag else 100

# Set up the clock
clock = pygame.time.Clock()

def get_current_state():

    # Plug any state model needed here

    # 0 - 99
    player_hp_percent = ((player_pokemon.stats.hp / player_pokemon.stats.max_hp) * 100) - 1
    enemy_hp_percent = ((enemy_pokemon.stats.hp / enemy_pokemon.stats.max_hp) * 100) - 1


    state = BrainState(player_hp_percent, enemy_hp_percent, player_pokemon.type, enemy_pokemon.type)

    #print("$: " + str(player_pokemon.type))
    #print("&: " + str(state.player_type))
    return state

def initialize_pokemon():

    global master_move_list, master_pokemon_list
    master_pokemon_list = []
    master_move_list = []

    # Cleanly fix variable type issues
    with open('data/moves.csv', 'r') as move_file:
        move_reader = csv.reader(move_file)
        for move in move_reader:
            new_move = Move(move[0],move[1],constants.types[move[2]],int(move[3]),int(move[4]),move[5])
            master_move_list.append(new_move)

    with open('data/pokemon_data.csv', 'r') as pokemon_file:
        pokemon_reader = csv.reader(pokemon_file)
        for pokemon in pokemon_reader:
            moves = []
            move_ids = [pokemon[10],pokemon[11],pokemon[12],pokemon[13]]
            for id in move_ids:
                move_index = 0
                for i, move in enumerate(master_move_list):
                    if move.id == id:
                        move_index = i
                        break
                moves.append(master_move_list[move_index])
            
    
            second_type = None if pokemon[3] == 'NULL' else constants.types[pokemon[3]]
            stats = Stats(50,int(pokemon[4]),int(pokemon[5]),int(pokemon[6]),int(pokemon[7]),int(pokemon[8]))
            new_pokemon = Pokemon(int(pokemon[0]),pokemon[1],constants.types[pokemon[2]],second_type,moves,stats)
            master_pokemon_list.append(new_pokemon)

    # [master_pokemon_list[0], master_pokemon_list[1], master_pokemon_list[2], master_pokemon_list[3], master_pokemon_list[4], master_pokemon_list[5], master_pokemon_list[6], master_pokemon_list[7], master_pokemon_list[8]]
    enemy_pokemon_pool = [master_pokemon_list[9], master_pokemon_list[10], master_pokemon_list[11]]
    # enemy_pokemon_pool = [master_pokemon_list[0], master_pokemon_list[1], master_pokemon_list[2], master_pokemon_list[3], master_pokemon_list[4], master_pokemon_list[5], master_pokemon_list[6], master_pokemon_list[7], master_pokemon_list[8]]
    if multi_pokemon_flag:
        if all_pokemon_flag:
            enemy_pokemon_choice = random.randint(0, len(master_pokemon_list) - 1)
            enemy_pokemon = copy.deepcopy(master_pokemon_list[enemy_pokemon_choice])
        else:
            enemy_pokemon_choice = random.randint(0, len(enemy_pokemon_pool) - 1)
            enemy_pokemon = copy.deepcopy(enemy_pokemon_pool[enemy_pokemon_choice])
    else:
        enemy_pokemon = copy.deepcopy(master_pokemon_list[single_pokemon_index])

    player_pokemon = copy.deepcopy(master_pokemon_list[0])

    return player_pokemon, enemy_pokemon

def submit_turn(move, player_pokemon, enemy_pokemon):
    
    ## Have selected move
    ## Execute move on enemy pokemon
    ## Damage Calculation
    ## Play Animation

    ## Determine enemy selected move
    ## Execute move on player pokemon
    ## Damage Calculation
    ## Play Animation

    ## TODO: Order of this could be determined by Speed

    global player_supereffective, enemy_supereffective

    prev_player_hp = player_pokemon.stats.hp
    prev_enemy_hp = enemy_pokemon.stats.hp

    enemy_knocked_out, player_supereffective, player_damage_dealt = process_turn(move, player_pokemon, enemy_pokemon)

    global player_battle_message 
    player_battle_message = (str(player_pokemon.name) + " used " + str(move.name) + "!")

    # TODO: Could add decision making to this
    global trainer
    enemy_move_index = random.randint(0, 3)
    enemy_move = enemy_pokemon.moves[enemy_move_index]

    player_knocked_out, enemy_supereffective, enemy_damage_dealt = process_turn(enemy_move, enemy_pokemon, player_pokemon)

    global enemy_battle_message
    enemy_battle_message = (str(enemy_pokemon.name) + " used " + str(enemy_move.name))

    if enemy_knocked_out:
        global player_has_won
        player_has_won = True

    if player_knocked_out and not enemy_knocked_out:
        global player_has_lost
        player_has_lost = True
        player_has_won = False

    next_state = get_current_state()

    new_player_hp = next_state.player_hp
    new_enemy_hp = next_state.enemy_hp

    # reward equals damage dealt

    multiplier = 1
    if player_supereffective:
        multiplier *= 1.5

    function_1 = (prev_enemy_hp - new_enemy_hp)
    function_2 = (prev_enemy_hp - new_enemy_hp) * multiplier
    function_3 = player_damage_dealt * multiplier

    reward = function_2

    #logging purposes
    global current_move_reward
    current_move_reward = reward

    return next_state, reward

def process_turn(move, attacker, defender):
    ## Damage Calculation
    ## TODO: Make this more complex and accurate if needed

    damage, is_super_effective = calculate_damage(move, attacker, defender)
    defender.stats.hp -= damage

    if (defender.stats.hp < 0):
        defender.stats.hp = 0

    ## Play Animation
    knocked_out = False

    if (defender.stats.hp <= 0):
        knocked_out = True

    return knocked_out, is_super_effective, damage

def calculate_damage(move, attacker, defender):

    attack = attacker.stats.atk if move.category is constants.categories['PHYSICAL'] else attacker.stats.spatk
    defense = defender.stats.defe if move.category is constants.categories['PHYSICAL'] else defender.stats.spdef

    type_multiplier, is_super_effective = check_types(move, defender)
    
    stab_multiplier = 1
    if move.type == attacker.type or move.type == attacker.type2:
        stab_multiplier *= 1.5

    damage = int((((((2 * attacker.stats.level) / 5) + 2) * move.power * (attack / defense)) / 50) + 2) * type_multiplier * stab_multiplier
    return damage, is_super_effective

def check_types(move, defender):

    multiplier = 1

    # UI Purposes
    is_super_effective = False

    # 0 = Immune
    # 1 = Neutral
    # 2 = Super Effective
    # 3 = Not Effective

    chart = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 1, 1, 3, 1], # Normal
    [1, 3, 3, 2, 1, 2, 1, 1, 1, 1, 1, 2, 3, 1, 3, 1, 2, 1], # Fire
    [1, 2, 3, 3, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 3, 1, 1, 1], # Water
    [1, 3, 2, 3, 1, 1, 1, 3, 2, 3, 1, 3, 2, 1, 3, 1, 3, 1], # Grass
    [1, 1, 2, 3, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 3, 1, 1, 1], # Electric
    [1, 3, 3, 2, 1, 3, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 3, 1], # Ice
    [2, 1, 1, 1, 1, 2, 1, 3, 1, 3, 3, 3, 2, 0, 1, 2, 2, 3], # Fighting
    [1, 1, 1, 2, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 1, 0, 2], # Poison
    [1, 2, 1, 3, 2, 1, 1, 2, 1, 0, 1, 3, 2, 1, 1, 1, 2, 1], # Ground
    [1, 1, 1, 2, 3, 1, 2, 1, 1, 1, 1, 2, 3, 1, 1, 1, 3, 1], # Flying
    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 0, 3, 1], # Psychic
    [1, 3, 1, 2, 1, 1, 3, 3, 1, 3, 2, 1, 1, 3, 1, 2, 3, 3], # Bug
    [1, 2, 1, 1, 1, 2, 3, 1, 3, 2, 1, 2, 1, 1, 1, 1, 3, 1], # Rock
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1], # Ghost
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 0], # Dragon
    [1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 3], # Dark
    [1, 3, 3, 1, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2], # Steel
    [1, 3, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1]] # Fairy
#    N  F  W  G  E  I  F  P  G  F  Ps B  R  Go Dr D  S  F

    chart_value = chart[move.type][defender.type] 

    # silly little thing
    if chart_value == 3:
        chart_value = 0.5

    multiplier *= chart_value

    if defender.type2 != None:
        # two types
        second_chart_value = chart[move.type][defender.type2]
        if second_chart_value == 3:
            second_chart_value = 0.5
        
        multiplier *= second_chart_value

    if multiplier >= 2:
        is_super_effective = True

    return multiplier, is_super_effective     


def reset():

    global player_pokemon, enemy_pokemon, player_has_won, player_has_lost, enemy_battle_message, player_battle_message, initial_draw, total_episode_reward, current_move_reward
    player_pokemon, enemy_pokemon = initialize_pokemon()
    player_has_lost = False
    player_has_won = False
    enemy_battle_message = ""
    player_battle_message = ""
    initial_draw = False
    total_episode_reward = 0
    current_move_reward = 0
    
# Grabs all data and sends it to smeargle
def draw_battle():
    smeargle.draw_battle(win,
        loss,
        total_episode_reward,
        current_move_reward,
        ai_flag,
        enemy_pokemon,
        player_pokemon,
        player_battle_message,
        enemy_battle_message,
        player_supereffective,
        enemy_supereffective,
        selected_move_index,
        win_record,
        loss_record,
        master_pokemon_list,
        move_frequency
    )

player_pokemon, enemy_pokemon = initialize_pokemon()

initial_draw = True
running = True
while running:

    for e in range(num_of_episodes):

        if initial_draw:
            draw_battle()
            initial_draw = False

        if ai_flag:

            pygame.time.wait(TURN_BUFFER)
            state = get_current_state()
            move_choice = trainer.choose_move(epsilon=epsilon, q_table=q_table, state=state)
            move_frequency[move_choice] += 1
            active_move = player_pokemon.moves[move_choice]
            # TODO: Write to file

            next_state, reward = submit_turn(active_move, player_pokemon, enemy_pokemon)

            #print("0: " + str(player_pokemon.type))
            #print("1: ", type(state.player_hp))
            #print("2: ", type(state.enemy_hp))
            #print("3: ", type(state.player_type))
            #print("4: ", type(state.enemy_type))

            #print("5: ", type(next_state.player_hp))
            #print("6: ", type(next_state.enemy_hp))
            #print("7: ", type(next_state.player_type))
            #print("8: ", type(next_state.enemy_type))
            #print("8: " + str(next_state.enemy_type))


            q_table[state.player_hp, state.enemy_hp, state.player_type, state.enemy_type, move_choice] = q_table[state.player_hp, state.enemy_hp, state.player_type, state.enemy_type, move_choice] + \
            learning_rate * (reward + discount_rate * np.max(q_table[next_state.player_hp, next_state.enemy_hp, next_state.player_type, next_state.enemy_type, :]) 
            - q_table[state.player_hp, state.enemy_hp, state.player_type, state.enemy_type, move_choice])
            total_episode_reward += reward
            state = next_state

            draw_battle()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    with open('q_table.pkl', 'wb') as f:
                        pickle.dump(q_table, f)

            # Options for player turn
            if player_turn == True and not ai_flag:
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
                        submit_turn(player_pokemon.moves[selected_move_index], player_pokemon, enemy_pokemon)

                    draw_battle()

        if player_has_won:
            if not ai_flag:
                smeargle.draw_win()
            
            win_record[enemy_pokemon.id] += 1
            pygame.display.update()
            pygame.time.wait(NEW_GAME_BUFFER)
            win += 1
            epsilon *= epsilon_decay_rate
            reset()

        if player_has_lost:
            if not ai_flag:
                smeargle.draw_lose()

            loss_record[enemy_pokemon.id] += 1
            pygame.display.update()
            pygame.time.wait(NEW_GAME_BUFFER)
            loss += 1
            epsilon *= epsilon_decay_rate
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

