import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        
        radius1 = 2
        radius2 = 0.156

        app = adsk.core.Application.get()
        ui = app.userInterface
        
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch1 = sketches.add(xyPlane)
        sketch2 = sketches.add(xyPlane)
        

        # Draw some circles.
        circle1 = sketch1.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius1)
        circle2 = sketch2.sketchCurves.sketchCircles.addByCenterRadius(adsk.core.Point3D.create(radius1, 0, 0), radius2)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))