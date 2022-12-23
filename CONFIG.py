######################################################
#                                                    #
#                   Configuration                    #
#                                                    #
######################################################


MAP_DIMENSION = 100
NUM_INITIAL_AGENTS = 1000
NUM_GENERATIONS = 100

DO_RENDER = True

######################################################
#                                                    #
#                Renderer Settings                   #
#                                                    #
######################################################


# Screen Sizing
SCREENSIZE = WIDTH, HEIGHT = 1500, 1000
PLOT_SIZE = 900

# Colors
BLACK = (0, 0, 0)
DARK_GREY = (75, 75, 57)
GREY = (160, 160, 160)
LIGHT_GREY = (200, 200, 200)
BROWN = (102, 0, 0)
RED = (255, 0, 0)
GREEN_1 = (0, 255, 0)
GREEN_2 = (0, 204, 0)
GREEN_3 = (0, 153, 0)
GREEN_4 = (0, 102, 0)
GREEN_5 = (0, 70, 0)
PALE_YELLOW = (255, 255, 204)

# Grid Setting
LINE_WIDTH = 1
BASE_COLOR = LIGHT_GREY
AGENT_COLOR = RED
LINE_COLOR = GREY
BORDER_COLOR = BLACK


######################################################
#                                                    #
#                World Settings                      #
#                                                    #
######################################################


DESERT_CHANCE = 85
FOOD_1_CHANCE = 90
FOOD_2_CHANCE = 94
FOOD_3_CHANCE = 97
FOOD_4_CHANCE = 99
FOOD_5_CHANCE = 100

######################################################
#                                                    #
#                Agent Settings                      #
#                                                    #
######################################################

NEIGHBORHOOD_TYPES = ["NEUMANN", "MOORE"]       # Moore includes diagnals
NEIGHBORHOOD_TYPE_USED = "MOORE"
VIEWING_DISTANCE = 1

REPRODUCTION_COST = 10

PRIMITIVE_INPUTS = ["AGENT_HEALTH", "LOCATION_YIELD", "NUMBER_COHABITANTS", "AGENT_WEALTH", "AGENT_OFFSPRING_COUNT"] # "AGENT_WEALTH", "AGENT_OFFSPRING_COUNT", "LOCATION_COHABITANTS", "NEIGHBOR_YIELDS", "NEIGHBOR_COHABITANTS"] #... Need to think about these more
PRIMITIVE_OPERATORS = ["+", "-", "*", "/"]

OUTPUT_ACTIONS = ["WAIT", "MOVE", "PROCREATE", "FIGHT"] #, "TRADE"]

######################################################
#                                                    #
#                Neural Net Settings                 #
#                                                    #
######################################################

MIN_HIDDEN_NEURONS = 1
MAX_HIDDEN_NEURONS = 8
MAX_WEIGHT_VALUE = 100
MIN_WEIGHT_VALUE = -100
NUMBER_HIDDEN_LAYERS = 1

GENOME_FILE = "C:\SourceCode\Python\CASimulation\saved_genomes\survivors.txt"