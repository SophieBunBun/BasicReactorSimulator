#import mlist #em stand-by, descarregar e carregar o módulo
import random

class cubo:
    
    def __init__(self, aresta):
        self._tanque=[[[[] for x in range(aresta)] for y in range(aresta)] for z in range(aresta)]
        
    def aresta(self):
        return len(self._tanque)
    
    def volume(self):
        return (self.aresta())**3
    
    def insert(self,mol,coords): #Coords dadas por uma lista de listas do tipo [x,y,z]
        self._tanque[coords[0]][coords[1]][coords[2]]+=[mol]
        
    def remove(self,mol,coords):
        self._tanque[coords[0]][coords[1]][coords[2]].remove(mol)
        
    def move(self,mol,coords,vetor): #aaaaaaaaaaaaaa
        posfin=[]
        for i in range(3):    
            posfin+=[coords[i]+vetor[i]]
        self.insert(mol,posfin)
        self.remove(mol,coords)
        
    def cubinhos_com_coisas(self):
        w=[]
        for x in range(self.aresta()):
            for y in range(self.aresta()):
                for z in range(self.aresta()):
                    if self._tanque[x][y][z]!=[]:
                        w.append([x,y,z])
        return w
    
    def cenas_no_cubinho(self,coords):
        return self._tanque[coords[0]][coords[1]][coords[2]]

    def insertRandom(self,mol):
        self.insert(mol,[random.randint(0,self.aresta()),random.randint(0,self.aresta())],random.randint(0,self.aresta()))

    

