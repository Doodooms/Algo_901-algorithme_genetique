from operators.Codage import Codage # Importer la classe abstraite Codage
from operators.Crossover import Crossover, SimpleCrossover # Importer SimpleCrossover pour l'exemple
from operators.Mutation import Mutation 
from operators.Selection import Selection, Selection_roulette, Selection_tournoi 
from core.Population import Population 
from core.Individu import Individu 
from operators.Performance import Performance # Importer Performance (ou la fonction de fitness directement si elle n'est pas encapsulée)
import numpy as np 
import random 

class AlgorithmeGenetique:
    """
    Classe principale de l'algorithme génétique
    """

    def __init__(
        self,
        population_size: int, # Ajout : taille de la population
        dimension: int, # Ajout : nombre de coordonnées par individu
        bounds: list[tuple[float, float]], # Ajout : [ (min_x1, max_x1), (min_x2, max_x2), ... ]
        codage_operator: Codage, # Remplacement de 'codage' par 'codage_operator' pour la clarté
        crossover_operator: Crossover, # Remplacement de 'crossover' par 'crossover_operator'
        mutation_operator: Mutation, # Remplacement de 'mutation' par 'mutation_operator'
        selection_operator_type: type(Selection), # Ajout : type de la classe de sélection (e.g., Selection_tournoi)
        fitness_function, # Ajout : la fonction de fitness
        maximize_fitness: bool = True, # Ajout : indique si on maximise ou minimise
        taux_mutation: float = 0.01, # Ajout : taux de mutation (peut être aussi dans mutation_operator)
        selection_params: dict = None, # Ajout : paramètres spécifiques pour la sélection (e.g., taille_tournoi)
        taux_crossover: float = 0.8, # Ajout : probabilité qu'un crossover ait lieu
        num_generations: int = 100 # Ajout : nombre de générations à exécuter
    ):
        # Paramètres de l'AG
        self.population_size = population_size
        self.dimension = dimension
        self.bounds = bounds # [[min, max], [min, max], ...] pour chaque dimension
        self.fitness_function = fitness_function
        self.maximize_fitness = maximize_fitness
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
        self.selection_operator_type = selection_operator_type
        self.selection_params = selection_params if selection_params is not None else {}
        self.selection_operator = None # Sera initialisé plus tard

        # Historique (pour le suivi de la convergence)
        self.history = {'best_fitness': [], 'avg_fitness': [], 'best_individu': []}
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
            self.codage_operator.code(coords_obj) # Le résultat est stocké dans coords_obj.coordonnees_codees
            
            individu = Individu(id=i, coordonnees=coords_obj)
            
            liste_individus.append(individu)
        
        self.population = Population(liste_individus)
        # Après avoir initialisé la population, initialiser l'opérateur de sélection
        self.selection_operator = self.selection_operator_type(self.population, **self.selection_params)
