class Performance:
    from core.Individu import Individu
    def __init__(self, fitness_function):
        self.score = None
        self.fitness_function = fitness_function

    def __str__(self):
        return f"Son score de performance est : {self.score}"

    def evaluer(self, individu : Individu) -> None:
        """
        Évalue un individu en utilisant la fonction de fitness fournie
        et met à jour son score de performance."""
        self.score = self.fitness_function(individu.coordonnees.coordonnees)