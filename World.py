
import CONFIG
import NeuralNet

###################### World Map Classes #########################

# A World is a 2D map of LandPlots and a list of Agents
# Member functions:
#   - Return overlays for rendering: (map_dimension x map_dimension) grids with discrete relevant values 
class World:
    def __init__(self):
        self.world_map = []
        self.world_agents = []
    world_map = []
    world_agents = []

    def get_world_agent_overlay(self):
        rows, cols = (len(self.world_map), len(self.world_map))
        overlay = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(len(self.world_agents)):
            overlay[self.world_agents[i].locationx][self.world_agents[i].locationy] = overlay[self.world_agents[i].locationx][self.world_agents[i].locationy] + 1
        return overlay

    def get_world_food_overlay(self):
        rows, cols = (len(self.world_map), len(self.world_map))
        overlay = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(0, len(self.world_map)):
            for j in range(0, len(self.world_map)):
                overlay[i][j] = self.world_map[i][j].food_yield
        return overlay

    def get_plot_food_value(self, x ,y):
        return self.world_map[x][y].food_yield

    def get_agent_index_by_ID(self, refID):
        for index in range(len(self.world_agents)):
            if(self.world_agents[index].ID == refID):
                return index
    
    def get_agents_at_location(self, x, y):
        agent_IDS = []
        for i in range(len(self.world_agents)):
            if(self.world_agents[i].locationx == x and self.world_agents[i].locationy == y):
                agent_IDS.append(self.world_agents[i].ID)
        return agent_IDS

    def get_neighboring_plots(self, x, y):
        neighboring_plots = []
        LEFT = [x - 1 if x - 1 >= 0 else 0, y]
        RIGHT = [x + 1 if x + 1 <= 99 else 99, y]
        UP = [x, y - 1 if y - 1 <= 0 else 0]
        DOWN = [x, y + 1 if y + 1 <= 99 else 99]
        LEFT_UP = [LEFT[0], UP[1]]
        RIGHT_UP = [RIGHT[0], UP[1]]
        LEFT_DOWN = [LEFT[0], DOWN[1]]
        RIGHT_DOWN = [RIGHT[0], DOWN[1]]
        neighboring_plots.append(self.world_map[LEFT[0]][LEFT[1]])
        neighboring_plots.append(self.world_map[RIGHT[0]][RIGHT[1]])
        neighboring_plots.append(self.world_map[UP[0]][UP[1]])
        neighboring_plots.append(self.world_map[DOWN[0]][DOWN[1]])
        if(CONFIG.NEIGHBORHOOD_TYPE_USED == "MOORE"):
            neighboring_plots.append(self.world_map[LEFT_UP[0]][LEFT_UP[1]])
            neighboring_plots.append(self.world_map[RIGHT_UP[0]][RIGHT_UP[1]])
            neighboring_plots.append(self.world_map[LEFT_DOWN[0]][LEFT_DOWN[1]])
            neighboring_plots.append(self.world_map[RIGHT_DOWN[0]][RIGHT_DOWN[1]])
        return neighboring_plots


# A Landplot is a collection of attributes associated with an individual grid point
class LandPlot:
    def __init__(self, food):
        self.food_yield = food   
    food_yield = 0

# An agent is a ### at a position in the world
class Agent:
    def __init__(self, **kw_params):
        for key, value in kw_params.items():
            if(key == "locationx"):
                self.locationx = value
            if(key == "locationy"):
                self.locationy = value
            if(key == "health"):
                self.health = value
            if(key == "wealth"):
                self.wealth = value
            if(key == "id"):
                self.ID = value
            if(key == "age"):
                self.age = value
        self.cortex = NeuralNet.NeuralNetwork()
    # Stats
    health = 5
    wealth = 0
    age = 0
    offspring_count = 0
    locationx = 0
    locationy = 0

    times_moved = 0
    foes_defeated = 0

    cortex = NeuralNet.NeuralNetwork()

    alive = 1
    ID = 0

    def execute_turn(self, location_yield, neighbors):
        decision = 'NONE'
        if(self.alive == 0):
            return decision

        decision = self.get_decision(LOCATION_YIELD = location_yield, NUMBER_COHABITANTS = len(neighbors))
        self.health = self.health + location_yield - (len(neighbors))

        if(self.health > 5):
            self.wealth = self.wealth + self.health - 5
            self.health = 5

        if(self.health <= 0):
            self.alive = 0
        else:
            self.age = self.age + 1

        return decision

    def get_decision(self, **INPUTS):
        decision = "NONE"
        input_vector = []
        for i in range(len(CONFIG.PRIMITIVE_INPUTS)):
            input_vector.append(0)
        input_vector[0] = self.health
        for key, value in INPUTS.items():
            if(key == CONFIG.PRIMITIVE_INPUTS[1]):
                input_vector[1] = value
            if(key == CONFIG.PRIMITIVE_INPUTS[2]):
                input_vector[2] = value

        output = self.cortex.get_output_vector(input_vector)
        
        largest_outpulse = -100
        index  = 0
        for i in range(len(output)):
            if(output[i] > largest_outpulse):
                largest_outpulse = output[i]
                index = i
        
        if(index == 0):
            decision = "WAIT"
        if(index == 1):
            decision = "MOVE"
            self.times_moved = self.times_moved + 1
        if(index == 2):
            decision = "PROCREATE"
        if(index == 3):
            decision = "FIGHT"

        return decision

    def print_agent_stats(self):
            print("[ID]:", self.ID, "[Age]:", self.age, "[Health]:", self.health, "[Wealth]:", self.wealth, "[Offspring]:", self.offspring_count, "[Moved]:", self.times_moved, "[Foes Defeated]:", self.foes_defeated, "SCORE:", self.get_agent_fitness_score())

    def get_agent_fitness_score(self):
       # print("MOVED: ", self.has_moved, "OFF_SPRING: ", self.offspring_count)
        fitness_score = self.offspring_count + (self.times_moved) + (self.foes_defeated)
        return fitness_score