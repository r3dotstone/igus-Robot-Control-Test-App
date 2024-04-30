import pandas as pd
import numpy as np
import time

class vision():

    def __init__(self, convVel = 450, data = [
            {"pick": True, "posInt": 246, "time": 1714356330.463, "angle": 92.0, "posNow": 787, "id": 1},
            {"pick": False, "posInt": 257, "time": 1714356330.877, "angle": 93.4, "posNow": 617, "id": 2},
            {"pick": True, "posInt": 246, "time": 1714356331.249, "angle": 103.6, "posNow": 427, "id": 3},
            {"pick": True, "posInt": 244, "time": 1714356331.669, "angle": 84.1, "posNow": 245, "id": 4}
        ]):
        # time = time.time() when measured

        # Create the pandas DataFrame
        self.dfQ = pd.DataFrame(data)
        self.dfBox = pd.DataFrame(columns=self.dfQ.columns)
        self.dfBin = pd.DataFrame(columns=self.dfQ.columns)

        self.convVel = convVel # mm/s
        self.posPick = 2000 # mm from front edge of scanner
        self.timeLast = time.time()
        self.printTimeLast = 0

    def looped(self): # goes in a continuous loop

        timeNow = time.time()
        dt = timeNow - self.timeLast
        self.timeLast = timeNow
        self.dfQ["posNow"] = self.dfQ["posNow"] + (self.convVel*dt)

        dfPick = self.dfQ[(self.dfQ["pick"] == True) & (self.dfQ["posNow"] >= self.posPick)] 

        if self.dfQ.empty: 
            print("no more cookies :(") # picked all the cookies
            status = "error"            
            angle = 90 # get ready to pick next good cookie
            position = 1500 + 350

        elif (self.dfQ.at[self.dfQ.index[0],"pick"] == True) and (self.dfQ.at[self.dfQ.index[0],"posNow"] >= self.posPick): # current pick target is good
            print("picking id: ", self.dfQ.at[self.dfQ.index[0],"id"])
            row_to_append = self.dfQ.loc[[self.dfQ.index[0]]]
            self.dfBox = self.dfBox.append(row_to_append, ignore_index=True)
            self.dfQ = self.dfQ.drop(self.dfQ.index[0])
            status = "picking"
            angle = self.dfBox.at[self.dfBox.index[0],"angle"]
            position = self.dfBox.at[self.dfBox.index[0],"posNow"]

        elif (self.dfQ.at[self.dfQ.index[0],"pick"] == False) and (self.dfQ.at[self.dfQ.index[0],"posNow"] >= self.posPick): # current pick target is bad
            print("binning id: ", self.dfQ.at[self.dfQ.index[0],"id"])
            row_to_append = self.dfQ.loc[[self.dfQ.index[0]]]
            self.dfBin = self.dfBin.append(row_to_append, ignore_index=True)
            self.dfQ = self.dfQ.drop(self.dfQ.index[0])
            status = "binning"            
            angle = 90 # get ready to pick next good cookie
            position = 1500 + 350

        elif len(dfPick) > 1: # something has gone wrong and there is more than one cookie beyond the pick position
            print("cookie overload!")
            status = "error"
            angle = 90 # get ready to pick next good cookie
            position = 1500 + 350

        else: 
            print("no cookies to pick :(") # all the cookies haven't arrived or dissapeared
            status = "waiting"
            angle = 90 # get ready to pick next good cookie
            position = 1500 + 350

        #if time.time() - self.printTimeLast >= 0.2:
        print("dt=",dt,"\n",self.dfQ)
        print("angle: ", angle, "position: ", position,"\n")
            #self.printTimeLast = timeNow

        return status, angle, position # angle for A axis to navigate to in base frame, 
                                # Y position of current pick target, relative to farthest up-conveyor edge of the camera pod