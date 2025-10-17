import numpy as np

from core.Individu import individu
from core.Coordonnees import coordonnees


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
        taille_codage = len(
            coordonnees_mutees[0]
        )  # !! mantisse et exposant pas même taille de codage à modifier
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
                    print(f"Mutation en {i}!")
                    coordonne[i] = 1 - coordonne[i]  # Pareil ici, peut être à modifier


if __name__ == "__main__":
    c1 = coordonnees(np.array([1, 2]))
    c2 = coordonnees(np.array([3, 4]))
    c1.coordonnees_codees = np.array([[0, 0, 0, 0]])
    c2.coordonnees_codees = np.array([[1, 1, 1, 1]])
    parent1 = individu(1, c1)
    parent2 = individu(2, c2)
    mutation = Mutation(0.5)
    mutation.mutation2(parent1)
    print(parent1.coordonnees.coordonnees_codees)
