
import CONFIG
import World
import random

class Simulation:
    World.sim_world = []

    def __init__(self):
        self.sim_world = World.World()

    def generate_initial_map(self):
        for i in range(0, CONFIG.MAP_DIMENSION):
            col = []
            for j in range(0, CONFIG.MAP_DIMENSION):
                _yield = random.randint(1, 100)
                if(_yield <= CONFIG.DESERT_CHANCE):
                    _yield = 0
                elif(_yield > CONFIG.DESERT_CHANCE and _yield <= CONFIG.FOOD_1_CHANCE):
                    _yield = 1
                elif(_yield > CONFIG.FOOD_1_CHANCE and _yield <= CONFIG.FOOD_2_CHANCE):
                    _yield = 2
                elif(_yield > CONFIG.FOOD_2_CHANCE and _yield <= CONFIG.FOOD_3_CHANCE):
                    _yield = 3
                elif(_yield > CONFIG.FOOD_3_CHANCE and _yield <= CONFIG.FOOD_4_CHANCE):
                    _yield = 4
                else:
                    _yield = 5
                col.append(World.LandPlot(_yield))
            self.sim_world.world_map.append(col)

    def generate_initial_agents(self):
        for _ in range(CONFIG.NUM_INITIAL_AGENTS):
            x = random.randint(0, CONFIG.MAP_DIMENSION-1)
            y = random.randint(0, CONFIG.MAP_DIMENSION-1)
            new_agent = World.Agent(locationx = x, locationy = y, id = len(self.sim_world.world_agents) + 1)
            new_agent.cortex.create_random_neural_network()
            self.sim_world.world_agents.append(new_agent)

            
    # Provide information about the world and have agent's execute their turn, then update the world accordingly
    def simulate(self):
        new_agents = []
        IDs_of_Dead = []
        for i in range(len(self.sim_world.world_agents)):
            if(self.sim_world.world_agents[i].alive == 1):
                agent_decision = "none"
                # Get the enviornment
                location_yield = self.sim_world.world_map[self.sim_world.world_agents[i].locationx][self.sim_world.world_agents[i].locationy].food_yield
                cohabiting_agents = self.sim_world.get_agents_at_location(self.sim_world.world_agents[i].locationx, self.sim_world.world_agents[i].locationy)
                number_cohabitants = len(cohabiting_agents) - 1
                # neighboring_plots = self.sim_world.get_neighboring_plots()

                agent_decision = self.sim_world.world_agents[i].execute_turn(location_yield, cohabiting_agents)
                
                # Implement agent decisions that impact the world beyond them
                if(agent_decision == "PROCREATE"):
                    if(number_cohabitants > 0 and self.sim_world.world_agents[i].wealth > CONFIG.REPRODUCTION_COST):
                        self.sim_world.world_agents[i].wealth = self.sim_world.world_agents[i].wealth - CONFIG.REPRODUCTION_COST
                        self.sim_world.world_agents[i].offspring_count = self.sim_world.world_agents[i].offspring_count + 1
                        id = len(self.sim_world.world_agents) + 1
                        new_agent = World.Agent(locationx = self.sim_world.world_agents[i].locationx, locationy = self.sim_world.world_agents[i].locationy, age = 0, wealth = 0, health = 5, id = id)
                        new_agent.cortex.create_random_neural_network()
                        new_agents.append(new_agent)

                if(agent_decision == "MOVE"):
                    movement = random.randint(0,3)  # left, right, up, down
                    if(movement == 0 and self.sim_world.world_agents[i].locationx != 0):
                        self.sim_world.world_agents[i].locationx = self.sim_world.world_agents[i].locationx - 1
                    if(movement == 1 and self.sim_world.world_agents[i].locationx != CONFIG.MAP_DIMENSION - 1):
                        self.sim_world.world_agents[i].locationx = self.sim_world.world_agents[i].locationx + 1
                    if(movement == 2 and self.sim_world.world_agents[i].locationy != 0):
                        self.sim_world.world_agents[i].locationy = self.sim_world.world_agents[i].locationy - 1
                    if(movement == 3 and self.sim_world.world_agents[i].locationy != CONFIG.MAP_DIMENSION - 1):
                        self.sim_world.world_agents[i].locationy = self.sim_world.world_agents[i].locationy + 1

                
                if(agent_decision == "FIGHT"):
                    if(number_cohabitants > 0):
                        index_of_defeated = random.randint(0, number_cohabitants)
                        IDs_of_Dead.append(cohabiting_agents[index_of_defeated])
                        if(IDs_of_Dead.count(self.sim_world.world_agents[i].ID) == 0):
                            self.sim_world.world_agents[i].foes_defeated = self.sim_world.world_agents[i].foes_defeated + 1

                if(agent_decision == "NONE"):
                    self.sim_world.world_agents[i].alive = 0

        self.sim_world.world_agents = [x for x in self.sim_world.world_agents if x.alive == 1 and IDs_of_Dead.count(x.ID) == 0]
        self.sim_world.world_agents = self.sim_world.world_agents + new_agents

