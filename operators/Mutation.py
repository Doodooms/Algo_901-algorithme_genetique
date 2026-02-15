import numpy as np

from core.Individu import Individu
from core.Coordonnees import Coordonnees
from operators.Codage import Codage


class Mutation:
    """
    Classe qui permet d'effectuer une mutation sur un individu selon un certain taux de mutation
    Marche uniquement sur un codage binaire !
    """

    def __init__(self, taux_mutation: float, codage: Codage):
        self.taux_mutation = taux_mutation
        self.codage = codage

    def mutation(self, individu: Individu):
        """
        Fonction qui prend un individu et effectue des mutations sur ses coordonnées.
        Pour chaque case, on a la probabilité taux_mutation d'effectuer une mutation
        """
        for indice, coordonne in enumerate(individu.coordonnees.coordonnees_codees):
            mutation = False
            for i in range(len(coordonne)):
                if (
                    np.random.rand() <= self.taux_mutation
                ):  # On effectue la mutation avec la proba taux_mutation
                    coordonne[i] = 1 - coordonne[i]
                    mutation = True
            if (
                mutation
            ):  # S'il il y a eu une mutation il faut recalculer les coordonnées non codées
                individu.coordonnees.coordonnees[indice] = self.codage.decode(coordonne)


if __name__ == "__main__":
    from operators.MantisseExposant import MantisseExposant

    c1 = Coordonnees(np.array([1, 2]))
    c2 = Coordonnees(np.array([3, 4]))
    c1.coordonnees_codees = np.array([[0, 0, 0, 0]])
    c2.coordonnees_codees = np.array([[1, 1, 1, 1]])
    parent1 = Individu(1, c1)
    parent2 = Individu(2, c2)
    codage = MantisseExposant()
    mutation = Mutation(0.5, codage)
    mutation.mutation(parent1)
    print(parent1.coordonnees.coordonnees_codees)
