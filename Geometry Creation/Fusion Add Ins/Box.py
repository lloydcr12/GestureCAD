#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import threading, random, json, os, csv, math, time
from collections import OrderedDict

ui = adsk.core.UserInterface.cast(None)
handlers = []
stopFlag = None
myCustomEvent = 'MyCustomEventId'
customEvent = None
Last_mod = os.path.getmtime('D:\Source\LeapPython37\handscoords.csv')
app: adsk.core.Application = adsk.core.Application.get()
gate = 0

z1dim = []
z2dim = []
x1dim = []
x2dim = []
extrudeParam = []
offsetParam = []
view = app.activeViewport
## FUTURE WORK, AUTO SET CAMERA POSITION
# camera = view.camera
# eye = adsk.core.Point3D.create(-450, 411, -700)
# target = adsk.core.Point3D.create(300, 0, 300)
# camera.eye = eye
# camera.target = target
# view.camera = camera

#GENERATE GEOMETRY
#initial shape
x1 = 325
z1 = 325
y1 = 325
x2 = 350
z2 = 350
y2 = 350

design = adsk.fusion.Design.cast(app.activeProduct)    
# Get the root component of the active design.
rootComp = design.rootComponent

# Create a new sketch on the xy plane.
sketches = rootComp.sketches
planes = rootComp.constructionPlanes
planeInput = planes.createInput()
xzPlane = rootComp.xZConstructionPlane
offsetValue = adsk.core.ValueInput.createByReal(y1)
planeInput.setByOffset(xzPlane, offsetValue)
plane = planes.add(planeInput)
sketch1 = sketches.add(plane)
# define points
rectanglepoint1 = adsk.core.Point3D.create(x1, z1, 0)
rectanglepoint2 = adsk.core.Point3D.create(x2, z2, 0)
origin = adsk.core.Point3D.create(0, 0, 0)
# make sketch points 
sketchPoints = sketch1.sketchPoints
sketchPoint1 = sketchPoints.add(rectanglepoint1)
sketchPoint2 = sketchPoints.add(rectanglepoint2)
sketchOrigin = sketchPoints.add(origin)
sketchOrigin.isFixed = True
#sketch rectangle
box = sketch1.sketchCurves.sketchLines.addTwoPointRectangle(sketchPoint1, sketchPoint2)
#make dimensions
z1dim = sketch1.sketchDimensions.addDistanceDimension(sketchOrigin, sketchPoint1, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, rectanglepoint1)
z2dim = sketch1.sketchDimensions.addDistanceDimension(sketchOrigin, sketchPoint2, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, rectanglepoint1)
x1dim = sketch1.sketchDimensions.addDistanceDimension(sketchOrigin, sketchPoint1, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, rectanglepoint2)
x2dim = sketch1.sketchDimensions.addDistanceDimension(sketchOrigin, sketchPoint2, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, rectanglepoint2)
#extrude
extrudes = rootComp.features.extrudeFeatures
# Get the profile defined by the rectangle
prof = sketch1.profiles.item(0)
# Extrude Sample 1:
extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
# Create a distance extent definition
distance = adsk.core.ValueInput.createByReal(abs(y2-y1))     
extent_distance = adsk.fusion.DistanceExtentDefinition.create(distance) 
extrudeInput.setOneSideExtent(extent_distance, adsk.fusion.ExtentDirections.PositiveExtentDirection)       
# Get the extrusion body
extrude1 = extrudes.add(extrudeInput)
body1 = extrude1.bodies.item(0)
body1.name = "box 1"
ParamCount = design.rootComponent.modelParameters.count
extrudeParam = design.rootComponent.modelParameters.item(ParamCount-2) #extrude distance is named d5 for some reason parameters-7
offsetParam = design.rootComponent.modelParameters.item(ParamCount-7) #extrude distance is named d5 for some reason parameters -1


# The event handler that responds to the custom event being fired.
class ThreadEventHandler(adsk.core.CustomEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, data):
        try:
            # Make sure a command isn't running before changes are made.
            if ui.activeCommand != 'SelectCommand':
                ui.commandDefinitions.itemById('SelectCommand').execute()

            global z1dim
            global z2dim
            global x1dim
            global x2dim
            global extrudeParam
            global offsetParam
            global camera
            global view


                            
            # Get the value from the JSON data passed through the event.
            eventArgs = json.loads(data.additionalInfo)
            x1 = float(eventArgs['x1'])
            y1 = float(eventArgs['y1'])
            z1 = -float(eventArgs['z1'])
            x2 = float(eventArgs['x2'])
            y2 = float(eventArgs['y2'])
            z2 = -float(eventArgs['z2'])
            S1 = float(eventArgs['s1'])
            S2 = float(eventArgs['s2'])

            x1 = x1 + 300
            x2 = x2 + 300
            z1 = z1 + 300
            z2 = z2 + 300

            global gate

            if S1 == 1 and S2 ==1:
                
                #change parameters
                z1dim.parameter.value = z1
                z2dim.parameter.value = z2
                x1dim.parameter.value = x1
                x2dim.parameter.value = x2
                #change extrude
                extrudeParam.value = abs(y2-y1)
                #change offset
                offsetParam.value = min(abs(y1),abs(y2))
                gate = 1

            if gate == 1:

                if S1 < 0.5 or S2 < 0.5 :
                    mLibs = app.materialLibraries
                    appearanceLib1 = mLibs.itemByName("Fusion 360 Appearance Library")          
                    aOne = appearanceLib1.appearances.itemByName("Paint - Enamel Glossy (Green)")
                    body1.appearance = aOne
                    app.activeViewport.refresh()
                    adsk.terminate()

        except:
            if ui:
                ## Error messages for development, commented out to avoid CSV reading error
                # ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                pass


# The class for the new thread.
class MyThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        # Every 0.1 seconds, check last modified time of target file
        Last_mod = os.path.getmtime('D:\Source\LeapPython37\handscoords.csv')
        while not self.stopped.wait(0.05):
            if os.path.getmtime('D:\Source\LeapPython37\handscoords.csv') > Last_mod:
                filename = 'D:\Source\LeapPython37\handscoords.csv'
                with open(filename, 'r') as csvFile:
                    csvReader = csv.DictReader(csvFile)
                    for line in csvReader:
                        data = dict(line)
                    app.fireCustomEvent(myCustomEvent, json.dumps(data))
            
            Last_mod = os.path.getmtime('D:\Source\LeapPython37\handscoords.csv')
        
        
def run(context):
    global ui
    global app
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
       
        # Register the custom event and connect the handler.
        global customEvent
        customEvent = app.registerCustomEvent(myCustomEvent)
        onThreadEvent = ThreadEventHandler()
        customEvent.add(onThreadEvent)
        handlers.append(onThreadEvent)

        # Create a new thread for the other processing.        
        global stopFlag        
        stopFlag = threading.Event()
        myThread = MyThread(stopFlag)
        myThread.start()
    except:
        if ui:
            # ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            pass


def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        if handlers.count:
            customEvent.remove(handlers[0])
        stopFlag.set() 
        app.unregisterCustomEvent(myCustomEvent)

    except:
        if ui:
            # ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            pass