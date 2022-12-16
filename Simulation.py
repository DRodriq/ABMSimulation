
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
            ambition = random.randint(0, 100) / 100
            aggression = random.randint(0, 100) / 100
            sex_num = random.randint(0,1)
            if(sex_num == 0):
                sex = "male"
            else:
                sex = "female"
            self.sim_world.world_agents.append(World.Agent(locationx = x, locationy = y, base_ambition = ambition, base_aggression = aggression, sex = sex))



# Needs a lot of work. ---->
    def move_agents(self):
        # Will Agent Move?
        
        for i in range(len(self.sim_world.world_agents)):
            if(self.sim_world.world_agents[i].alive == 1):

                food_secure = False

                # Assess the external situation 
                abs_yield = self.sim_world.world_map[self.sim_world.world_agents[i].locationx][self.sim_world.world_agents[i].locationy].food_yield
                shared_population = self.sim_world.get_number_of_agents_on_a_plot(self.sim_world.world_agents[i].locationx, self.sim_world.world_agents[i].locationy) - 1
                current_yield = abs_yield - shared_population if abs_yield - shared_population >= 0 else 0

                # Are we food secure?
                if(current_yield != 0):
                    food_secure = True
                
                # Give reward
                self.sim_world.world_agents[i].health = self.sim_world.world_agents[i].health + current_yield - 1
                self.sim_world.world_agents[i].age = self.sim_world.world_agents[i].age + 1

                # Is dead?
                if(self.sim_world.world_agents[i].health == 0):
                    self.sim_world.world_agents[i].alive = 0
                
                else:
                    will_move = not(food_secure)

                    if(will_move):
                        movement = random.randint(0,3)  # left, right, up, down
                        if(movement == 0 and self.sim_world.world_agents[i].locationx != 0):
                            self.sim_world.world_agents[i].locationx = self.sim_world.world_agents[i].locationx - 1
                        if(movement == 1 and self.sim_world.world_agents[i].locationx != CONFIG.MAP_DIMENSION - 1):
                            self.sim_world.world_agents[i].locationx = self.sim_world.world_agents[i].locationx + 1
                        if(movement == 2 and self.sim_world.world_agents[i].locationy != 0):
                            self.sim_world.world_agents[i].locationy = self.sim_world.world_agents[i].locationy - 1
                        if(movement == 3 and self.sim_world.world_agents[i].locationy != CONFIG.MAP_DIMENSION - 1):
                            self.sim_world.world_agents[i].locationy = self.sim_world.world_agents[i].locationy + 1
            
        self.sim_world.world_agents = [x for x in self.sim_world.world_agents if not x.alive == 0]