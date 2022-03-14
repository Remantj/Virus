import pygame, random

pygame.init()

WINDOW_RESOLUTION = (900, 900)
NB_POPULATION = 100
screen = pygame.display.set_mode(WINDOW_RESOLUTION)
pygame.display.set_caption("Propagation épidémie")
power = True
clock = pygame.time.Clock()
white = (255, 255, 255)

liste_agents = []
liste_x = []
liste_y = []

def create_agent():
   dico = {}
   x = random.randint(0, WINDOW_RESOLUTION[0])
   y = random.randint(0, WINDOW_RESOLUTION[1])
   dico['x'] = x
   dico['y'] = y
   return dico

def initialisation_population():
   dico = {}
   for i in range(NB_POPULATION):
      dico = create_agent()
      liste_agents.append(dico)

def actualisation_coordonnees():
   liste_x = []
   liste_y = []
   for i in liste_agents:
      liste_x.append(i['x'])
      liste_y.append(i['y'])
   return liste_x, liste_y

def actualisation():
   screen.fill(white)
   modifier_coordonnees()
   liste_x, liste_y = actualisation_coordonnees()
   for i in range(len(liste_agents)):
      pygame.draw.circle(screen, (255,0,0), (liste_x[i], liste_y[i]), 5)

def modifier_coordonnees():
      for i in range(int((20/100)*NB_POPULATION)):
         n = random.randint(0, len(liste_agents)-1)
         nx = random.randint(liste_agents[n]['x']-2, liste_agents[n]['x']+2)
         ny = random.randint(liste_agents[n]['y']-2, liste_agents[n]['y']+2)
         liste_agents[n]['x'] = nx
         liste_agents[n]['y'] = ny



def main():
   global power
   initialisation_population()
   while power:
      actualisation()
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
               power = False

      pygame.display.flip()
      clock.tick(60)



main()