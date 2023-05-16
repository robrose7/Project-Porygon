from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np

class Brain: 
    def __init__(self) -> None:
        self.brain = self.initialize_brain()

    def initialize_brain(self):
        # Define the number of inputs and outputs
        num_inputs = 4
        num_outputs = 2

        # Define the neural network model
        model = Sequential()
        model.add(Dense(32, input_dim=num_inputs, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(num_outputs, activation='softmax'))

        # Compile the model with the Adam optimizer and mean squared error loss function
        model.compile(optimizer=Adam(lr=0.001), loss='mse')
        return model
    
    def choose_move(self, epsilon, q_table, state):
        # Start the brain here
        if np.random.rand() < epsilon:
            action = np.random.randint(4)
        else:
            q_values = q_table[state.player_hp, state.enemy_hp, state.player_type, state.enemy_type, :]
            action = np.argmax(q_values)
        return action

