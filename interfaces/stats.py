import math

class Stats:

    def __init__(self, level, b_hp, b_atk, b_defe, b_spatk, b_spdef):

        self.level = level
        self.hp = self.hp_base_to_value(b_hp)
        self.atk = self.base_to_value(b_atk)
        self.defe = self.base_to_value(b_defe)
        self.spatk = self.base_to_value(b_spatk)
        self.spdef = self.base_to_value(b_spdef)

        self.max_hp = self.hp
    
    def hp_base_to_value(self, b):
        value = math.floor((0.01 * ((2 * b) * self.level)) + self.level + 10)
        return value
    
    def base_to_value(self, b):
        value = math.floor(0.01 * ((2 * b) * self.level) + 5)
        return value




        
