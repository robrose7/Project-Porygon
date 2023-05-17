import constants
import random

from interfaces.model_state import ModelState


def submit_turn(move, player_pokemon, enemy_pokemon):

    prev_player_hp = player_pokemon.stats.hp
    prev_enemy_hp = enemy_pokemon.stats.hp

    enemy_knocked_out, player_supereffective, player_damage_dealt = process_turn(move, player_pokemon, enemy_pokemon)

    player_battle_message = (str(player_pokemon.name) + " used " + str(move.name) + "!")

    # TODO: Could add decision making to this
    enemy_move_index = random.randint(0, 3)
    enemy_move = enemy_pokemon.moves[enemy_move_index]

    player_knocked_out, enemy_supereffective, enemy_damage_dealt = process_turn(enemy_move, enemy_pokemon, player_pokemon)

    enemy_battle_message = (str(enemy_pokemon.name) + " used " + str(enemy_move.name))

    player_has_won = False
    player_has_lost = False

    if enemy_knocked_out:
        player_has_won = True

    if player_knocked_out and not enemy_knocked_out:
        player_has_lost = True
        player_has_won = False

    next_state = get_current_state(player_pokemon, enemy_pokemon)

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

    return next_state, reward, player_has_won, player_has_lost, player_battle_message, enemy_battle_message,  player_supereffective, enemy_supereffective, player_damage_dealt, enemy_damage_dealt

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

def get_current_state(player_pokemon, enemy_pokemon):

        # 0 - 99
        player_hp_percent = ((player_pokemon.stats.hp / player_pokemon.stats.max_hp) * 100) - 1
        enemy_hp_percent = ((enemy_pokemon.stats.hp / enemy_pokemon.stats.max_hp) * 100) - 1

        state = ModelState(player_hp_percent, enemy_hp_percent, player_pokemon.type, enemy_pokemon.type)
        return state 