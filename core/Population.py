from Individu import individu

class population:
    def __init__(self, liste_individus : list[individu]):
        self.liste_individus = liste_individus

    def __str__(self):
        return f"La population est composée des individus suivants : {self.liste_individus}"