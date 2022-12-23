
import Renderer
import threading
import pygame
import time
import Simulation
import CONFIG

def main():

    # Setup
    simulation = Simulation.Simulation()
    simulation.generate_initial_map()
    simulation.generate_initial_agents()
    rendering_thread = threading.Thread(target=Renderer.start_rendering, daemon=None)
    if(CONFIG.DO_RENDER):
        rendering_thread.start()
    time.sleep(1)
    print("Start: ",len(simulation.sim_world.world_agents))

    # Loop 
    i = 0
    while(i < CONFIG.NUM_GENERATIONS and len(simulation.sim_world.world_agents) != 0):
        simulation.simulate()
        if(CONFIG.DO_RENDER):
            update1 = pygame.event.Event(Renderer.UPDATE_FOOD_OVERLAY, message=simulation.sim_world.get_world_food_overlay())
            pygame.event.post(update1)
            update2 = pygame.event.Event(Renderer.UPDATE_AGENT_OVERLAY, message=simulation.sim_world.get_world_agent_overlay())
            pygame.event.post(update2)
        time.sleep(.2)
        i = i + 1
    
    # Processing
    print("End: ", len(simulation.sim_world.world_agents))
    highest_score = 0
    agent_index = 0
    for i in range(len(simulation.sim_world.world_agents)):
        if(simulation.sim_world.world_agents[i].get_agent_fitness_score() > highest_score):
            highest_score = simulation.sim_world.world_agents[i].get_agent_fitness_score()
            agent_index = i
    simulation.sim_world.world_agents[agent_index].print_agent_stats()

    # Teardown
    if(CONFIG.DO_RENDER):
        stop_rendering = pygame.event.Event(Renderer.STOP_RENDERING, message=False)
        pygame.event.post(stop_rendering)
    print("Done")


main()