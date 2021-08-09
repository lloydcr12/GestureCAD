#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import threading, random, json, os, csv, math

ui = adsk.core.UserInterface.cast(None)
handlers = []
stopFlag = None
myCustomEvent = 'MyCustomEventId'
customEvent = None
Last_mod = os.path.getmtime('D:\Source\LeapPython37\handroll.csv')
app: adsk.core.Application = adsk.core.Application.get()

# Global Initial Camera Settings
view = app.activeViewport
camera = view.camera
glob_up = [camera.upVector.x, camera.upVector.y, camera.upVector.z]
glob_eye = [camera.eye.x, camera.eye.y, camera.eye.z]


# The event handler that responds to the custom event being fired.
class ThreadEventHandler(adsk.core.CustomEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, data):
        try:
            # Make sure a command isn't running before changes are made.
            if ui.activeCommand != 'SelectCommand':
                ui.commandDefinitions.itemById('SelectCommand').execute()
                            
            # Get the value from the JSON data passed through the event.
            eventArgs = json.loads(data.additionalInfo)
            rollangle = float(eventArgs['Roll'])
            yawangle = float(eventArgs['Yaw'])
            zoom = float(eventArgs['Zoom'])

            app: adsk.core.Application = adsk.core.Application.get()

            view = app.activeViewport
            camera = view.camera
            start_coords = [camera.eye.x, camera.eye.y, camera.eye.z]
            # Takes the roll angle from the csv and uses it to update the camera's up vector
            target = camera.target
            global glob_up
            up = [camera.upVector.x, camera.upVector.y, camera.upVector.z]
            C = math.cos(rollangle)
            S = math.sin(rollangle)
            new_coords = [glob_up[0] * C - glob_up[1] * S , glob_up[0]*S + glob_up[1]*C , glob_up[2]]
            new_up = adsk.core.Vector3D.create(new_coords[0], new_coords[1], new_coords[2])

            # Updates the camera zoom based on distance between palms
            camera.viewExtents = -1.5*zoom+1050

            camera.target = target
            camera.upVector = new_up

            # Takes the yaw angle from the csv and uses it to update the camera's position
            Cyaw = math.cos(yawangle)
            Syaw = math.sin(yawangle)

            global glob_eye
            eye1 = glob_eye
            targetpoint = adsk.core.Point3D.asArray(camera.target)
            x1 = eye1[0]
            z1 = eye1[2]
            x0 = targetpoint[0]
            z0 = targetpoint[2]
            x2 = Cyaw*(x1) - Syaw*(z1)
            z2 = Syaw*(x1) + Cyaw*(z1)

            eye2 = adsk.core.Point3D.create(x2, start_coords[1], z2)

            camera.eye = eye2

            camera.isSmoothTransition = False
            view.camera = camera
            adsk.doEvents()
            view.refresh()

        except:
            if ui:
                # ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                pass


# The class for the new thread.
class MyThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        # Every 0.01 seconds, check last modified time of target file
        Last_mod = os.path.getmtime('D:\Source\LeapPython37\handroll.csv')
        while not self.stopped.wait(0.01):
            if os.path.getmtime('D:\Source\LeapPython37\handroll.csv') > Last_mod:
                filename = 'D:\Source\LeapPython37\handroll.csv'
                with open(filename, 'r') as csvFile:
                    csvReader = csv.DictReader(csvFile)
                    for line in csvReader:
                        data = dict(line)
                    app.fireCustomEvent(myCustomEvent, json.dumps(data))
            
            Last_mod = os.path.getmtime('D:\Source\LeapPython37\handroll.csv')
        
        
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
        if handlers.count:
            customEvent.remove(handlers[0])
        stopFlag.set() 
        app.unregisterCustomEvent(myCustomEvent)
        ui.messageBox('Stop addin')
    except:
        if ui:
            # ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            pass