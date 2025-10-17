from Individu import individu

class population:
    def __init__(self, liste_individus : list[individu]):
        self.liste_individus = liste_individus

    def __str__(self):
        x = (", ".join(str(ind) for ind in self.liste_individus))
        return f"La population est composée des individus suivants : {x}"

    def ajouter(self, population : individu | list[individu]):
        if isinstance(population, list):
            self.liste_individus.extend(population)
        else:
            self.liste_individus.append(population)

    def retirer(self, population : individu | list[individu]):
        if isinstance(population, list):
            self.liste_individus = [x for x in self.liste_individus if x not in population]
        else:
            self.liste_individus.remove(population)

if __name__ == "__main__":
    import numpy as np
    from Coordonnees import coordonnees
    c1 = coordonnees(np.array([1,2]))
    c2 = coordonnees(np.array([3,4]))
    i1 = individu(1, c1)
    i2 = individu(2, c2)
    pop = population([i1, i2])
    print(pop)