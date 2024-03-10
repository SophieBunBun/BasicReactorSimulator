import cube as cb
import mollist as ml
import random

class simulation:
    
    #objList comes in as a molList class
    def __init__(self, objList, size):
        
        #Current object count in system (gets updated after every time the number of particles in system changes)
        self.totalMolCount = objList
        
        #Total retrieved objects
        self.totalMolRetrieved = ml.molList()
        
        #Total consumed objects
        self.totalMolConsumed = objList
        
        #3d simulation space
        self.simSpace = cb.cube(size)
        
        #Insert objects into cube at random
        for obj in self.totalMolCount.getObjects():
            for i in range(self.totalMolCount.getCount(obj)):
                
                #Generate random coordinates
                randCoords = [(random.randint(0, self.simSpace.size() - 1)) for i in range(3)]
                self.simSpace.insertObj(obj, randCoords)
                                               
    def globalMoveEvent(self, moveMaxDistance):
        
        #Choose coordinates in cube where there are objects, run for every object within cell
        for coords in self.simSpace.getCellsWithObj():
            
            for obj in self.simSpace.getObjListInCell(coords):
            
                #Generate movement vector
                randVector = [random.randint(-moveMaxDistance, moveMaxDistance) for i in range(3)]
                
                #Move object to coordinates
                self.simSpace.moveObj(obj, coords, randVector) 
            
    
    def reactionEvent(self):
        
        #Choose coordinates in cube where there are objects
        for coords in self.simSpace.getCellsWithObj():
            
            #Getting a list of every object in the cell
            objList = self.simSpace.getObjListInCell(coords)

            #Select reaction to perform
            #Reaction 1: A + B -> C
            while (objList.count("A")) > 0 and (objList.count("B")) > 0:
                
                #Do reaction
                self.simSpace.removeObj("A", coords)
                self.simSpace.removeObj("B", coords)
                self.simSpace.insertObj("C", coords)
                
            #Reaction 2 & 3: C + A -> 2A + B or C + B -> A + 2B
            while (objList.count("C")) > 0 and ((objList.count("A")) > 0 or objList.count("B") > 0):
                
                self.simSpace.removeObj("C", coords)
                self.simSpace.insertObj("A", coords)
                self.simSpace.insertObj("B", coords)  
                
            #Reaction 4: 2C -> 2A + 2B
            while (objList.count("C")) > 1:
                
                for i in range(2):
                    self.simSpace.removeObj("C", coords)
                    self.simSpace.insertObj("A", coords)
                    self.simSpace.insertObj("B", coords)
                    
        #Update molecule lists
        self.totalMolCount = self.simSpace.getObjectTotals()
        
    def insertEvent(self, obj, count):
        
        self.totalMolCount.insert(obj, count)
        self.totalMolConsumed.insert(obj, count)
        
        #Definir por vizinhança
        
        for i in range(count):
            
            #Generate random coordinates within 1/4 of the space
            randCoords = [(random.randint(0, round((self.simSpace.size() - 1) / 4))) for i in range(3)]
        
            if obj == "A":
    
                randCoords[2] += round(((self.simSpace.size() - 1) * 3) / 4)
                    
            elif obj == "B":
                
                for x in range(3):
                    
                    randCoords[x] += round(((self.simSpace.size() - 1) * 3) / 4)
                
            self.simSpace.insertObj(obj, randCoords)
    
    #If count is -1 it removes all in one area, else removes count from area
    def removeEvent(self, obj):
        
        #Get list of coordinates within 0 <= x, y, z <= L/4 that contains object
        for coords in [y for y in self.simSpace.getCellsWithObj() if ((y[0] <= round((self.simSpace.size() - 1) / 4)) and (y[1] <= round((self.simSpace.size() - 1) / 4)) and (y[2] <= round((self.simSpace.size() - 1) / 4))) and (self.simSpace.getObjListInCell(y).count(obj) > 0)]:
            
            for i in self.simSpace.getObjListInCell(coords):   
            
                if i == obj:
                    
                    #Remove object from coordinate and add 1 to totalMol for that obj
                    self.simSpace.removeObj(obj, coords)
                    self.totalMolRetrieved.insert(obj, 1)
                    
                    self.totalMolCount.remove(obj, 1)
            
            
            