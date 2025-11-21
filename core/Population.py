from core.Individu import Individu

class Population:
    def __init__(self, liste_individus : list[Individu] = [Individu()]):
        self.liste_individus = liste_individus if isinstance(liste_individus, list) else [liste_individus]

    def __str__(self):
        if len(self.liste_individus) == 0:
            return "La population est vide."
        else:
            x = (",\n".join(str(ind) for ind in self.liste_individus))
            return f"La population est composée des individus suivants : \n{x}"

    def ajouter(self, population : Individu | list[Individu]):
        if isinstance(population, list):
            self.liste_individus.extend(population)
        else:
            self.liste_individus.append(population)

    def retirer(self, population : Individu | list[Individu]):
        if isinstance(population, list):
            self.liste_individus = [x for x in self.liste_individus if x not in population]
        else:
            self.liste_individus.remove(population)

if __name__ == "__main__":
    import numpy as np
    from core.Coordonnees import Coordonnees
    c1 = Coordonnees(np.array([1,2]))
    c2 = Coordonnees(np.array([3,4]))
    c2.coordonnees_codees = np.array([1, 0, 1, 0, 0, 1])
    i1 = Individu(1, c1)
    i2 = Individu(2, c2)
    pop = Population([i1])
    print(pop)
    pop.ajouter(i2)
    print(pop)
    pop.retirer(i1)
    c2.coordonnees_codees = np.array([0, 1, 0, 1, 1, 0])
    print(pop)
    pop.retirer(i2)
    print(pop)