from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np

from core.Individu import individu
from core.Coordonnees import coordonnees


class Crossover(ABC):
    """
    Classe abstraite de crossover
    """

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def crossover(parent1: individu, parent2: individu) -> Tuple[individu, individu]:
        """
        Fonction qui prends 2 individus (les parents) et effectue le crossover pour obtenir
        deux nouveaux individus (les enfants).
        En supposant que les coordonnées des parents sont déjà encodées.
        On obtient alors des individus avec seulement des encoded_coordonnees pour l'instant
        Le résultat est un tuple de deux individus, (enfant1,enfant2)
        """


class SimpleCrossover(Crossover):
    """
    Crossover le plus simple qui coupe en deux l'ADN  de manière aléatoire
    en mettant première partie un morceau de l'ADN du parent1 et en deuxième partie l'ADN
    du parent2 pour l'enfant 1 et l'inverse pour l'enfant2
    """

    @staticmethod
    def crossover(parent1: individu, parent2: individu) -> Tuple[individu, individu]:
        """
        Tous les coordonnées codées sont de même longueur
        """
        encoded_parent1 = parent1.coordonnees.coordonnees_codees
        encoded_parent2 = parent2.coordonnees.coordonnees_codees

        nb_coordonnees = len(encoded_parent1)
        taille_codage = len(encoded_parent1[0])

        c1 = coordonnees(np.array([]))
        c1.coordonnees_codees = []
        c2 = coordonnees(np.array([]))
        c2.coordonnees_codees = []

        for num_coordonnee in range(nb_coordonnees):
            separateur = np.random.randint(
                1, taille_codage
            )  # Pour chaque coordonnées on choisit un séparateur pour split le codage des deux parents
            encoded_coord1 = np.concatenate(
                (
                    encoded_parent1[num_coordonnee][:separateur],
                    encoded_parent2[num_coordonnee][separateur:],
                )
            )
            encoded_coord2 = np.concatenate(
                (
                    encoded_parent2[num_coordonnee][:separateur],
                    encoded_parent1[num_coordonnee][separateur:],
                )
            )
            c1.coordonnees_codees.append(encoded_coord1)
            c2.coordonnees_codees.append(encoded_coord2)

        c1.coordonnees_codees = np.array(c1.coordonnees_codees)
        c2.coordonnees_codees = np.array(c2.coordonnees_codees)
        enfant1 = individu(1, c1)
        enfant2 = individu(2, c2)
        # Pour l'instant les enfants n'ont que des coordonnees_codees,
        # on les decodera s'ils sont selectionnés après pour rejoindre la population ou on pourrait le faire maintenant comme vous voulez
        return enfant1, enfant2


if __name__ == "__main__":
    c1 = coordonnees(np.array([1, 2]))
    c2 = coordonnees(np.array([3, 4]))
    c1.coordonnees_codees = np.array([[0, 0, 0, 0]])
    c2.coordonnees_codees = np.array([[1, 1, 1, 1]])
    parent1 = individu(1, c1)
    parent2 = individu(2, c2)
    enfant1, enfant2 = SimpleCrossover.crossover(parent1, parent2)
    print(f"Enfant1 : {enfant1.coordonnees.coordonnees_codees}")
    print(f"Enfant2{enfant2.coordonnees.coordonnees_codees}")
