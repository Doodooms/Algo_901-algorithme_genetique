import numpy as np

from core.Individu import individu


class Mutation:
    """
    Classe qui permet d'effectuer une mutation sur un individu selon un certain taux de mutation
    Marche uniquement sur un codage binaire !
    J'ai mis deux facon de voir je sais pas laquelle vous semble la plus logique
    """

    def __init__(self, taux_mutation: float):
        self.taux_mutation = taux_mutation

    def mutation1(self, individu: individu):
        """
        Fonction qui prend un individu et effectue des mutations sur ses coordonnées.
        On calcule d'abord le nombre de mutation, puis on modifie aléatoirement dans les coordonnées codées
        """
        coordonnees_mutees = (
            individu.coordonnees.coordonnees_codees
        )  # On l'initalise avec les coordonnées codées intiales
        nb_coordonnees = len(coordonnees_mutees)
        taille_codage = len(coordonnees_mutees[0])
        nb_cases = nb_coordonnees * taille_codage
        nb_mutation = int(np.floor(nb_cases * self.taux_mutation))
        cases_mutees = np.random.choice(nb_cases, nb_mutation, False)

        for case in cases_mutees:
            num_coord = case // taille_codage
            num_case = case % taille_codage
            coordonnees_mutees[num_coord][num_case] = (
                1 - coordonnees_mutees[num_coord][num_case]
            )
            # Je sais pas vraiment encore sous quelle forme est le codage, ligne du dessus peut être à modifier

    def mutation2(self, individu: individu):
        """
        Fonction qui prend un individu et effectue des mutations sur ses coordonnées.
        Pour chaque case, on a la probabilité taux_mutation d'effectuer une mutation
        """
        for coordonne in individu.coordonnees.coordonnees_codees:
            for i in range(len(coordonne)):
                if (
                    np.random.rand() <= self.taux_mutation
                ):  # On effectue la mutation avec la proba taux_mutation
                    coordonne[i] = 1 - coordonne[i]  # Pareil ici, peut être à modifier
