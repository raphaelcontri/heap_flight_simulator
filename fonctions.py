#################################
from random import *
from classes import *
from pynput import keyboard # pour la gestion du clavier
import copy
import sys

# création de fonctions pour générer une file de n avions aléatoires

 
def genereListeAvions(n) :
    assert n >= 0
    """ génère une liste d'avions aléatoirs de taille n
    input : un naturel
    output : une liste do'bjets avions"""
    caracteres = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn1234567890"
    res = []
    for i in range(n) :
        indicatif = ""

        # on ne gère pas les doublons (ils sont par contre gérés lors de l'ajout manuel)
        # mais il y a 62**6 = 56.8 milliards de noms d'avions différents possibles
        for j in range(6) :
            indicatif += caracteres[randint(0, len(caracteres)-1)]

        pi = randint(0, 10)
        
        if pi >= 7 :
            pirate = True
        else :
            pirate = False

        fe = randint(0, 10)
        if fe >= 6 :
            feu = True
        else :
            feu = False
        tmp = Avion(indicatif, uniform(0, 2), pirate, feu)

        res.append(tmp)

    return res
    


def genereFilePriorite(liste) :
    """ génère une file de priorité à partir d'une liste d'avions
    input : une liste d'objets avions
    output : une file (tas min) d'objets avions"""
    assert isinstance(liste, list) 
    
    File = Empty()
    for f in liste :
        File = File.ajouter(f)

    assert isinstance(File, Tas) or isinstance(File, Empty)

    return File
    
def generefile(n) :
    """ génère une file de n avions aléatoires en utilisant les deux fonctions définies ci-dessus """
    res = genereFilePriorite(genereListeAvions(n))
    assert res.estTas()
    return res

#################################

















#################################





def affichage(file, p = False) : # p indique si la file est la file d'attente des avions ou la piste d'atterissage (utile uniquement pour l'affichage dans le shell
    """ affiche les avions en fonction de leur priorité
        l'idée est ici  de créer unen copie de la file et de print puis supprimer successivement l'élement minimal de la file
        input : une file d'attente d'avions
        output : rien"""
    tmp = copy.deepcopy(file)

    if file.taille() != 0 : 
        print("\n \n ⭡ les avions les plus prioritaires ⭡ \n")
        while tmp.taille() > 1 :
            sys.stdout.shell.write(str(tmp.val) + "\n", "KEYWORD")
            tmp = tmp.supprimer()
        if file.taille() != 0 : 
            sys.stdout.shell.write(str(tmp.val) + "\n", "KEYWORD")

        print()

    if p :
        if file.taille() == 0 :
            print("\nil n'y a aucun avion sur la piste\n")
    else : 
        if file.taille() == 0 :
            print("\nil n'y a aucun avion dans la file d'attente ! \n")

#################################










def ajouter_avion(file) :
    ''' demande à l'utilisateur les informations cocnernant l'avion à ajouter puis ajoute l'avion à la file d'attente
    input et output : file'''
    indicatif = ""
    while len(indicatif) != 6 or file.appartient_indicatif(indicatif) : 
        indicatif = input('entrez l\'indicatif 6 caractères de l\'avion ')
        if file.appartient_indicatif(indicatif) : #permet d'interdire à l'utilisateur d'ajouter deux avions avec le même indicatif
            print("l'avion existe déjà !! ")
    tps = "a"
    while not isinstance(tps, float):
        tps = input('entrez le temps restant que l\'avion peut encore voler (entrez uniquement un flottant !!) ')
        tps = eval(tps)
    pirate = None
    while not isinstance(pirate, bool) : 
        pirate = input("Y a-t-il un pirate a bord ? O/n ")
        if pirate == "O" :
            pirate = True
        elif pirate == "n" :
            pirate = False

    feu = None
    while not isinstance(feu, bool) : 
        feu = input("Y a-t-il un incendie a bord ? O/n ")
        if feu == "O" :
            feu = True
        elif feu == "n" :
            feu = False

    avion = Avion(indicatif, tps, pirate, feu)
    file = file.ajouter(avion)
    assert file.estTas()
    return file





def supprimer_avion_pirate(file) :
    """ Fonction appelée toutes les secondes.
    Elle parcourt le tas, et pour chaque avion piraté, elle choisit au hasard si cet avion sera détourné
    l'enjeu de ce programme est de supprimer un avion qui se situe sur des noeuds intermédiaires

    l'idée est donc de parcourir la file jusqu'à tomber sur l'avion a supprimer, puis de fusionner les deux fils de l'avion à supprimer
    inout : file d'attente d'avions
    output : la file d'attente d'avions"""


    if isinstance(file, Empty) : #cas de base 
        return Empty()
    
    assert isinstance(file.val.pirate, bool)
    if file.val.pirate :

        r = randint(1, 25) #chaque seconde, un avion piraté à un risque sur 25 d'être détourné


        if r == 1 : #l'avion piraté sera détourné
            
            sys.stdout.shell.write("ATTENTION !! L'avion " + str(file.val) + " a été détourné, il est maintenant supprimé de la file d'attente !! \n" , "COMMENT")
            print() # pour sauter une ligne 
            return supprimer_avion_pirate(file.gauche.fusion(file.droite)) #supprime l'avion détourné. Le programme continue : plusieurs avions sur le même chemin de l'arbre peuvent être supprimés avec un seul appel de la fonction

        else :

            # ces 4 cas permettent de gérer les cas ou les sous arbres sont vides
            if not isinstance(file.gauche, Empty) and not isinstance(file.droite, Empty) :
                return Tas(supprimer_avion_pirate(file.gauche), file.val, supprimer_avion_pirate(file.droite))

            if not isinstance(file.gauche, Empty) and  isinstance(file.droite, Empty) :
                return Tas(supprimer_avion_pirate(file.gauche), file.val, Empty())

            if  isinstance(file.gauche, Empty) and not isinstance(file.droite, Empty) : 
                return Tas(Empty(), file.val, supprimer_avion_pirate(file.droite))

            if  isinstance(file.gauche, Empty) and  isinstance(file.droite, Empty) : 
                return Tas(Empty(), file.val, Empty())
            
    else :
        if not isinstance(file.gauche, Empty) and not isinstance(file.droite, Empty) :
            return Tas(supprimer_avion_pirate(file.gauche), file.val, supprimer_avion_pirate(file.droite))

        if not isinstance(file.gauche, Empty) and  isinstance(file.droite, Empty) :
            return Tas(supprimer_avion_pirate(file.gauche), file.val, Empty())

        if  isinstance(file.gauche, Empty) and not isinstance(file.droite, Empty) : 
            return Tas(Empty(), file.val, supprimer_avion_pirate(file.droite))

        if  isinstance(file.gauche, Empty) and  isinstance(file.droite, Empty) : 
            return Tas(Empty(), file.val, Empty())




def atterrissage_avions(file, piste) :
    """ permet de gérer l'atterrissage des avions en les supprimant de la file d'attente uniquement si il y a de la place sur la piste d'atterrissage
    input et output : file d'attente d'avions et piste"""
    if file.taille() != 0 :
    # permet de gérer la piste. Si la piste est déjà remplie, aucun avion ne pourra atterrir et il faudra attendre environ 1 minute
        if piste.taille() < 3 :
            piste = piste.ajouter(file.val)
            tmp = file.val
            file = file.supprimer()
            sys.stdout.shell.write(str("\nl'avion " +  str(tmp) +  " a atteri sur la piste de l'aéroport \n"), "STRING")
            print("il reste ", 3 - piste.taille(), " place(s) sur la piste d'atterrissage")
            if piste.taille() == 3 :
                sys.stdout.shell.write("Vous devez attendre qu'un avion parte de la piste d'atterrissage pour que le suivant puisse atterrir ! \n \n", "KEYWORD")

    

    return file, piste








def interaction(file, piste) :
    """ fonction appelée uniquement en cas de pression de la touche ctrl. la finction demande l'action a effectuer
    input et output : file d'attente d'avions et piste"""
    reponses = ["q", "a", "l", "g", "r", "info", "p", "t"]
    a = input('\nq pour quitter, a pour ajouter un avion, l pour lister les avions, g pour générer une file de n avions aléatoires, p pour afficher la piste, t pour consulter les tailles des deux files ')
    while not a in reponses :
        print()
        a = input('q pour quitter, a pour ajouter un avion, l pour lister les avions, g pour générer une file de n avions aléatoires, p pour afficher la piste, t pour consulter les tailles des deux files ')


    if a == "a" :
        file = ajouter_avion(file)

    if a == "l" :
        affichage(file)


    if a == "p" :
        affichage(piste, p = True)
        

    if a == "g" :
        n = "a"
        n = eval(n)
        while not isinstance(n, int) :
            n = str(input("\nentrez le nombre d'avions voulu dans la file  "))
            n = eval(n)
        file = generefile(n)

        print("\n voici la file d'origine :")
        affichage(file)



    if a == "info" :
        f = open("regles_du_jeu.txt", "r")
        print()
        txt = f.read()
        print(txt)

    if a == "t" :
        print()
        b = str(input("1 pour afficher la taille de la file d'attente des avions, 2 pour consulter le nombre d'avions sur la piste"))
        if b == "1" :
            print()
            print(file.taille())
            print()
        elif b == "2" :
            print()
            print(piste.taille())
            print()
        else :
            print(" sélectionnez 1 ou 2 !! ")

    return file, piste










def supprimer_piste(piste) :
    """ permet de supprimer un avion de la piste
    input et output : piste"""
    taille_avant = piste.taille()
    tmp = piste.val
    piste = piste.supprimer()
    sys.stdout.shell.write(str("\nl'avion " +  str(tmp) +  " a été libéré de la piste, il reste " +  str(3 - piste.taille()) + " place(s) sur la piste\n"), "BUILTIN")
    print()
    if piste.taille() > 0 :
        assert piste.taille() == taille_avant - 1
    return piste



