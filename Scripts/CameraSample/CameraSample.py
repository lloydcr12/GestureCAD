import adsk.core, adsk.fusion, traceback, math, pickle

def move_camera(app, view):
    try:
        camera = view.camera

        with open("C:\Users\admin\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts\FibonacciTutorial\file.pickle", mode="rb") as fileObj:
            obj=pickle.load(fileObj)
        
        target = adsk.core.Point3D.create(0,0,0)
        up = adsk.core.Vector3D.create(1,0,0)
        steps = 1000
        
        dist = camera.target.distanceTo(camera.eye)
    
        for i in range(0, steps):
            eye = adsk.core.Point3D.create(dist * math.cos((math.pi*2) * (i/steps)), dist * math.sin((math.pi*2) * (i/steps)), 10)
            
            camera.eye = eye
            camera.target = target
            camera.upVector = up
        
            camera.isSmoothTransition = False
            view.camera = camera
            adsk.doEvents()
            view.refresh()
    except:
        ui = app.userInterface
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def main():
    ui = None
  
    try:
        print('hello, world')
        app = adsk.core.Application.get()
        move_camera(app, app.activeViewport)
    
    except:
        ui = app.userInterface
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

      
main()