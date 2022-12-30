
import numpy as np
import random
import CONFIG

class NeuralNetwork:
    # A gene is a node ID and vector of weights 
    matrices = []

    def __init__(self):
        self.matrices = []

    def create_input_matrix(self):
        self.matrices.append(np.identity(len(CONFIG.PRIMITIVE_INPUTS)))

    def create_hidden_layer_matrix(self, dimension):
        # Create an n-dimensional square array filled with zeros
        matrix = np.zeros((self.matrices[-1].shape[1] ,dimension))
        # Fill the array with random values between
        for i in range(self.matrices[-1].shape[1]):
            for j in range(dimension):
                do_populate = random.randint(0,4)
                if(do_populate != 5):
                    matrix[i, j] = (random.randint(CONFIG.MIN_WEIGHT_VALUE, CONFIG.MAX_WEIGHT_VALUE) / 100)
        self.matrices.append(matrix)

    def create_output_matrix(self):
        dimension1 = self.matrices[-1].shape[1]
        dimension2 = len(CONFIG.OUTPUT_ACTIONS)
        matrix = np.zeros((dimension1, dimension2))
        for i in range(dimension1):
            for j in range(dimension2):
                matrix[i, j] = random.randint(CONFIG.MIN_HIDDEN_NEURONS, CONFIG.MAX_HIDDEN_NEURONS) / 100
        self.matrices.append(matrix)

    def create_random_neural_network(self):
        self.create_input_matrix()
        number_layers = random.randint(0, CONFIG.MAX_NUMBER_HIDDEN_LAYERS)
        for i in range(number_layers):
            dimension = random.randint(CONFIG.MIN_HIDDEN_NEURONS, CONFIG.MAX_HIDDEN_NEURONS)
            self.create_hidden_layer_matrix(dimension=dimension)
        self.create_output_matrix()

    def get_output_vector(self, input_vector):
        current_vector = input_vector
        for i in range(len(self.matrices)):
            current_vector = np.matmul(current_vector,self.matrices[i])
        return current_vector

    def mutate_cortex(self):
        for i in range(1,len(self.matrices)-1):
            for j in range(self.matrices[i].shape[0]):
                for k in range(self.matrices[i].shape[1]):
                    mutate = random.randint(0,10000)
                    if(mutate > 9999):
                        add = (random.randint(CONFIG.MIN_WEIGHT_VALUE / 10, CONFIG.MAX_WEIGHT_VALUE / 10) / 100)
                        print("EVENT: Mutation by ", add, " amount!")
                        self.matrices[i][j][k] = self.matrices[i][j][k] + add

    def print_cortex_details(self):
        nodes_per_layer = []
        for i in range(len(self.matrices)):
            nodes_per_layer.append(self.matrices[i].shape[1])

        print("CORTEX > [LAYERS]:", len(self.matrices), "[NODES PER LAYER]:", nodes_per_layer)