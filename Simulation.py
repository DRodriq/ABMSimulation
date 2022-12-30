
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
                if(_yield <= CONFIG.LANDSCAPE_PROFILE[0]):
                    _yield = 0
                elif(_yield > CONFIG.LANDSCAPE_PROFILE[0] and _yield <= CONFIG.LANDSCAPE_PROFILE[1]):
                    _yield = 1
                elif(_yield > CONFIG.LANDSCAPE_PROFILE[1] and _yield <= CONFIG.LANDSCAPE_PROFILE[2]):
                    _yield = 2
                elif(_yield > CONFIG.LANDSCAPE_PROFILE[2] and _yield <= CONFIG.LANDSCAPE_PROFILE[3]):
                    _yield = 3
                elif(_yield > CONFIG.LANDSCAPE_PROFILE[3] and _yield <= CONFIG.LANDSCAPE_PROFILE[4]):
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
        IDs_of_Defeated = []
        for i in range(len(self.sim_world.world_agents)):
            if(self.sim_world.world_agents[i].alive == 1):
                agent_decision = "none"
                # Get the enviornment
                location_yield = self.sim_world.world_map[self.sim_world.world_agents[i].locationx][self.sim_world.world_agents[i].locationy].food_yield
                cohabiting_agents = self.sim_world.get_agents_at_location(self.sim_world.world_agents[i].locationx, self.sim_world.world_agents[i].locationy)
                number_cohabitants = len(cohabiting_agents) - 1
                neighboring_plots = self.sim_world.get_neighboring_plots(self.sim_world.world_agents[i].locationx, self.sim_world.world_agents[i].locationy)

                agent_decision = self.sim_world.world_agents[i].execute_turn(location_yield, cohabiting_agents, neighboring_plots)
                
                # Implement agent decisions that impact the world beyond them
                if(agent_decision == "PROCREATE"):
                    if(len(cohabiting_agents) > 0 and self.sim_world.world_agents[i].wealth > CONFIG.REPRODUCTION_COST):
                        self.sim_world.world_agents[i].wealth = self.sim_world.world_agents[i].wealth - CONFIG.REPRODUCTION_COST
                        new_agents.append(self.simulate_procreation(self.sim_world.world_agents[i], cohabiting_agents))
                        self.sim_world.world_agents[i].wealth = self.sim_world.world_agents[i].wealth - new_agents[-1].wealth
                        self.sim_world.world_agents[i].offspring_count = self.sim_world.world_agents[i].offspring_count+1

                if(agent_decision == "FIGHT"):
                    if(number_cohabitants > 0):
                        IDs_of_Defeated.append(self.simulate_battle(self.sim_world.world_agents[i], cohabiting_agents))
                        self.sim_world.world_agents[i].foes_defeated = self.sim_world.world_agents[i].foes_defeated + 1

                if(agent_decision == "NONE"):
                    self.sim_world.world_agents[i].alive = 0
                
        self.sim_world.world_agents = [x for x in self.sim_world.world_agents if x.alive == 1 and IDs_of_Defeated.count(x.ID) == 0]
        self.sim_world.world_agents = self.sim_world.world_agents + new_agents

    def simulate_procreation(self, agent_y, agent_population):
        # Find agent_x with probability based on fitness score - for now just do highest fitness score
        highest_fitness = 0
        agent_x = agent_y
        for i in range(len(agent_population)):
            if(agent_population[i].get_agent_fitness_score() > highest_fitness):
                agent_x = agent_population[i]
                highest_fitness = agent_population[i].get_agent_fitness_score()
        new_agent_id = len(self.sim_world.world_agents) + 1
        inheritance = random.randint(0, agent_y.wealth)
        new_agent = World.Agent(locationx = agent_y.locationx, locationy = agent_y.locationy, age = 0, wealth = inheritance, health = 5, id = new_agent_id)
        # Want to do some sort of sexual combination of two agents cortices here --->
        x_y = random.randint(0,1)
        if(x_y == 0):
            new_agent.cortex = agent_x.cortex
        else:
            new_agent.cortex = agent_y.cortex
        print("Event: Agent Born")
    #    new_agent.cortex.mutate_cortex()
        return new_agent

    def simulate_battle(self, instigating_agent, agent_population):
        ID_of_defeated = 0
        # Probability based on fitness score - for now just do lowest
        lowest_fitness = 1000
        for i in range(len(agent_population)):
            if(agent_population[i].get_agent_fitness_score() < lowest_fitness):
                ID_of_defeated = agent_population[i].ID
                lowest_fitness = agent_population[i].get_agent_fitness_score()
        print("EVENT: A battle was fought")
        return ID_of_defeated

