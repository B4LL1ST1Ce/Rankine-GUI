import CoolProp.CoolProp as CP

class States:
    def __init__(self):
        self.h = None
        self.s = None
        self.t = None
        self.p = None
        self.q = None
        self.d = None
        self.v = None
        
    def enterValues(self, type1, data1, type2, data2, p, t):
        match type1:
            case "H":
                self.h = data1
            case "S":
                self.s = data1
            case "T":
                if data1 == None:
                    self.t = None
                    return
                elif t == "\u00b0C":
                    self.t = data1+273
                elif t == "K":
                    self.t = data1
                if t == "\u00b0F":
                    self.t = ((data1-32)*(5/9))+273
            case "P":
                if data1 == None:
                    self.p = None
                    return
                if p == "MPa":
                    self.p = data1*1000000
                elif p == "bar":
                    self.p = data1*100000
                elif p == "kPa":
                    self.p = data1*1000
                elif p == "Pa":
                    self.p = data1
            case "Q":
                self.q = data1
            case "D":
                self.d = data1
        match type2:
            case "H":
                self.h = data2
            case "S":
                self.s = data2
            case "T":
                if data2 == None:
                    self.t = None
                    return
                elif t == "\u00b0C":
                    self.t = data2+273
                elif t == "K":
                    self.t = data2
                elif t == "\u00b0F":
                    self.t = ((data2-32)*(5/9))+273
                elif t == "\u00b0R":
                    self.t = data2*(5/9)
            case "P":
                if data2 == None:
                    self.p = None
                    return
                if p == "MPa":
                    self.p = data2*1000000
                elif p == "bar":
                    self.p = data2*100000
                elif p == "kPa":
                    self.p = data2*1000
                elif p == "Pa":
                    self.p = data2
            case "Q":
                self.q = data2
            case "D":
                self.d = data2
    
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
            case "D":
                self.d = data
            case "V":
                self.v = data
    
    def resetValues(self):
        self.h = None
        self.s = None
        self.t = None
        self.p = None
        self.q = None
        self.d = None
        self.v = None