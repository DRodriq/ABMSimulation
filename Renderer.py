
import sys
import pygame
from pygame import USEREVENT
from pygame.locals import KEYDOWN, K_q
import time
import CONFIG

_VARS = {'surf': False, 'gridWH': CONFIG.PLOT_SIZE,
         'gridOrigin': (25, 25), 'lineWidth': CONFIG.LINE_WIDTH}

# Events
UPDATE_FOOD_OVERLAY = USEREVENT+1
STOP_RENDERING = USEREVENT+2
UPDATE_AGENT_OVERLAY = USEREVENT+3

def start_rendering():
  pygame.init()
  while True:
    _VARS['surf'] = pygame.display.set_mode(CONFIG.SCREENSIZE)
    _VARS['surf'].fill(CONFIG.BASE_COLOR)
    drawSquareGrid(
    _VARS['gridOrigin'], _VARS['gridWH'], CONFIG.MAP_DIMENSION)
    checkEvents()
    pygame.display.update()
    time.sleep(.5)
        
# Parameters: A 2D map of integers
# Precondition: A partially rendered world map
# Postcondition: A populated world map with tiles representing the overlay 
def drawOverlay(overlay, overlayType):
  #gridCells = cellMAP.shape[0]
  dimension = len(overlay)
  cellBorderPadding = 1
  celldimX = celldimY = (_VARS['gridWH']/dimension) - (cellBorderPadding*2)
  # DOUBLE LOOP
  for row in range(0, dimension):
    for column in range(0, dimension):
      # Is the grid cell tiled ?
      if(overlayType == "FOOD"):
        x = _VARS['gridOrigin'][0] + (celldimY*row) + cellBorderPadding + (2*row*cellBorderPadding) + _VARS['lineWidth']/2
        y = _VARS['gridOrigin'][1] + (celldimX*column) + cellBorderPadding + (2*column*cellBorderPadding) + _VARS['lineWidth']/2
        drawSquareCell(x, y, celldimX, celldimY, getFoodColor(overlay[column][row]))
      elif(overlayType == "AGENT"):
        if(overlay[column][row] != 0):
          x = _VARS['gridOrigin'][0] + ( (celldimY*row + celldimY*(row+1))/2) + cellBorderPadding + (2*row*cellBorderPadding) + _VARS['lineWidth']/2
          y = _VARS['gridOrigin'][1] + ( (celldimX*column + celldimX*(column+1))/2) + cellBorderPadding + (2*column*cellBorderPadding) + _VARS['lineWidth']/2
          drawCircleCell(x, y, overlay[column][row], CONFIG.AGENT_COLOR)

# Draw filled rectangle at coordinates
def drawSquareCell(x, y, dimX, dimY, COLOR):
  pygame.draw.rect(
    _VARS['surf'], COLOR,
    (x, y, dimX, dimY)
  )

def drawCircleCell(x, y, value, COLOR):
  radius = (value) * (value/100 + 1)
  pygame.draw.circle(_VARS['surf'], COLOR, (x,y), radius)

def drawSquareGrid(origin, gridWH, cells):
  CONTAINER_WIDTH_HEIGHT = gridWH
  cont_x, cont_y = origin

  # DRAW Grid Border:
  # TOP lEFT TO RIGHT
  pygame.draw.line(
    _VARS['surf'], CONFIG.BORDER_COLOR,
    (cont_x, cont_y),
    (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y), _VARS['lineWidth'])
  # # BOTTOM lEFT TO RIGHT
  pygame.draw.line(
    _VARS['surf'], CONFIG.BORDER_COLOR,
    (cont_x, CONTAINER_WIDTH_HEIGHT + cont_y),
    (CONTAINER_WIDTH_HEIGHT + cont_x,
      CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])
  # # LEFT TOP TO BOTTOM
  pygame.draw.line(
    _VARS['surf'], CONFIG.BORDER_COLOR,
    (cont_x, cont_y),
    (cont_x, cont_y + CONTAINER_WIDTH_HEIGHT), _VARS['lineWidth'])
  # # RIGHT TOP TO BOTTOM
  pygame.draw.line(
    _VARS['surf'], CONFIG.BORDER_COLOR,
    (CONTAINER_WIDTH_HEIGHT + cont_x, cont_y),
    (CONTAINER_WIDTH_HEIGHT + cont_x,
      CONTAINER_WIDTH_HEIGHT + cont_y), _VARS['lineWidth'])

  # Get cell size, just one since its a square grid.
  cellSize = CONTAINER_WIDTH_HEIGHT/cells

  # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
  for x in range(cells):
      pygame.draw.line(
          _VARS['surf'], CONFIG.LINE_COLOR,
          (cont_x + (cellSize * x), cont_y),
          (cont_x + (cellSize * x), CONTAINER_WIDTH_HEIGHT + cont_y), 2)
  # # HORIZONTAl DIVISIONS
      pygame.draw.line(
        _VARS['surf'], CONFIG.LINE_COLOR,
        (cont_x, cont_y + (cellSize*x)),
        (cont_x + CONTAINER_WIDTH_HEIGHT, cont_y + (cellSize*x)), 2)

def getFoodColor(num):
  if(num == 0):
    return(CONFIG.PALE_YELLOW)
  if(num == 1):
    return(CONFIG.GREEN_1)
  if(num == 2):
    return(CONFIG.GREEN_2)
  if(num == 3):
    return(CONFIG.GREEN_3)
  if(num == 4):
    return(CONFIG.GREEN_4)
  if(num == 5):
    return(CONFIG.GREEN_5)

def checkEvents():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == KEYDOWN and event.key == K_q:
      pygame.quit()
      sys.exit()
    elif event.type == UPDATE_FOOD_OVERLAY:
      drawOverlay(event.message, "FOOD")
    elif event.type == UPDATE_AGENT_OVERLAY:
      drawOverlay(event.message, "AGENT")
    elif event.type == STOP_RENDERING:
      pygame.quit()
      sys.exit()
