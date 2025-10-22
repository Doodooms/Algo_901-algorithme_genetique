from Codage import Codage

def entier_en_binaire(n):
    """
    Fonction qui convertit un entier en binaire avec un bit de signe.
    Le premier bit indique le signe (0 pour positif, 1 pour négatif).
    Les bits suivants représentent la valeur absolue de l'entier en binaire.
    """
    if n == 0:
        return '0'  # Representation binaire de 0

    bit_de_signe = '0' if n >= 0 else '1'
    valeur_absolue = abs(n)
    bits_valeur = bin(valeur_absolue)[2:]  # Conversion en binaire sans le préfixe '0b'

    return bit_de_signe + bits_valeur

def binaire_en_entier(binaire):
    """
    Fonction qui convertit une représentation binaire avec un bit de signe en entier.
    Le premier bit indique le signe (0 pour positif, 1 pour négatif).
    Les bits suivants représentent la valeur absolue de l'entier en binaire.
    """
    if len(binaire) == 0:
        raise ValueError("La chaîne binaire ne peut pas être vide.")

    bit_de_signe = binaire[0]
    bits_valeur = ''.join(binaire[1:])

    valeur_absolue = int(bits_valeur, 2) if bits_valeur else 0

    if bit_de_signe == '0':
        return valeur_absolue
    else:
        return -valeur_absolue


# Creation de la classe MantisseExposant

class MantisseExposant(Codage):
    """
    Classe représentant un nombre en mantisse-exposant - hérite de la classe Codage.
    """
    def __init__(self):
        # Attributs definis a l'initialisation
        self.reel = 0 # valeur du nombre reel
        self.precision = 5 # nombre de chiffres significatifs dans la mantisse

        # Attributs non definis a l'initialisation
        self.mantisse = None # valeur de la mantisse sous forme decimale 
        self.exposant = None # valeur de l'exposant sous forme d'entier 
        
        self.mantisseBinaire = None # valeur de la mantisse en binaire (premier bit = signe)
        self.exposantBinaire = None # valeur de l'exposant en binaire (premier bit = signe)

    def code(self, reel):
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

    def codeBinaire(self, reel):
        """
        Fonction qui prend en un réel et utilise la méthode decode pour obtenir 
        une mantisse et un exposant et retourne leur valeur en binaire.
        """
        # Initialisation de la valeur du reel
        self.reel = reel

        # On decode d'abord la mantisse et l'exposant en decimal
        self.mantisse, self.exposant = self.code(self.reel)

        # On convertit la mantisse en binaire
        self.mantisseBinaire = entier_en_binaire(int(self.mantisse * (10 ** self.precision)))

        # On convertit l'exposant en binaire
        # Calcule le signe
        signe = 0 if self.exposant >= 0 else 1

        # Valeur absolue de l'exposant (limitée à 7 bits = de 0 à 127)
        valeur = abs(self.exposant)

        # Conversion en binaire sur 7 bits
        valeur_binaire = format(valeur, '07b') 

        # Ajout du bit de signe devant
        self.exposantBinaire = str(signe) + valeur_binaire

        res1 = [int(bit) for bit in self.mantisseBinaire]
        res2 = [int(bit) for bit in self.exposantBinaire]
        res = res1 + res2

        return res

    def __str__(self):
        """
        Affichage de la mantisse et de l'exposant sous forme décimale.
        """
        self.mantisse, self.exposant = self.code(self.reel) # on calcule la mantisse et l'exposant
        return f"{self.mantisse} x 10^{self.exposant}"
    
    def afficherBinaire(self):
        """
        Affichage de la mantisse et de l'exposant sous forme binaire.
        """
        coordonnees_binaires = self.codeBinaire(self.reel) # on calcule la mantisse et l'exposant en binaire 
        print(coordonnees_binaires)

    @staticmethod
    def decode(coordonnees_binaires):
        """
        Fonction qui décode la mantisse et l'exposant pour retrouver le nombre réel.
        """
        exposant = ''.join(map(str,coordonnees_binaires[-8:])) # les 8 derniers bits sont l'exposant
        mantisse = ''.join(map(str,coordonnees_binaires[:-8])) # le reste est la mantisse


        # Decodage de l'exposant
        exposant_decimal = binaire_en_entier(exposant)
        mantisse_decimal = binaire_en_entier(mantisse)

        print(f"{mantisse_decimal / (10 ** 5)} x 10^{exposant_decimal}")

    

# Test de création 
# ME = MantisseExposant()
# print(ME)
# coordonnees = ME.codeBinaire(12)
# ME.afficherBinaire()
# ME.decode(coordonnees)