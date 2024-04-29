import pandas as pd
import time

# time = time.time() when measured
cookies = [
    {"pick": True, "posInt": 246, "time": 1714356330.463, "angle": 209.95, "posNow": 787},
    {"pick": False, "posInt": 257, "time": 1714356330.877, "angle": 200.03, "posNow": 617},
    {"pick": True, "posInt": 246, "time": 1714356331.249, "angle": 209.81, "posNow": 427},
    {"pick": True, "posInt": 244, "time": 1714356331.669, "angle": 190.99, "posNow": 245}
]

# Create the pandas DataFrame
dfQ = pd.DataFrame(cookies)

convVel = 450 # mm/s
pickLocation = 2000 # mm from front edge of scanner
timeLast = time.time()
printTimeLast = 0
while True:
    timeNow = time.time()
    dt = timeNow - timeLast
    timeLast = timeNow
    dfQ["posNow"] = dfQ["posNow"] + (convVel*dt)

    dfPick = dfQ[(dfQ["pick"] == True) and (dfQ["posNow"] >= pickLocation)] 
    if len(dfPick) == 1:
        print("picking position", dfPick["posNow"])
        dfQ = dfQ.drop(dfQ.index[0])
    if len(dfPick) > 1:
        print("cookie overload!")
    else: print("no cookies to pick :(")
    # if dfQ["pick"] == True and dfQ["posNow"] >= 2000:


    if time.time() - printTimeLast >= 0.2:
        print("dt=",dt,"\n",dfQ)
        printTimeLast = timeNow

    time.sleep(0.01)
