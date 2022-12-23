
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
                do_populate = random.randint(0,5)
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
        for i in range(CONFIG.NUMBER_HIDDEN_LAYERS):
            dimension = random.randint(CONFIG.MIN_HIDDEN_NEURONS, CONFIG.MAX_HIDDEN_NEURONS)
            self.create_hidden_layer_matrix(dimension=dimension)
        self.create_output_matrix()

    def get_output_vector(self, input_vector):
        #if(len(input_vector) != len(self.matrices[0])):
        #    buffer_num = len(self.matrices[0]) - len(input_vector)
        #    if(buffer_num > 0):
        #        for i in range(buffer_num):
        #            input_vector.append(0)
        #    else:
        #        print("Input vector too large!!!!!!")
        current_vector = input_vector
        for i in range(len(self.matrices)):
            current_vector = np.matmul(current_vector,self.matrices[i])
        return current_vector
