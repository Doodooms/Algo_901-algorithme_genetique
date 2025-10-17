#from codage import Codage

from email.errors import NoBoundaryInMultipartDefect


class MantisseExposant:
    """
    Classe représentant un nombre en mantisse-exposant.
    Pour initialiser un objet de cette classe, on donne simplement un nombre réel.
    La mantisse et l'exposant sont calculés automatiquement.
    D'abord, sous forme decimale, puis convertis en binaire.
    """
    def __init__(self, reel : float, precision : int = 5):
        # Attributs definis a l'initialisation
        self.reel = reel # valeur du nombre reel
        self.precision = precision # nombre de chiffres significatifs dans la mantisse

        # Attributs non definis a l'initialisation
        self.mantisse = None # valeur de la mantisse sous forme decimale 
        self.exposant = None # valeur de l'exposant sous forme d'entier 
        
        self.mantisseBinaire = None # valeur de la mantisse en binaire (premier bit = signe)
        self.exposantBinaire = None # valeur de l'exposant en binaire (premier bit = signe)

    def decode(self):
        """
        Fonction qui prend en entrée un nombre réel et retourne sa représentation en mantisse-exposant.
        La mantisse et l'exposant sont représentés en binaire avec un bit de signe.
        """
        # Traiement du signe 
        signe_negatif = False
        if self.reel < 0:
            signe_negatif = True

        # Si la valeur absolue du reel est contenu entre 1 et 10 on ne passera pas dans les boucles
        self.mantisse = abs(self.reel)
        self.exposant = 0

        # Cas ou le nombre est superieur ou egal a 10 en valeur absolue
        while self.mantisse >= 10:
            self.mantisse /= 10
            self.exposant += 1

        # Cas ou le nombre est inferieur a 1 en valeur absolue
        while self.mantisse < 1 and self.mantisse != 0:
            self.mantisse *= 10
            self.exposant -= 1
    
        # On arrondi la mantisse a la precision donnee
        self.mantisse = round(self.mantisse, self.precision)

        # On gere le signe negatif
        if signe_negatif:
            self.mantisse = -self.mantisse
    
        return self.mantisse, self.exposant
    

    def decodeBinaire(self):
        """
        Fonction qui prend en un réel et utilise la méthode decode pour obtenir 
        une mantisse et un exposant et retourne leur valeur en binaire.
        """
        # On decode d'abord la mantisse et l'exposant en decimal
        self.mantisse, self.exposant = self.decode()

        # On convertit la mantisse en binaire
        # Gestion du bit de signe
        bit_de_signe_mantisse = '0' if self.mantisse >= 0 else '1'

        # On convertit la partie absolue de la mantisse en binaire  
        mantisse_absolue = abs(self.mantisse)

        # On convertir l'exposant en binaire
        # Gestion du bit de signe
        bit_de_signe_exposant = '0' if self.exposant >= 0 else '1'
        
        # On convertit la partie absolue de l'exposant en binaire
        exposant_absolu = abs(self.exposant)

        self.mantisseBinaire = self.mantisse

        return self.mantisseBinaire, self.exposantBinaire

    def __str__(self):
        """
        Affichage de la mantisse et de l'exposant sous forme décimale.
        """
        self.mantisse, self.exposant = self.decode() # on calcule la mantisse et l'exposant
        return f"{self.mantisse} x 10^{self.exposant}"
    
    def afficherBinaire(self):
        """
        Affichage de la mantisse et de l'exposant sous forme binaire.
        """
        self.mantisseBinaire, self.exposantBinaire = self.decodeBinaire() # on calcule la mantisse et l'exposant en binaire 
        print(f"{self.mantisseBinaire} x 10^{self.exposantBinaire}")

    
    
    @staticmethod
    def code(value: float) -> 'MantisseExposant':
        if value == 0:
            return MantisseExposant(0, 0)
        
        exposant = 0
        while abs(value) >= 10:
            value /= 10
            exposant += 1
        while abs(value) < 1:
            value *= 10
            exposant -= 1
        
        return MantisseExposant(value, exposant)
    

# Test de création 
ME = MantisseExposant(0.1234567)
ME.afficherBinaire()
