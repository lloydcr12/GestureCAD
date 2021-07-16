#Author-
#Description-


import adsk.core, adsk.fusion, adsk.cam, traceback,threading
import math
import time



times = 0


def eachMove():
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface


        #get product        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('No active Fusion design', 'No Design')
            return


        # Get the root component of the active design.
        rootComp = design.rootComponent
        #get array of occurrences
        occurrences = rootComp.occurrences.asList
        
        #get first component
        occurrence_first = occurrences.item(0)
        
         #get second component
        occurrence_second= occurrences.item(1)
        
        #get thrid component
        occurrence_third= occurrences.item(2)
        
       
        while (times < 20):           
            
            #translate the first component by updating [translation] property

            #wrong way: occurrence.transform will clone and return a matrix
            #so any change on this cloned matrix does not take effect on the 
            #update of component
            #offsetVector = adsk.core.Vector3D.create(5.0, 0, 0)
            #occurrence.transform.translation.add( offsetVector )
        
            # Get the current transform of the first occurrence
            transform = occurrence_first.transform
            
            if times <10:
                # Change the transform data by moving 5.0cm on X+ axis
                transform.translation = adsk.core.Vector3D.create( transform.translation.x +  5.0, 0, 0)
            else:
                # Change the transform data by moving 5.0cm on X- axis
                transform.translation = adsk.core.Vector3D.create( transform.translation.x -  5.0, 0, 0)
                
            # Set the tranform data back to the occurrence
            occurrence_first.transform = transform
            
            # Get the current transform of the second occurrence
            transform = occurrence_second.transform
            
            
            rotX = adsk.core.Matrix3D.create()
            # Change the transform data by rotating around Z+ axis

            rotX.setToRotation(math.pi/4, adsk.core.Vector3D.create(0,0,1), adsk.core.Point3D.create(0,0,0))
            transform.transformBy(rotX)
            
             # Set the tranform data back to the occurrence
            occurrence_second.transform = transform
            
             # Get the current transform of the third occurrence
            transform = occurrence_third.transform
            
            if times <10:
                # Change the transform data by moving 5.0cm on Y+ axis
                transform.setCell(1,3,transform.getCell(1,3) + 5.0)
            else:
                # Change the transform data by moving 5.0cm on Y- axis
                transform.setCell(1,3,transform.getCell(1,3) - 5.0)
                 

            #rotate around Z+ axis
            rotZSin = math.sin(math.pi/4 * times)
            rotZCos = math.cos(math.pi/4 * times)
            
            #change the cells value 
            transform.setCell(0,0,rotZCos)
            transform.setCell(0,1,rotZSin)
            transform.setCell(1,0,-rotZSin)
            transform.setCell(1,1,rotZCos) 
            
             # Set the tranform data back to the occurrence
            occurrence_third.transform = transform
            
            
            global times
            times =times +1 
            time.sleep( 0.1 )

            #Calling doEvents gives it a chance to catch up each time the components are transformed. 
            adsk.doEvents() 

       
        
       
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def run(context): 
    global times
    times = 0
    eachMove() 
   
