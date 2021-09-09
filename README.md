# GestureCAD
Gesture based CAD project using Leap Motion Orion to control Fusion 360 as part of a summer internship at the University of Bristol DMF Lab.

# Leap files
Download sdk files from Leap website (only compatible with Python 2)
This project uses files from https://github.com/Cipulot/Leap-Motion-Python-3 and Python 3.7

Download relevant Leap script & required packages, modify csv file name to relevant path.

# Fusion files
Create an Add-In in fusion, edit and copy in code from relevant Fusion Add-In file and modify csv file name to relevent path.

# Gesture Instructions
2 Hand Orbit: Use 2 hands to navigate the model, with the distance between hands controlling the zoom and roll and yaw of the line connecting hands controlling roll and yaw of the model respectively.

1 Hand Roll:  Use 1 hands to navigate the model, with the vertical distance between hand and controller controlling the zoom and roll and yaw of the hand controlling roll and yaw of the model respectively.

Box, Cylinder and Sphere: When the Add-In is run, an initial shape is generated. Make a pinch gesture with both hands and the dimensions of the body will be controlled by the coordinates of the hand. Once the body is in the desired position, release the pinch gesture and the body will turn green. The Add-In will be terminated and can be run again to generate another body
