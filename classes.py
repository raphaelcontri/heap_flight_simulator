
class Empty :
    """ permet de gérer les cas de base de la classe Tas """

    def __init__(self) :
        pass

    def fusion(self, other) :
        if isinstance(self, Empty) :
            return other
        elif isinstance(other, empty) :
            return self

    def infixe(self) :
        return ""


    def minimum(self) :
        return None

    def appartient(self, x) :
        return False

    def appartient_indicatif(self, x) :
        return False

    def taille(self) :
        return 0

    def hauteur(self) :
        return 0

    def ajouter(self, avion) :
        return Tas(Empty(), avion, Empty())

    def estTas(self) :
        return True

    def estVide(self) :
        return

    def delete(self) :
        return Empty()



class Tas :
    """ certaines méthodes de cette classe ne peuvent être utilisées qu'avec des avions """
    def __init__(self, g, v, d) :
        self.gauche = g
        self.val = v
        self.droite = d



    
    def fusion(self, other) :
        if isinstance(self, Empty) :
            return other
        elif isinstance(other, Empty) :
            return self

        else :
        
            if self.val.priorite < other.val.priorite :
                return Tas(self.droite.fusion(other), self.val, self.gauche)

            else :
                return Tas(other.droite.fusion(self), other.val, other.gauche)


    def infixe(self) :
        return "(" + self.gauche.infixe() + str(self.val) + self.droite.infixe() + ")"

    def minimum(self) :
        return self.val

    def appartient(self, x) :
        if self.val == x :
            return True

        else :
            return self.gauche.appartient(x) or self.droite.appartient(x)

    def appartient_indicatif(self, x) :
        """ vérifier qu'un avion appartient à un tas, en ayant son indicatif comme entrée """
        if self.val.indicatif == x :
            return True
        else :
            return self.gauche.appartient_indicatif(x) or self.droite.appartient_indicatif(x)


    def taille(self) :
        return 1 + self.gauche.taille() + self.droite.taille()


    def hauteur(self) :
        return 1 + max(self.droite.hauteur(), self.gauche.hauteur())


    def ajouter(self, avion) :
        """ ici, avion est un objet avion """
        return self.fusion(Tas(Empty(), avion, Empty()))

    def supprimer(self) :
        return self.gauche.fusion(self.droite)

    def estTas(self) :
        if not isinstance(self.gauche, Empty) and not isinstance(self.droite, Empty) : 
            if self.droite.val.priorite < self.val.priorite or self.gauche.val.priorite < self.val.priorite :
                return False
            else :
                return self.droite.estTas() and self.gauche.estTas()

        if isinstance(self.gauche, Empty) and not isinstance(self.droite, Empty) :
            if self.droite.val.priorite < self.val.priorite :

                return False
            else :
                return self.droite.estTas()

        if not isinstance(self.gauche, Empty) and isinstance(self.droite, Empty) :
            if self.gauche.val.priorite < self.val.priorite :

                return False
            else :
                return self.gauche.estTas()

        if isinstance(self.gauche, Empty) and isinstance(self.droite, Empty) :
            return True


    def estVide(self) :
        return self.taille() == 0

    def delete(self, x) :
        """ permet de supprimer un avion dans la file à partir de son indicatif """
        if self.val.indicatif == x :
            return self.gauche.fusion(self.droite)

        else :
            return Tas(self.gauche.delete(x), self.val, self.droite.delete(x))


            







class Avion :
    def __init__(self, indicatif, autonomie, pirate, feu) :
        self.indicatif = indicatif
        self.autonomie = autonomie
        self.pirate = pirate
        self.feu = feu
        self.execution = False
        self.priorite = self.calcul_priorite()  # la priorité de l'avion es tcalculée directement à la création de l'avion
        assert isinstance(self.indicatif, str) and len(self.indicatif) == 6
        assert isinstance(self.autonomie, float) or isinstance(self.autonomie, int)
        assert isinstance(self.pirate, bool) and isinstance(self.feu, bool)


    def __repr__(self) :
        pirate = "piraté    " if self.pirate else str("non piraté")
        feu = "en feu    " if self.feu else str("pas en feu")
        res = "[" + str(self.indicatif) + " | " + str(round(self.autonomie, 3)) + "h | " + pirate + " | " + feu + " | " + str(round(self.priorite, 4)) + " ] "      
        return res


    def calcul_priorite(self) :
        """ renvoie un nombre représentant la priorité de l'avion dans la file d'attente"""

        # on part du temps de vol restant

        score = 100
        

        if self.feu is True :
            score -= 50

        if self.pirate is True :
            score -= 25


        if self.autonomie < 0.17 : # si il reste moins de 10 minutes de temps de vol (0.17 * 60 = 10,2 minutes)
            score -= 20

        else :
            score -= (20 - 3 * self.autonomie)

        return score
            

