class ModelState:

    def __init__(self, player_hp_percent, enemy_hp_percent, player_type, enemy_type):
        self.player_hp = int(player_hp_percent)
        self.enemy_hp = int(enemy_hp_percent)
        self.player_type = int(player_type)
        self.enemy_type = int(enemy_type)