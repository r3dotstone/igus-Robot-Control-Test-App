import datetime
import sys
from time import sleep
from AppClient import AppClient
from MinimalApp import MinimalApp
from DataTypes.Matrix44 import Matrix44
from visionClass import vision
import time
import random
# from DataTypes.ProgramVariable import NumberVariable, PositionVariable, ProgramVariable


# Below you will find examples for sending requests from the app to the robot control.
# Also check MinimalApp.py for examples on how to handle requests from the robot control (e.g. user interface and program commands)


# Example: Requests and prints the tool center point (cartesian) position.
def ExamplePrintTCP(app: AppClient):
    tcp = app.GetTcp()
    print(
        f"TCP: X={tcp.GetX():.2f} Y={tcp.GetY():.2f} Z={tcp.GetZ():.2f} A={tcp.GetA():.2f} B={tcp.GetB():.2f} C={tcp.GetC():.2f}"
    )


# Example: Requests and prints a number variable. This variable must be defined in a m_running robot program.
def ExamplePrintNumberVariable(app: AppClient, variableName: str) -> float:
    try:
        numberVariable = app.GetNumberVariable(variableName)

        print(f'Program variable "{variableName}": {numberVariable.GetValue():.4f}')
        return numberVariable.GetValue()
    except RuntimeError as ex:
        print(f'Could not get number variable "{variableName}":', file=sys.stderr)
        print(
            "for this example please start the a program that defines this variable",
            file=sys.stderr,
        )
        print(ex, file=sys.stderr)
        return 0


# Example: Sets a number variable. The value increases with each call.
def ExampleSetNumberVariable(app: AppClient, variableName: str, value: float):
    try:
        app.SetNumberVariable(variableName, value)
    except RuntimeError as ex:
        print(f'Could not set number variable "{variableName}":', file=sys.stderr)
        print(
            "for this example please start the a program that defines this variable",
            file=sys.stderr,
        )
        print(ex, file=sys.stderr)

# Jaden tries to set position variable
# def JadenSetPositionVariable(app: AppClient, name: str, 
#         a1: float,
#         a2: float,
#         a3: float,
#         a4: float,):
#     try:
#         app.SetPositionVariable(name, 
#         a1,
#         a2,
#         a3,
#         a4,)
#     except RuntimeError as ex:
#         print(f'Could not set number variable "{name}":', file=sys.stderr)
#         print(
#             "for this example please start the a program that defines this variable",
#             file=sys.stderr,
#         )
#         print(ex, file=sys.stderr)

# Jaden tries again
def JadenSetPositionMatrix(app: AppClient, name: str, cartesianPosition: Matrix44, e1: float, e2: float, e3: float):
    try:
        app.SetPositionVariable(name, cartesianPosition,e1,e2,e3)
    except RuntimeError as ex:
        print(f'Could not set position variable "{name}":', file=sys.stderr)
        print(
            "for this example please start the a program that defines this variable",
            file=sys.stderr,
        )
        print(ex, file=sys.stderr)

# def SetPositionVariable(
#     self, name: str, cartesianPosition: Matrix44, e1: float, e2: float, e3: float
# ):
#     if not self.IsConnected():
#         raise RuntimeError("not connected")

#     request = robotcontrolapp_pb2.SetProgramVariablesRequest()
#     request.app_name = self.GetAppName()
#     variable = request.variables.add()
#     variable.name = name
#     variable.cartesian = cartesianPosition.ToGrpc()
#     variable.externalAxes.e1 = e1
#     variable.externalAxes.e2 = e2
#     variable.externalAxes.e3 = e3
#     self.__grpcStub.SetProgramVariables(request)


# Example: Requests and prints a position variable. This variable must be defined in a m_running robot program.
def ExamplePrintPositionVariable(app: AppClient, variableName: str):
    try:
        positionVariable = app.GetPositionVariable(variableName)

        print(
            f'Position variable "{variableName}" cart: '
            + f"X={positionVariable.GetCartesian().GetX():.2f} "
            + f"Y={positionVariable.GetCartesian().GetY():.2f} "
            + f"Z={positionVariable.GetCartesian().GetZ():.2f} "
            + f"A={positionVariable.GetCartesian().GetA():.2f} "
            + f"B={positionVariable.GetCartesian().GetB():.2f} "
            + f"C={positionVariable.GetCartesian().GetC():.2f}"
        )
        print(
            f'Position variable "{variableName}" joint: '
            + f"A1={positionVariable.GetRobotAxes()[0]:.2f} "
            + f"A2={positionVariable.GetRobotAxes()[1]:.2f} "
            + f"A3={positionVariable.GetRobotAxes()[2]:.2f} "
            + f"A4={positionVariable.GetRobotAxes()[3]:.2f} "
            + f"A5={positionVariable.GetRobotAxes()[4]:.2f} "
            + f"A6={positionVariable.GetRobotAxes()[5]:.2f} "
            + f"E1={positionVariable.GetExternalAxes()[0]:.2f} "
            + f"E2={positionVariable.GetExternalAxes()[1]:.2f} "
            + f"E3={positionVariable.GetExternalAxes()[2]:.2f}"
        )
    except RuntimeError as ex:
        print(f'Could not get position variable "{variableName}":', file=sys.stderr)
        print(
            "for this example please start the a program that defines this variable",
            file=sys.stderr,
        )
        print(ex, file=sys.stderr)


# Start the app
print("Starting minimal app example")

# The first command line argument (if given) is the connection target
connectionTarget = "localhost:5000"
if len(sys.argv) > 1:
    connectionTarget = sys.argv[1]

# Create an instance of the app and connect. The name given here must be equal to the name in rcapp.xml.
app = MinimalApp("MinimalApp-Python", connectionTarget)
app.Connect()

# time of the last example run
lastUpdate = datetime.datetime.now()

convVel = 50 #mm/s
# v = vision(convVel,[
#             {"pick": True, "posInt": 246, "time": 1714356330.463, "angle": 92.0, "posNow": 787, "id": 1},
#             {"pick": False, "posInt": 257, "time": 1714356330.877, "angle": 93.4, "posNow": 617, "id": 2},
#             {"pick": True, "posInt": 246, "time": 1714356331.249, "angle": 103.6, "posNow": 427, "id": 3},
#             {"pick": True, "posInt": 244, "time": 1714356331.669, "angle": 84.1, "posNow": 245, "id": 4}
#         ])

matrix = Matrix44()

moveflag = 0
posPick = 1700
posBin = 2000
sampled = False
item = {"pick": 1, "pos": 1600, "angle": 0}

try:
    var = 0
    # Keep the app running
    timeLast = time.time()

    while app.IsConnected():
        # sleep(0.1)

        # Run some examples every few seconds
        now = datetime.datetime.now()
        if now - lastUpdate > datetime.timedelta(seconds=0.1):
            lastUpdate = now

            try:
                # GET
                timeNow = time.time()
                dt = timeNow - timeLast
                timeLast = timeNow
                item["pos"] = item["pos"] + (convVel*dt)         
                moveflag = ExamplePrintNumberVariable(app, "moveflag")
                
                # SET
                if item["pos"] >= posPick: passflag = 1
                else: passflag = 0
                pickflag = item["pick"]
                ExampleSetNumberVariable(app, "passflag", passflag)
                print("passflag: ", passflag,"pickflag: ", pickflag)
                ExampleSetNumberVariable(app, "pickflag", pickflag)
                
                if  (pickflag == 1) and passflag == 1: # picking
                    print("STATE: picking...")
                    if (sampled == False):
                        sampled = True
                        matrix.SetX(465)
                        matrix.SetY(item["pos"]-1500)
                        matrix.SetZ(210)
                        matrix.SetA(item["angle"])
                        JadenSetPositionMatrix(app, "pypos", matrix,0,0,0)  

                elif (item["pick"] == 0):
                    print("STATE: bad item, waiting for good item...")

                else: print("STATE: waiting...")

                if moveflag == 1: 
                    if pickflag == 1: sampled = False
                    item = {"pick": random.choice([1,0]), "pos": random.randint(1400,1500), "angle": random.randint(-20,20)}
                    ExampleSetNumberVariable(app, "moveflag", 0)


                ExamplePrintTCP(app)
                print("item: ", item) 
                print("dt: ", dt, "\n")
            
            except RuntimeError:
                pass

# Make sure to disconnect on exception
finally:
    app.Disconnect()
    print("Minimal app example stopped")


####################################################################

    #  def SetPositionVariable(
#         self,
#         name: str,
#         a1: float,
#         a2: float,
#         a3: float,
#         a4: float,
#         a5: float,
#         a6: float,
#         e1: float,
#         e2: float,
#         e3: float,
#     ):

                # moveflag = ExamplePrintNumberVariable(app, "moveflag")
                # status, angle, posY = v.looped()
                # posY = posY - 1500 # make relative to robot frame

                # if moveflag == 0: print("moving...")
                
                # elif moveflag == 1.0:
                #     if status == "picking":
                #         print("picking in app.py...")
                #         posX = 400#0
                #         posZ = 210
                #         ExampleSetNumberVariable(app, "placeflag", 1)
                #         ExampleSetNumberVariable(app, "moveflag", 0)
                        
                #     elif status == "binning":
                #         print("binning in app.py...")
                #         posX = #350
                #         posZ = #210
                #         ExampleSetNumberVariable(app, "placeflag", 0)
                #         ExampleSetNumberVariable(app, "moveflag", 0)
                #     elif status == "waiting":
                #         print("waiting in app.py...")
                #         posX = 0
                #         posZ = 210
                #         ExampleSetNumberVariable(app, "placeflag", 0)
                #     matrix.SetX(posX)
                #     matrix.SetY(posY+1000)
                #     matrix.SetZ(posZ)
                #     matrix.SetA(angle)
                #     JadenSetPositionMatrix(app, "pypos", matrix,0,0,0)

                # else: print("something is wrong!")




                # var = 300.0
                # ExamplePrintTCP(app)
                # ExampleSetNumberVariable(app, "myNrVar", var)
                # ExamplePrintNumberVariable(app, "myNrVar")
                # ExamplePrintPositionVariable(app,"pypos")
                # ExamplePrintPositionVariable(app, "apppos")
                # value = ExamplePrintNumberVariable(app, "appnum")