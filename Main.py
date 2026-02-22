####  installer la librairie pynput et executer le fichier dans IDLE ###


from random import *
import copy # pour les deppcopy
import time
from pynput import keyboard # pour la gestion du clavier 

import sys # pour print des textes colorés dans le shell de IDLE
# cf : https://stackoverflow.com/questions/42472958/how-do-i-print-colored-text-in-idles-terminal
# pour colorer les textes dans IDLE


from classes import *
from fonctions import *



sys.stdout.shell.write("Appuyez environ 1 seconde sur la touche ctrl pour pouvoir interagir avec la file d'attente d'avions \n", "COMMENT")
print("entrez 'info' pour + d'informations")
sys.stdout.shell.write("pressez esc pour arrêter le programme\n\n", "BUILTIN")
file = Empty()
piste = Empty()

ctrl_pressed = False # c'est une variable globale





# gérer la pression de la touche ctrl avec la librairie pynput
def on_press(key): #fonction "obligatoire" de la librairie pynput


    # on utilise une variable globale car il est compliqué d'ajouter des paramètres dans l'apel de la fonction keyboard.Listener()
    global ctrl_pressed
    global continuer

    if key == keyboard.Key.ctrl:
        ctrl_pressed = True

    if key == keyboard.Key.esc :
        sys.stdout.shell.write("fermeture du programme", "BUILTIN")
        continuer = False


def on_release(key): #fonction "obligatoire" de la librairie pynput
    global ctrl_pressed
    if key == keyboard.Key.ctrl:
        ctrl_pressed = False





# permet de gérer les pressions de la touche ctrl tout en executant la simulation (et plus spécifiquement la fonction qui détourne et supprime aléatoirement des avions, qui doit être executée chaque seconde)



# les infos sur le fonctionnement de pynput sont ici :

# et plus spécifiquement cette partie du code, qui permet de surveiller la pression des touches du clavier et d'executer du code en même temps (comme supprimer de la file un avion qui a été détourné) 


""" https://pynput.readthedocs.io/en/latest/keyboard.html : 
# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
"""


listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()





cpt = 0 # utilisé uniquement pour savoir quand supprimer un avion de la piste d'atterrissage

continuer = True
while continuer :
    cpt += 1
    if cpt % 10 == 0 : #%10 pour ajouter un délai d'environ 10 secondes
        if piste.taille() > 0 : 
            piste = supprimer_piste(piste)
        
    time.sleep(1)
    file = supprimer_avion_pirate(file)

    if cpt % 3 == 0 : #%3 pour ajouter un délai d'environ 3 secondes
        file, piste = atterrissage_avions(file, piste)
    
    if ctrl_pressed == True :
        file, piste = interaction(file, piste)
    



























