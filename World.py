
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

    def get_number_of_agents_on_a_plot(self,x, y):
        num_agents = 0
        for _ in range(len(self.world_agents)):
            if(self.world_agents[_].locationx == x and self.world_agents[_].locationy == y):
                num_agents = num_agents + 1
        return num_agents

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
            if(key == "base_aggression"):
                self.aggression = value
            if(key == "base_ambition"):
                self.ambition = value
            if(key == "sex"):
                self.sex = value

    # Attributes
    health = 5
    wealth = 0
    age = 10
    alive = 1

    locationx = 0
    locationy = 0

    base_aggression = .5
    base_ambition = .5

    sex = "male"
    offspring = 0

    def print_agent_stats(self):
        print("[Age]: ", self.age, "[Health]: ", self.health, "[Wealth]: ", self.wealth, "[Ambition]: ", self.ambition, "[SEX]: ", self.sex)
