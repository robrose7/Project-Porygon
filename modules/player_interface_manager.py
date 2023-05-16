# Will Control All User Input Methods
# Future Scope: Interface for training model
def navigate_menu(input, selected_move_index):
    if input == "left":
        match selected_move_index:
            case 0:
                selected_move_index = 0
            case 1:
                selected_move_index = 0
            case 2:
                selected_move_index = 2
            case 3:
                selected_move_index = 2
    elif input == "up":
        match selected_move_index:
            case 0:
                selected_move_index = 0
            case 1:
                selected_move_index = 1
            case 2: 
                selected_move_index = 0
            case 3:
                selected_move_index = 1
    elif input == "right":
        match selected_move_index:
            case 0:
                selected_move_index = 1
            case 1:
                selected_move_index = 1
            case 2: 
                selected_move_index = 3
            case 3:
                selected_move_index = 3
    elif input == "down":
        match selected_move_index:
            case 0:
                selected_move_index = 2
            case 1:
                selected_move_index = 3
            case 2: 
                selected_move_index = 2
            case 3:
                selected_move_index = 3

    return selected_move_index
    