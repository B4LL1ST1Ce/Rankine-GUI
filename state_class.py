import CoolProp.CoolProp as CP

class States:
    def __init__(self):
        self.h = None
        self.s = None
        self.t = None
        self.p = None
        self.q = None
        
    def enterValues(self, type1, data1, type2, data2):
        match type1:
            case "H":
                self.h = data1
            case "S":
                self.s = data1
            case "T":
                if data1 == None:
                    self.t = None
                else:
                    self.t = data1+273
            case "P":
                self.p = data1
            case "Q":
                self.q = data1
        match type2:
            case "H":
                self.h = data2
            case "S":
                self.s = data2
            case "T":
                if data2 == None:
                    self.t = None
                else:
                    self.t = data2+273
            case "P":
                self.p = data2
            case "Q":
                self.q = data2
    
    def updateValues(self, type, data):
        match type:
            case "H":
                self.h = data
            case "S":
                self.s = data
            case "T":
                self.t = data
            case "P":
                self.p = data
            case "Q":
                self.q = data
    
    def resetValues(self):
        self.h = None
        self.s = None
        self.t = None
        self.p = None
        self.q = None