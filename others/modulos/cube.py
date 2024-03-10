import mollist as ml
import itertools as it

class cube:
    
    def __init__(self, size):
        self.space = [[[[] for z in range(size)] for y in range(size)] for x in range(size)]
    
    #Return cube size (L for L^3)
    def size(self):
        return len(self.space)
    
    #Insert object onto a desired cell using its coordinates
    def insertObj(self, obj, coords):
        self.space[coords[0]][coords[1]][coords[2]].append(obj)
    
    #Remove object from a desired cell using its coordinates
    def removeObj(self, obj, coords):
        self.space[coords[0]][coords[1]][coords[2]].remove(obj)
    
    #Move an object from a certain coordinate by a vector
    def moveObj(self, obj, coords, vector):
        
        if self.space[coords[0]][coords[1]][coords[2]].count(obj) > 0:
            
            #Get "Wall bounce" if vector goes out of bounds
            vector = [(vector[i] if 0 <= int(coords[i] + vector[i]) < self.size() else max(min(coords[i] + vector[i], self.size()  - 1),0) - coords[i] - ((coords[i] + vector[i]) % (self.size()  - 1))) for i in range(3)]
            
            #Calculate final object position
            finalCoords = [int(coords[i] + vector[i]) for i in range(3)]
            
            #Move object
            self.insertObj(obj, finalCoords)
            self.removeObj(obj, coords)
    
    #Returns a list of all the coordinates where there exists objects within a cell
    def getCellsWithObj(self):
        a = []
        for x, y, z in it.product(range(self.size()), range(self.size()), range(self.size())):
            if self.space[x][y][z] != []:
                a.append([x,y,z])
        return a
    
    #Returns a list of all the objects inside a cell
    def getObjListInCell(self, coords):
        return self.space[coords[0]][coords[1]][coords[2]]
    
    #Gets the total count of all objects within cube
    def getObjectTotals(self):
        
        mollist = ml.molList()
        
        for coords in self.getCellsWithObj():
            
            cell = self.getObjListInCell(coords)
            
            while cell != []:
                
                mollist.insert(cell[0], cell.count(cell[0]))
                cell = [y for y in cell if y != cell[0]]
                
        return mollist
            
            
            
            
            
            
            