
import constants
import pygame
 
pygame.init()
        
def draw_battle(window,
    win, 
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
    ): 

    window.fill(constants.WHITE)

    # Stats
    draw_stat_tracker(window=window, win_record=win_record, loss_record=loss_record, master_pokemon_list=master_pokemon_list, player_pokemon=player_pokemon, move_frequency=move_frequency)
    draw_text(window, "Win: " + str(win), 600, 100, constants.FONT_SMALL, constants.BLACK)
    draw_text(window, "Loss: " + str(loss), 600, 130 , constants.FONT_SMALL, constants.BLACK)

    if ai_flag:
        draw_text(window, "Current Move Reward: " + str(current_move_reward), 600, 160, constants.FONT_SMALL, constants.BLACK)
        draw_text(window, "Total Reward: " + str(total_episode_reward), 600, 190, constants.FONT_SMALL, constants.BLACK)

    # Pokemon Name and HP Bars
    draw_text(window, str(enemy_pokemon.name), 150, 100, constants.FONT_LARGE, constants.BLACK)
    draw_hp_bar(window, 50, 125, enemy_pokemon.stats.hp, enemy_pokemon.stats.max_hp)
    draw_text(window, str(player_pokemon.name), 600, 450, constants.FONT_LARGE, constants.BLACK)
    draw_hp_bar(window, 425, 475, player_pokemon.stats.hp, player_pokemon.stats.max_hp)

    # Move Messages
    draw_text(window, player_battle_message, 400, 300, constants.FONT_SMALL, constants.DARK_GREEN if player_supereffective else constants.BLACK)
    draw_text(window, enemy_battle_message, 400, 350, constants.FONT_SMALL, constants.RED if enemy_supereffective else constants.BLACK)

    # Move Option Display
    draw_player_menu(window, player_pokemon, selected_move_index)    

def draw_hp_bar(surface, x, y, hp, max_hp):

    constants.HP_BAR_WIDTH = 300
    constants.HP_BAR_HEIGHT = 40
    constants.HP_BAR_MARGIN = 10
    constants.HP_BAR_BORDER_WIDTH = 10
    # calculate percentage of HP remaining
    hp_percent = float(hp) / max_hp

    # calculate colors based on HP remaining
    if hp_percent > 0.5:
        color = constants.GREEN
    elif hp_percent > 0.2:
        color = constants.YELLOW
    else:
        color = constants.RED

    # calculate dimensions of HP bar
    bar_width = int(hp_percent * constants.HP_BAR_WIDTH)
    bar_height = constants.HP_BAR_HEIGHT

    # calculate coordinates of HP bar
    bar_x = x + constants.HP_BAR_MARGIN
    bar_y = y + constants.HP_BAR_MARGIN

    # draw border of HP bar
    pygame.draw.rect(surface, constants.WHITE, (bar_x - constants.HP_BAR_BORDER_WIDTH, bar_y - constants.HP_BAR_BORDER_WIDTH, constants.HP_BAR_WIDTH + constants.HP_BAR_BORDER_WIDTH * 2, constants.HP_BAR_HEIGHT + constants.HP_BAR_BORDER_WIDTH * 2))

    # draw background of HP bar
    pygame.draw.rect(surface, constants.BLACK, (bar_x, bar_y, constants.HP_BAR_WIDTH, constants.HP_BAR_HEIGHT))

    # draw HP bar
    pygame.draw.rect(surface, color, (bar_x, bar_y, bar_width, bar_height))

    # draw text displaying HP remaining
    font = pygame.font.Font(None, 18)
    text = font.render(str(hp) + '/' + str(max_hp), True, constants.WHITE)
    text_rect = text.get_rect()
    text_rect.center = (x + constants.HP_BAR_MARGIN + constants.HP_BAR_WIDTH / 2, y + constants.HP_BAR_MARGIN + constants.HP_BAR_HEIGHT / 2)
    surface.blit(text, text_rect)

def draw_player_menu(window, player_pokemon, selected_move_index):

    draw_text(window, player_pokemon.moves[0].name + ": " + str(player_pokemon.moves[0].power), 200, 700, constants.FONT_SMALL, constants.RED if selected_move_index == 0 else constants.BLACK)
    draw_text(window, player_pokemon.moves[1].name + ": " + str(player_pokemon.moves[1].power), 600, 700, constants.FONT_SMALL, constants.RED if selected_move_index == 1 else constants.BLACK)
    draw_text(window, player_pokemon.moves[2].name + ": " + str(player_pokemon.moves[2].power), 200, 750, constants.FONT_SMALL, constants.RED if selected_move_index == 2 else constants.BLACK)
    draw_text(window, player_pokemon.moves[3].name + ": " + str(player_pokemon.moves[3].power), 600, 750, constants.FONT_SMALL, constants.RED if selected_move_index == 3 else constants.BLACK)

def draw_win(window):
    window.fill(constants.WHITE)
    draw_text(window, "You win!", 400, 400, constants.FONT_LARGE, constants.BLACK)

def draw_lose(window):
    window.fill(constants.WHITE)
    draw_text(window, 'You lose.', 400, 400, constants.FONT_LARGE, constants.BLACK) 

def remove_text(window, text, x, y, font):
    bg_color = window.get_at((0, 0))
    text_surface = font.render(text, True, bg_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

def draw_text(window, text, x, y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

def draw_stat_tracker(window, win_record, loss_record, master_pokemon_list, player_pokemon, move_frequency):

    FONT = pygame.font.Font(None, 30)

    x = 5
    y = 275
    for i, record in enumerate(win_record):
        text = f"{master_pokemon_list[i].name}: {int(win_record[i])} - {int(loss_record[i])} - {get_win_rate(win_record, loss_record, i)}%"
        text_surface = text_surface = FONT.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        window.blit(text_surface, text_rect)

        y += 25

    for i, move, in enumerate(move_frequency):
        text = f"{player_pokemon.moves[i].name}: {int(move_frequency[i])}"
        text_surface = text_surface = FONT.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        window.blit(text_surface, text_rect)

        y += 25

def get_win_rate(win_record, loss_record, i):

    if(win_record[i] == 0):
        return 0
    if(loss_record[i] == 0):
        return 100

    return int((win_record[i] / (loss_record[i] + win_record[i])) * 100)

