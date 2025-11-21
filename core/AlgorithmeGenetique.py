from operators.Codage import Codage # Importer la classe abstraite Codage
from operators.Crossover import Crossover, SimpleCrossover # Importer SimpleCrossover pour l'exemple
from operators.Mutation import Mutation 
from operators.Selection import Selection, Selection_roulette, Selection_tournoi 
from operators.MantisseExposant import MantisseExposant
from core.Population import Population 
from core.Individu import Individu
from core.Coordonnees import Coordonnees
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
        codage_operator : MantisseExposant, # Remplacement de 'codage' par 'codage_operator' pour la clarté
        crossover_operator: Crossover, # Remplacement de 'crossover' par 'crossover_operator'
        mutation_operator: Mutation, # Remplacement de 'mutation' par 'mutation_operator'
        selection_operator_type: Selection, # Ajout : type de la classe de sélection (e.g., Selection_tournoi)
        fitness_function, # Ajout : la fonction de fitness
        maximize_fitness: bool = True, # Ajout : indique si on maximise ou minimise
        taux_mutation: float = 0.01, # Ajout : taux de mutation (peut être aussi dans mutation_operator)
        selection_params: dict = {}, # Ajout : paramètres spécifiques pour la sélection (e.g., taille_tournoi)
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
        self.selection_params = selection_params if selection_params is not None else None
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
            coords_obj.coordonnees_codees=map(lambda x: self.codage_operator.codeBinaire(x), coords_obj.coordonnees)
            coords_obj.coordonnees_codees = list(coords_obj.coordonnees_codees)

            self.codage_operator # Le résultat est stocké dans coords_obj.coordonnees_codees
            
            individu = Individu(id=i, coordonnees=coords_obj)
            individu.coordonnees.coordonnees_codees = coords_obj.coordonnees_codees
            
            liste_individus.append(individu)
        
        self.population = Population(liste_individus)

        # Evaluation de la population
        self._evaluer_population()
        
        # Après avoir initialisé la population, initialiser l'opérateur de sélection
        self.selection_operator = self.selection_operator_type
        self.selection_operator.population = self.population

    def _evaluer_population(self):
        """
        Évalue la performance (fitness) de chaque individu dans la population.
        """
        for individu in self.population.liste_individus:
            # individu avec ses coordonnées réelles décodées
            # (Si le codage est binaire, vbesoin d'une étape de décodage ici)
            
            # On utilise la classe Performance pour évaluer l'individu
            perf = Performance(self.fitness_function)
            individu.fitness = perf.evaluer(individu) # Ajouter un attribut fitness à l'individu

            # Ajuster le score si on minimise (les opérateurs de sélection tendent à maximiser)
            if not self.maximize_fitness:
                individu.fitness *= -1 # Transformer la minimisation en maximisation


    def _selectionner_parents(self, num_parents_needed = None) -> list[Individu]:
        """
        Sélectionne les parents pour la reproduction en utilisant l'opérateur de sélection.
        Retourne une liste d'individus sélectionnés.
        """
        
        # La sélection doit retourner un nombre de parents suffisant pour la reproduction
        # Par exemple, pour générer une nouvelle population de self.population_size individus,
        # il faudra self.population_size / 2 paires de parents.
        # Ici on simplifie et sélectionne un ensemble, l'opérateur de sélection
        # devra s'assurer de la taille.
        # la méthode selection() des classes de sélection retourne un `set`.
        # Il faut convertir en liste et s'assurer qu'il y a assez de parents pour les crossovers.
        
        # Initialisation par défault du nombre de parent (pour obtenir une population de même taille après le crossover)
        if num_parents_needed == None:
            num_parents_needed = np.floor(self.population_size/2) 
        
        # Vérification que le nombre de parents est paire
        if num_parents_needed%2 == 1:
            if num_parents_needed != 1:
                num_parents_needed -= 1
            else:
                num_parents_needed += 1
        
        # Il faudra probablement modifier l'interface de Selection pour qu'elle prenne 'self.population'
        # comme argument ou soit mise à jour avec la dernière population.
        
        
        # self.selection_params contient la bonne 'taille_selection'
        # pour obtenir le nombre de parents souhaité.
        
        if self.selection_params is not None:
            selected_parents = list(self.selection_operator.selection(num_parents_needed, self.selection_params)) 
        else:
            selected_parents = list(self.selection_operator.selection(num_parents_needed))
        
        # Si le nombre de parents sélectionnés est inférieur à ce dont nous avons besoin pour la prochaine génération,
        # il faut soit rappeler la sélection, soit adapter la stratégie de reproduction.
    
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
                # Le crossover_operator doit être adapté pour travailler avec les objets Individu
                # et créer de nouveaux objets Individu pour les enfants.
                enfant1_coords_obj = Coordonnees(np.array([])) # Coordonnées réelles vide pour l'instant
                enfant2_coords_obj = Coordonnees(np.array([]))
                
                # Le crossover opère sur les coordonnées encodées
                # et devrait retourner les nouvelles coordonnées encodées des enfants
                # Il faudra modifier SimpleCrossover.
                # Temporairement, on simule le retour d'enfants basés sur les parents
                # C'est ici que l'implémentation de Crossover doit être appelée.
                # Par exemple : enfant1_encoded, enfant2_encoded = self.crossover_operator.crossover(parent1, parent2)
                # puis créer de nouveaux objets Coordonnees et Individu
                
                # Pour l'exemple, supposons que crossover_operator retourne des individus complets
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
            # Stratégie à définir : ajouter des individus aléatoires, ou des parents élites
            # Pour l'instant, on peut compléter avec des parents si le nombre d'enfants est insuffisant
            remaining_needed = self.population_size - len(nouvelle_generation)
            if remaining_needed > 0 and len(parents) >= remaining_needed:
                nouvelle_generation.extend(random.sample(parents, remaining_needed))
            elif remaining_needed > 0: # Si pas assez de parents non plus
                print("Avertissement: Nouvelle génération plus petite que la population cible.")


        return nouvelle_generation


    def _remplacer_population(self, nouvelle_generation: list[Individu]):
        """
        Remplace l'ancienne population par la nouvelle génération.
        Implémente ici la stratégie de remplacement (e.g., Elitisme + nouvelle_generation).
        """
        # Stratégie d'élitisme : garder les meilleurs individus de l'ancienne population
        # et les ajouter à la nouvelle génération avant de la tronquer si nécessaire.
        
        # On suppose que les individus ont déjà leur fitness calculée.
        self.population.liste_individus.sort(key=lambda ind: ind.fitness, reverse=self.maximize_fitness)
        
        # Garder le meilleur individu (l'élite)
        elite_individu = self.population.liste_individus[0]
        
        # Créer la nouvelle population en combinant l'élite et la nouvelle génération
        #  si l'élite est déjà dans la nouvelle_generation, il ne faut pas le dupliquer.
        # on remplace juste la population par la nouvelle génération.
        
        # Pour l'instant, on remplace simplement
        self.population = Population(nouvelle_generation)
        
        # il faut que l'élite soit dans la nouvelle population s'il y a de l'élitisme.
        # Par exemple:
        # if elite_individu not in self.population.liste_individus:
        #    self.population.retirer(self.population.liste_individus[-1]) # retirer le pire si nouvelle_generation est pleine
        #    self.population.ajouter(elite_individu)
    
if __name__ == "__main__":
    # Exemple d'utilisation de la classe AlgorithmeGenetique
    def exemple_fitness_function(coordonnees: np.ndarray) -> float:
        return -np.sum(coordonnees**2) + 10

    # Initialiser les opérateurs (exemples simples)
    #codage = Codage() # Remplacer par une implémentation concrète
    crossover = SimpleCrossover()
    mutation = Mutation(0.05) # Remplacer par une implémentation concrète
    codage = MantisseExposant()
    tournoi = Selection_tournoi(Population()) # Population sera définie plus tard
    tournoi_params = 5

    # Créer une instance de l'algorithme génétique
    ag = AlgorithmeGenetique(
        population_size=50,
        dimension=2,
        bounds=[(-5, 5), (-5, 5)],
        codage_operator=codage,
        crossover_operator=crossover,
        mutation_operator=mutation,
        selection_operator_type=tournoi,
        fitness_function=exemple_fitness_function,
        maximize_fitness=True,
        taux_mutation=0.05,
        selection_params=tournoi_params,
        taux_crossover=0.7,
        num_generations=100
    )

    # Initialiser la population
    ag._initialiser_population()
    print(ag.population)
    ag._selectionner_parents()
    ag._reproduire()
    ag._