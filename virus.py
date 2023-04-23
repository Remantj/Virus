import pygame, random
from math import sqrt
from matplotlib import pyplot as plt

pygame.init()

###################################
#### Variables gérant le modèle ###
###################################

#Taille de la fenetre
WINDOW_RESOLUTION = (900, 900)

#Paramètres généraux
NB_POPULATION = 400
NOMBRE_INFECTE_DEBUT = 5

DISTANCE_CONTAMINATION = 50
TAUX_MORTALITE = 50
TAUX_INFECTION = 50

TEMPS_INFECTION_MAX = 25
TEMPS_IMMUNITE_MAX = 25

#Paramètres de la simulation
SIMULATION = True   #Activer ou non la simulation visuelle
AFFICHER_LEGENDE = True   #Variable permettant d'afficher ou non la légende
AFFICHER_GRAPHIQUES = True   #Afficher ou non les graphiques à la fin de la simulation
MOYENNE = 5     #Echelle de la moyenne pour les courbes
VITESSE = 1     #Experimental, vitesse de la simulation


###################################


#Initialisation de la fenêtre
if SIMULATION:
    fenetre = pygame.display.set_mode(WINDOW_RESOLUTION)
    pygame.display.set_caption("Propagation épidémie")

#Definition des variables initiales
power = True
clock = pygame.time.Clock()
blanc = (255, 255, 255)
rose = (240, 180, 195)
rouge = (255, 0, 0)
bleu = (0, 0, 250)
vert = (0, 255, 25)
seconde = 0
seconde_mouvement = 0
liste_agents = []
liste_x = []
liste_y = []

#Listes pour les graphiques
cpt_mort = 0
nbre_morts = []
cpt_immunite = 0
nbre_immunises = []
cpt_infecte = 0
nbre_infectes = []

# Variables du menu principal
taille_police = 36
police = pygame.font.Font(None,taille_police)
titre = police.render("Légende", True, pygame.Color("Black"))
texte1 = police.render("Individu sain", True, pygame.Color("Black"))
texte2 = police.render("Individu immunisé", True, pygame.Color("Black"))
texte3 = police.render("Individu contaminé", True, pygame.Color("Black"))
texte4 = police.render("Veuillez presser une touche", True, pygame.Color("Black"))


# Fonction permettant la création d'un agent
def creation_agent():
    dico = {}
    x = random.randint(0, WINDOW_RESOLUTION[0])
    y = random.randint(0, WINDOW_RESOLUTION[1])
    dico['x'] = x
    dico['y'] = y
    dico['dest'] = (random.randint(0, WINDOW_RESOLUTION[0]), random.randint(0, WINDOW_RESOLUTION[1]))
    dico['wait'] = random.randint(10, 100)
    dico["infection"] = 0
    dico["immunite"] = 0
    dico["test_mortalite"] = 0
    return dico

# Fonction calculant la distance entre deux agents
def distance(agent1, agent2):
    return sqrt((agent1['x'] - agent2['x'])**2 + (agent1['y'] - agent2['y'])**2)

# Fonction permettant d'initialiser la population avec NB_POPULATION agents
def initialisation_population():
    global cpt_infecte
    dico = {}
    #Creation des agents
    for i in range(NB_POPULATION):
        dico = creation_agent()
        liste_agents.append(dico)
    #Infection d'une partie d'entre eux
    for i in range(NOMBRE_INFECTE_DEBUT):
        n = random.randint(0, NB_POPULATION-1)
        while(liste_agents[n]["infection"] > 0):
            n = random.randint(0, NB_POPULATION-1)
        liste_agents[n]["infection"] = random.randint(5, TEMPS_INFECTION_MAX)
        liste_agents[n]["immunite"] = random.randint(5, TEMPS_IMMUNITE_MAX)
        liste_agents[n]["test_mortalite"] = 1
        cpt_infecte += 1

# Fonction permettant de modifier les coordonnées selon un mouvement prédéfini
def modifier_coordonnees():
    #Deplacement d'une partie de la population
    for i in range(int((80/100)*NB_POPULATION)):
        n = random.randint(0, len(liste_agents)-1)
        if(liste_agents[n]['wait'] > 0):
            liste_agents[n]['wait'] -= 1
        else:
            #Calcul des nouvelles coordonnées
            nx = (liste_agents[n]['dest'][0] - liste_agents[n]['x'])/150 * VITESSE + liste_agents[n]['x']
            ny = (liste_agents[n]['dest'][1] - liste_agents[n]['y'])/150 * VITESSE + liste_agents[n]['y']
            if(sqrt((nx - liste_agents[n]['dest'][0])**2 + (ny - liste_agents[n]['dest'][1])**2) < 50):
                liste_agents[n]['dest'] = (random.randint(0, WINDOW_RESOLUTION[0]), random.randint(0, WINDOW_RESOLUTION[1]))
                liste_agents[n]['wait'] = random.randint(10, 100)/VITESSE
            liste_agents[n]['x'] = nx
            liste_agents[n]['y'] = ny

# Fonction gérant les contaminations et l'immunité
def contamination():
    global cpt_immunite, cpt_infecte
    for i in liste_agents:
        if i["infection"] > 0:
            for j in liste_agents:
                if ((j["infection"] == 0) and (j["immunite"] == 0) and (distance(i, j) < DISTANCE_CONTAMINATION)):
                    #Infection de l'agent
                    n = random.randint(1, 100)
                    if n <= TAUX_INFECTION:
                        cpt_infecte += 1
                        j["infection"] = random.randint(5, TEMPS_INFECTION_MAX)
                        j["immunite"] = random.randint(5, TEMPS_IMMUNITE_MAX)
                        j["test_mortalite"] = 1
        #Verification de la fin du temps d'infection de l'agent
        if ((i["infection"] == 0) and (i["immunite"] > 0)):
            check_fin_immunite = False
            if(i["immunite"] > 0):
                check_fin_immunite = True
            i["immunite"] -= 1
            if(check_fin_immunite and i["immunite"] == 0):
                cpt_immunite -= 1

# Fonction gérant la mortalité
def mortalite():
    global cpt_mort, NB_POPULATION, cpt_infecte, cpt_immunite
    compteur_morts = 0
    for i in liste_agents:
       if i["infection"] > 0:
            i["infection"] -= 1
            if i["test_mortalite"] == 1:
                n = random.randint(1, i["infection"])
                if (n == 1):
                    #Test de mortalité
                    i["test_mortalite"] = 0
                    p = random.randint(1, 100)
                    if p <= TAUX_MORTALITE:
                        #Disparition de l'agent
                        liste_agents.remove(i)
                        NB_POPULATION -= 1
                        cpt_mort += 1
                        compteur_morts += 1
                        cpt_infecte -= 1
            if(i["infection"] == 0):
                #Diminution du temps d'infection restant
                cpt_infecte -= 1
                cpt_immunite += 1
    if NB_POPULATION > 0:
        nbre_morts.append(compteur_morts/NB_POPULATION)
        

            

# Fonction permettant d'actualiser les coordonnées dans les deux listes x et y afin de pouvoir tracer un point
def actualisation_coordonnees():
    liste_x = []
    liste_y = []
    for i in liste_agents:
        liste_x.append(i['x'])
        liste_y.append(i['y'])
    return liste_x, liste_y


# Fonction permettant d'actualiser le programme et de tracer les nouveaux points
def actualisation():
    global seconde, cpt_immunite, cpt_infecte, liste_x, liste_y, cpt_tour
    
    if SIMULATION:
        fenetre.fill(blanc)

    if (SIMULATION):
        #Tests de contamination et mort des agents, à intervalle d'une seconde environ
        if(pygame.time.get_ticks() - seconde >= 1000/VITESSE):
            seconde = pygame.time.get_ticks()
            contamination()
            mortalite()
            if NB_POPULATION > 0:
                nbre_immunises.append(cpt_immunite/NB_POPULATION)
                nbre_infectes.append(cpt_infecte/NB_POPULATION)
    else:
        contamination()
        mortalite()
        if NB_POPULATION > 0:
            nbre_immunises.append(cpt_immunite/NB_POPULATION)
            nbre_infectes.append(cpt_infecte/NB_POPULATION)

    if SIMULATION:
        modifier_coordonnees()
        liste_x, liste_y = actualisation_coordonnees()
    else:
        for i in range(60):
            modifier_coordonnees()
            liste_x, liste_y = actualisation_coordonnees()

    if SIMULATION:
        for i in range(len(liste_agents)):
            if (liste_agents[i]["infection"] > 0):
                point_couleur = rouge
            elif (liste_agents[i]["immunite"] > 0):
                point_couleur = vert
            else:
                point_couleur = bleu
            pygame.draw.circle(fenetre, point_couleur, (int(liste_x[i]), int(liste_y[i])), 5)

def test_fin():
    global cpt_mort, cpt_infecte
    if NB_POPULATION == 0:
        print("Toute la population est morte")
        print(f"Nombre de morts: {cpt_mort}")
        return 0
    if cpt_infecte == 0:
        print("Le virus a disparu")
        print(f"Nombre de survivant: {NB_POPULATION}")
        return 0
    return 1

# Fonction permettant d'afficher le menu principal contenant la légende
def menu_principal():
    global power, AFFICHER_LEGENDE, taille_police
    while AFFICHER_LEGENDE:
        fenetre.fill(blanc)
        fenetre.blit(titre, (int(WINDOW_RESOLUTION[0]/2.3), int(WINDOW_RESOLUTION[1]/10)))
        fenetre.blit(texte1, (int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/3)))
        fenetre.blit(texte2, (int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/3)+2*taille_police))
        fenetre.blit(texte3, (int(WINDOW_RESOLUTION[0]/2), int(WINDOW_RESOLUTION[1]/3)+4*taille_police))
        fenetre.blit(texte4, (int(WINDOW_RESOLUTION[0]/3), int(WINDOW_RESOLUTION[1]/1.1)))
        pygame.draw.circle(fenetre, bleu, (int(WINDOW_RESOLUTION[0]/2.2), int(WINDOW_RESOLUTION[1]/2.9)), 8)
        pygame.draw.circle(fenetre, vert, (int(WINDOW_RESOLUTION[0]/2.2), int(WINDOW_RESOLUTION[1]/2.9)+2*taille_police), 8)
        pygame.draw.circle(fenetre, rouge, (int(WINDOW_RESOLUTION[0]/2.2), int(WINDOW_RESOLUTION[1]/2.9)+4*taille_police), 8)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                AFFICHER_LEGENDE = False
            if event.type == pygame.QUIT:
                AFFICHER_LEGENDE = False
                power = False


# Fonction permettant de créer et d'afficher les graphiques
def graphiques():
    nbre_morts_moyenne = []
    nbre_infectes_moyenne = []
    nbre_immunises_moyenne = []
    cpt = 0
    cumul_mort = 0
    cumul_immunite = 0
    cumul_infection = 0

    for i in range(len(nbre_morts)):
        if cpt < MOYENNE:
            cpt += 1
            cumul_mort += nbre_morts[i]
            cumul_immunite += nbre_immunises[i]
            cumul_infection += nbre_infectes[i]
        else:
            nbre_morts_moyenne.append(cumul_mort/cpt)
            nbre_infectes_moyenne.append(cumul_infection/cpt)
            nbre_immunises_moyenne.append(cumul_immunite/cpt)
            cpt = 0
            cumul_mort = 0
            cumul_immunite = 0
            cumul_infection = 0
    if(cpt > 0):
        nbre_morts_moyenne.append(cumul_mort/cpt)
        nbre_infectes_moyenne.append(cumul_infection/cpt)
        nbre_immunises_moyenne.append(cumul_immunite/cpt)

    #Courbe morts
    plt.plot([i * MOYENNE for i in range(len(nbre_immunises_moyenne))], nbre_immunises_moyenne, color="green")

    #Courbe nbre infectes
    plt.plot([i * MOYENNE for i in range(len(nbre_infectes_moyenne))], nbre_infectes_moyenne, color="red")
    plt.show()

    #Courbe nbre immunisés
    plt.plot([i * MOYENNE for i in range(len(nbre_morts_moyenne))], nbre_morts_moyenne, color="black")
    plt.show()

    print("Simulation terminée.")


#Fonction principale gérant le programme
def main():
    global power
    #Affichage du menu principal
    if(SIMULATION):
        menu_principal()
    #Initialisation des agents
    initialisation_population()
    #Boucle principale
    while power:
        actualisation()
        power = test_fin()
        if SIMULATION:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    power = False
            pygame.display.flip()
            clock.tick(60)
    

    #Fin: Affichage des graphiques
    if(AFFICHER_GRAPHIQUES):
        graphiques()

main()
