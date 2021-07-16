#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        design = app.activeProduct

        ui  = app.userInterface
        ui.messageBox('Select Two Cylindrical Faces')
        selectedItem1 = ui.selectEntity("Select a Cylinder", "CylindricalFaces")
        selectedItem1Value = selectedItem1.point
        selectedItem2 = ui.selectEntity("Select a Cylinder", "CylindricalFaces")
        selectedItem2Value = selectedItem1.point
        lengthBetweenPoints = selectedItem1Value.distanceTo(selectedItem2Value)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
