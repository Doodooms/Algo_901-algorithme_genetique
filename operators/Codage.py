class codage_binaire():
    def codage(self, variables):
        # codage binaire pour chaque élément
        # A IMPLEMENTER
        pass

class codage_reel():
    def codage(self, variables):
        """"
        Transforme chaque élément de la liste en float
        """
        variables = [float(variables[i]) for i in range(len(variables))]
        return variables
    
if __name__=="__main__":
    x = [1, 2.5, 3, 4.7]
    codagereel = codage_reel()
    codagebinaire = codage_binaire()
    print(codagereel.codage(x))
    print(codagebinaire.codage(x))