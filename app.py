import datetime
import sys
from time import sleep
from AppClient import AppClient
from MinimalApp import MinimalApp
from DataTypes.Matrix44 import Matrix44
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

try:
    var = 0
    # Keep the app running
    while app.IsConnected():
        sleep(0.1)

        # Run some examples every few seconds
        now = datetime.datetime.now()
        if now - lastUpdate > datetime.timedelta(seconds=3):
            lastUpdate = now

            try:
                var = 300.0
                matrix = Matrix44()
                matrix.SetX(400)
                matrix.SetY(20)
                matrix.SetZ(var)
                ExamplePrintTCP(app)
                # ExampleSetNumberVariable(app, "myNrVar", var)
                # ExamplePrintNumberVariable(app, "myNrVar")
                JadenSetPositionMatrix(app, "pypos", matrix,0,0,0)
                ExamplePrintPositionVariable(app,"pypos")
                # ExamplePrintPositionVariable(app, "apppos")
                # value = ExamplePrintNumberVariable(app, "appnum")
                # ExampleSetNumberVariable(app, "appnum", value + 1)
            except RuntimeError:
                pass

# Make sure to disconnect on exception
finally:
    app.Disconnect()
    print("Minimal app example stopped")


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
