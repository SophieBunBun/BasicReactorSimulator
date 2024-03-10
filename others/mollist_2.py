class mlist:
    
    def __init__(self):
        self._list=[]
        
    def mlistlen(self):
        return len(self._list)
    
    def index(self,mol):
        i=0
        b=True
        while i<self.mlenlist() and b:
            if self._list[i][0]==mol:
                b=False
            else:
                i+=1
        if not b:
            print('não')
        else:
            return i
        
    def getcount(self,mol):
        if self.index(mol)=='não':
            print('não')
        else:
            return self._list[self.index(mol)][1]
        
    def getobjects(self): #devolve uma lista com os objetos lá presentes
        w=[]
        for i in range(self.mlistlen):
            w+=self._list[i]
        return w
    
    def insert(self,mol,qtd):
        if self.index(mol)!='não':
            self._list[self.index(mol)][1]+=qtd
        else:
            self._list+=[mol,qtd]
            
    def remove(self,mol,qtd):
        if self.index(mol)!='não':
            self._list[self.index(mol)][1]=self._list[self.index(mol)][1]-qtd
        
            
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

