import csv
import copy
import random
import constants

from flags import multi_pokemon_flag
from flags import all_pokemon_flag

from interfaces.move import Move
from interfaces.pokemon import Pokemon
from interfaces.stats import Stats

def initialize_pokemon():

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
        enemy_pokemon = copy.deepcopy(master_pokemon_list[constants.SINGLE_POKEMON_INDEX])

    player_pokemon = copy.deepcopy(master_pokemon_list[0])

    return player_pokemon, enemy_pokemon, master_pokemon_list, master_move_list