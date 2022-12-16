
import Renderer
import threading
import pygame
import time
import Simulation




def main():

    # Setup
    simulation = Simulation.Simulation()
    simulation.generate_initial_map()
    simulation.generate_initial_agents()
    rendering_thread = threading.Thread(target=Renderer.start_rendering, daemon=None)
    rendering_thread.start()
    time.sleep(.5)
    print("Start: ",len(simulation.sim_world.world_agents))

    # Loop 
    for i in range(0,50):
        simulation.move_agents()
        update1 = pygame.event.Event(Renderer.UPDATE_FOOD_OVERLAY, message=simulation.sim_world.get_world_food_overlay())
        pygame.event.post(update1)
        update2 = pygame.event.Event(Renderer.UPDATE_AGENT_OVERLAY, message=simulation.sim_world.get_world_agent_overlay())
        pygame.event.post(update2)
        time.sleep(.5)
    
    print("End: ",len(simulation.sim_world.world_agents))
  #  for i in range(len(simulation.sim_world.world_agents)):
  #      simulation.sim_world.world_agents[i].print_agent_stats()
    
    # Teardown
    stop_rendering = pygame.event.Event(Renderer.STOP_RENDERING, message=False)
    pygame.event.post(stop_rendering)
    print("Done")


main()