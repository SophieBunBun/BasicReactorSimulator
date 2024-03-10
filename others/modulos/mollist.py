class molList:
    
    def __init__(self):
        self.list = []

    #Return length of list (object count)
    def mollistLen(self):
        return len(self.list)
    
    #Gets index of object in list, returns -1 if object is not in list
    def index(self, obj):
        return -1 + sum(x + 1 for x in range(self.mollistLen()) if self.list[x][0] == obj)
    
    #Gets count of object in list, returns 0 if object does not exist
    def getCount(self, obj):
        return self.list[self.index(obj)][1] if self.index(obj) > -1 else 0
    
    #Return list of objects in list
    def getObjects(self):
        return [y[0] for y in self.list]
    
    #If object being insert does not exist, attach object
    def insert(self, obj, count):
        self.list = [y for y in self.list if y[0] != obj] + [[obj, self.getCount(obj) + count]] if self.index(obj) > -1 else self.list + [[obj, count]]
    
    #If object being removed does not exist, return list // if current count - count < 0 value becomes negative (since it will never happen we didnt implement it)
    def remove(self, obj, count):
        self.list = [y for y in self.list if y[0] != obj] + [[obj, self.getCount(obj) - count]] if self.index(obj) > -1 else [y for y in self.list if y[0] != obj]
