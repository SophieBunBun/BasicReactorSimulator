class event:
    
    def __init__(self, t, k):
        self.time = t
        self.kind = k

class cap:
    
    def __init__(self):
        self.cap = []
        
    def addEvent(self, e):
        self.cap = [e1 for e1 in self.cap if e1.time < e.time] + [e] + [e1 for e1 in self.cap if e1.time > e.time]
        
    def delCurrentEvent(self):
        self.cap = self.cap[1:] if len(self.cap) > 0 else []
        
    def currentEvent(self):
        return self.cap[0]