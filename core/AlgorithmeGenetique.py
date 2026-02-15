from operators.Codage import CodageReel # Importer la classe abstraite Codage
from operators.Crossover import Crossover, SimpleCrossover # Importer SimpleCrossover pour l'exemple
from operators.Mutation import Mutation 
from operators.Selection import Selection, Selection_roulette, Selection_tournoi, Selection_naturelle
from operators.MantisseExposant import MantisseExposant
from core.Population import Population 
from core.Individu import Individu
from core.Coordonnees import Coordonnees
from operators.Performance import Performance # Importer Performance (ou la fonction de fitness directement si elle n'est pas encapsulée)
import numpy as np 
import random 
from math import sin, sqrt

class AlgorithmeGenetique:
    """
    Classe principale de l'algorithme génétique
    """

    def __init__(
        self,
        population_size: int, # taille de la population
        dimension: int, # nombre de coordonnées par individu
        bounds: list[tuple[float, float]], # [ (min_x1, max_x1), (min_x2, max_x2), ... ]
        codage_operator : MantisseExposant,
        crossover_operator: Crossover,
        mutation_operator: Mutation,
        selection_operator : Selection, #  type de la classe de sélection (e.g., Selection_tournoi)
        fitness_function : Performance, #  la fonction de fitness pour évaluer les individus
        taux_mutation: float = 0.01, #  taux de mutation (peut être aussi dans mutation_operator)
        selection_params: dict = {}, #  paramètres spécifiques pour la sélection (e.g., taille_tournoi)
        taux_crossover: float = 0.8, #  probabilité qu'un crossover ait lieu
        num_generations: int = 100 #  nombre de générations à exécuter
    ):
        # Paramètres de l'AG
        self.population_size = population_size
        self.dimension = dimension
        self.bounds = bounds # [[min, max], [min, max], ...] pour chaque dimension
        self.fitness_function = fitness_function
        self.evaluateur = Performance(self.fitness_function)
        self.taux_mutation = taux_mutation # Peut être utilisé pour initialiser l'opérateur de mutation
        self.taux_crossover = taux_crossover
        self.num_generations = num_generations

        # Opérateurs
        self.codage_operator = codage_operator
        self.crossover_operator = crossover_operator
        self.mutation_operator = mutation_operator
        
        # Initialisation de la population (sera fait dans _initialiser_population)
        self.population = Population([]) 
        
        # Initialisation de l'opérateur de sélection (nécessite la population après initialisation)
        self.selection_operator = selection_operator
        self.selection_params = selection_params if selection_params is not None else {}
        

        # Historique (pour le suivi de la convergence)
        self.history = {'best_fitness': [], 'best_individu': []}
        self.best_fitness = None
        self.best_overall_individu = None


    def _initialiser_population(self):
        """
        Génère une population initiale aléatoire d'individus.
        """
        liste_individus = []
        for i in range(self.population_size):
            # Générer des coordonnées réelles aléatoires dans les bornes
            coordonnees_reelles = np.array([
                random.uniform(self.bounds[j][0], self.bounds[j][1])
                for j in range(self.dimension)
            ])
            
            coords_obj = Coordonnees(coordonnees_reelles)
            # Appliquer le codage défini
            self.codage_operator.code(coords_obj)
            
            individu = Individu(id=i, coordonnees=coords_obj)
            liste_individus.append(individu)
        
        self.population = Population(liste_individus)
        self.selection_operator.population = self.population

    def _evaluer_population(self):
        """
        Évalue la performance (fitness) de chaque individu dans la population.
        """
        for individu in self.population.liste_individus:
            # On utilise la classe Performance pour évaluer l'individu
            individu.fitness = self.evaluateur.evaluer(individu)

            if individu.fitness is None:
                raise ValueError(f"Fitness None pour l'individu {individu.id}. Vérifie Performance.evaluer().")
            
            # Mettre à jour le meilleur fitness et le meilleur individu
            if self.best_fitness is None or individu.fitness > self.best_fitness:
                self.best_fitness = individu.fitness
                self.best_overall_individu = individu
                self.history["best_fitness"].append(self.best_fitness)
                self.history["best_individu"].append(self.best_overall_individu)


    def _selectionner_parents(self) -> list[Individu]:
        """
        Sélectionne les parents pour la reproduction en utilisant l'opérateur de sélection.
        Retourne une liste d'individus sélectionnés.
        """
        # Mise à jour de l'opérateur de sélection avec la population actuelle
        self.selection_operator.population = self.population
        selected_parents = list(self.selection_operator.selection())
    
        return selected_parents


    def _reproduire(self, parents: list[Individu]) -> list[Individu]:
        """
        Effectue le crossover et la mutation sur les parents pour créer une nouvelle génération.
        """
        nouvelle_generation = []
        # il faut un nombre pair de parents pour le crossover par paires
        random.shuffle(parents) # Mélanger les parents pour des paires aléatoires
        
        for i in range(0, len(parents) - 1, 2):
            parent1 = parents[i]
            parent2 = parents[i+1]

            enfant1, enfant2 = parent1, parent2 # Initialisation par défaut, si pas de crossover

            # Décider si le crossover a lieu
            if random.random() < self.taux_crossover:
                enfant1, enfant2 = self.crossover_operator.crossover(parent1, parent2)
                
            # Appliquer la mutation aux enfants (même s'ils sont identiques aux parents si pas de crossover)
            self.mutation_operator.mutation(enfant1) # La mutation doit modifier individu.coordonnees.coordonnees_codees
            self.mutation_operator.mutation(enfant2)
            
            nouvelle_generation.append(enfant1)
            nouvelle_generation.append(enfant2)
            
        # S'assurer que la nouvelle génération a la bonne taille
        # Cela peut impliquer de retirer les excédents ou d'ajouter des parents directement si la population_size est impaire
        if len(nouvelle_generation) > self.population_size:
            nouvelle_generation = random.sample(nouvelle_generation, self.population_size)
        elif len(nouvelle_generation) < self.population_size:
            remaining_needed = self.population_size - len(nouvelle_generation)
            if remaining_needed > 0 and len(parents) >= remaining_needed:
                nouvelle_generation.extend(random.sample(parents, remaining_needed))
            elif remaining_needed > 0: # Si pas assez de parents non plus
                print("Avertissement: Nouvelle génération plus petite que la population cible.")


        return nouvelle_generation


    def _remplacer_population(self, nouvelle_generation: list[Individu]):
        """
        Remplace l'ancienne population par la nouvelle génération.
        """
        self.population.liste_individus.sort(key=lambda ind: ind.fitness)
        self.population = Population(nouvelle_generation)
    
if __name__ == "__main__":
    # Exemple d'utilisation de la classe AlgorithmeGenetique
    def exemple_fitness_function(coordonnees: np.ndarray) -> float:
        return -np.sum(coordonnees**2) + 10
    
    def exemple_fitness_function2(coordonnees : np.ndarray) -> float:
        return -(-coordonnees[0]*sin(sqrt(abs(coordonnees[0]))) - coordonnees[1]*sin(sqrt(abs(coordonnees[1]))))
    # (-x * sin(sqrt(abs( x )))) + (-y * sin(sqrt(abs( y ))))

    # Initialiser les opérateurs
    codage = MantisseExposant()
    crossover = SimpleCrossover(codage)
    mutation = Mutation(0.05, codage)

    tournoi = Selection_tournoi(
        None, taille_tournoi=3, taille_selection=10
    )  # Population sera définie plus tard

    # Créer une instance de l'algorithme génétique
    ag = AlgorithmeGenetique(
        population_size=500,
        dimension=2,
        bounds=[(-500, 500), (-500, 500)],
        codage_operator=codage,
        crossover_operator=crossover,
        mutation_operator=mutation,
        selection_operator=tournoi,
        fitness_function=exemple_fitness_function,
        taux_mutation=0.05,
        num_generations=100,
    )

    # Initialiser la population
    ag._initialiser_population()
    ag._evaluer_population()
    for t in range(
        ag.num_generations
    ):  # On fait évoluer la  population sur num_generations
        parents = ag._selectionner_parents()
        nouvelle_generation = ag._reproduire(parents)
        ag._remplacer_population(nouvelle_generation)
        ag._evaluer_population()
    print(ag.history)
    
    # On vérifie la convergence 
    print(f"Le résultat attendu est 10 et le résultat de l'algo est : {ag.history['best_fitness'][-1]}")