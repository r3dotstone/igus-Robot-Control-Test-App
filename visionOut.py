import pandas as pd
import time
from visionClass import vision

v = vision([
            {"pick": True, "posInt": 246, "time": 1714356330.463, "angle": 92.0, "posNow": 787, "id": 1},
            {"pick": False, "posInt": 257, "time": 1714356330.877, "angle": 93.4, "posNow": 617, "id": 2},
            {"pick": True, "posInt": 246, "time": 1714356331.249, "angle": 103.6, "posNow": 427, "id": 3},
            {"pick": True, "posInt": 244, "time": 1714356331.669, "angle": 84.1, "posNow": 245, "id": 4}
        ])

while True:
    v.looped()
    time.sleep(0.01)

























# # time = time.time() when measured
# cookies = [
#     {"pick": True, "posInt": 246, "time": 1714356330.463, "angle": 92.0, "posNow": 787, "id": 1},
#     {"pick": False, "posInt": 257, "time": 1714356330.877, "angle": 93.4, "posNow": 617, "id": 2},
#     {"pick": True, "posInt": 246, "time": 1714356331.249, "angle": 103.6, "posNow": 427, "id": 3},
#     {"pick": True, "posInt": 244, "time": 1714356331.669, "angle": 84.1, "posNow": 245, "id": 4}
# ]

# # Create the pandas DataFrame
# dfQ = pd.DataFrame(cookies)
# dfBox = pd.DataFrame(columns=dfQ.columns)
# dfBin = pd.DataFrame(columns=dfQ.columns)

# convVel = 450 # mm/s
# posPick = 2000 # mm from front edge of scanner
# timeLast = time.time()
# printTimeLast = 0
# while True:
#     timeNow = time.time()
#     dt = timeNow - timeLast
#     timeLast = timeNow
#     dfQ["posNow"] = dfQ["posNow"] + (convVel*dt)

#     dfPick = dfQ[(dfQ["pick"] == True) & (dfQ["posNow"] >= posPick)] 

#     if dfQ.empty: print("no more cookies :(")

#     elif (dfQ.at[dfQ.index[0],"pick"] == True) and (dfQ.at[dfQ.index[0],"posNow"] >= posPick):
#         print("picking id", dfQ.at[dfQ.index[0],"id"])
#         row_to_append = dfQ.loc[[dfQ.index[0]]]
#         dfBox = dfBox.append(row_to_append, ignore_index=True)
#         dfQ = dfQ.drop(dfQ.index[0])

#     elif (dfQ.at[dfQ.index[0],"pick"] == False) and (dfQ.at[dfQ.index[0],"posNow"] >= posPick):
#         print("binning id: ", dfQ.at[dfQ.index[0],"id"])
#         row_to_append = dfQ.loc[[dfQ.index[0]]]  # This keeps the row as a DataFrame
#         dfBin = dfBin.append(row_to_append, ignore_index=True)
#         dfQ = dfQ.drop(dfQ.index[0])

#     elif len(dfPick) > 1:
#         print("cookie overload!")
        
#     else: print("no cookies to pick :(")

#     if time.time() - printTimeLast >= 0.2:
#         print("dt=",dt,"\n",dfQ)
#         printTimeLast = timeNow

#     time.sleep(0.2)
