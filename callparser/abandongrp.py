# Contains client class which contains summed/averaged data from each spreadsheet

class AbandonGrp():

    def __init__(self):
        self.Call_ID = 0
        self.Internal_Party = 0
        self.External_Party = 0
        self.Answered = 0
        self.Start_Time = 0
        self.End_Time = 0
        self.Call_Duration = 0

    def __hash__(self):
        return self.Call_ID

    def __eq__(self, other):
        return self.Call_ID == other.Call_ID

    def __str__(self):
        print("self.Call_ID: " , self.Call_ID)
        print("self.Internal_Party: " , self.Internal_Party)
        print("self.External_Party: " , self.External_Party)
        print("self.Start_Time: " , self.Start_Time)
        print("self.Answered: " , self.Answered)
        print("self.Call_Duration: " , self.Call_Duration)
        print("self.End_Time: " , self.End_Time)
   
    def setRow(self, Call_ID, Internal_Party, External_Party, Answered, Start_Time, End_Time, Call_Duration):
        self.Call_ID = Call_ID
        self.Internal_Party = Internal_Party
        self.External_Party = External_Party
        self.Answered = Answered
        self.Start_Time = Start_Time
        self.End_Time = End_Time
        self.Call_Duration = Call_Duration

    def getInternal_Party(self):
        return self.Internal_Party
    
    def getCall_ID(self):
        return self.Call_ID
    
    def getExternal_Party(self):
        return self.External_Party
    
    def getAnswered(self):
        return self.Answered
    
    def getStart_Time(self):
        return self.Start_Time
    
    def getEnd_Time(self):
        return self.End_Time
    
    def getCall_Duration(self):
        return self.Call_Duration
        



        
