import Leap, sys, threading, time, pickle
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
#listener interacts with Leap
class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb','Index','Middle','Ring','Pinky']
    bone_names = ['Metacarpal','Proximal','Intermediate','Distal']
    state_names = ['STATE_INVALID','STATE_START','START_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print("Motion Sensor Connected")

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE); #note semicolon end for gestures
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller): #290fps leap data
        frame = controller.frame()

        """print " Frame ID: " + str(frame.id) \
            + " Timestamp: " + str(frame.timestamp) \
            + " # of Hands: " + str(len(frame.hands)) \
            + " # of Fingers: " + str(len(frame.fingers)) \
            + " # of Tools: " + str(len(frame.tools)) \
            + " # of Gestures: " + str(len(frame.gestures()))"""
        
        for hand in frame.hands:
            handType = "Left Hand" if hand.is_left else "Right Hand"

            """print handType + " Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)"""

            normal = hand.palm_normal
            direction = hand.direction

            print "Pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) \
                + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG) \
                + " Yaw: " + str(direction.yaw * Leap.RAD_TO_DEG) \

            """with open("file.pickle", mode="wb") as fileObj:
                pickle.dump(direction.pitch * Leap.RAD_TO_DEG, fileObj, protocol=2)"""
            

            if normal.roll * Leap.RAD_TO_DEG < -30:
                filename = 'D:\Source\LeapPython3\GUI_outcome.csv'
                f = open(filename, 'w')
                f.write('13')

                print "ROLL RIGHT"

            if normal.roll * Leap.RAD_TO_DEG > 30:
                filename = 'D:\Source\LeapPython3\GUI_outcome.csv'
                f = open(filename, 'w')
                f.write('12')

                print "ROLL LEFT"
            
            if direction.pitch * Leap.RAD_TO_DEG < -15:
                filename = 'D:\Source\LeapPython3\GUI_outcome.csv'
                f = open(filename, 'w')
                f.write('9')

                print "PITCH DOWN"

            if direction.pitch * Leap.RAD_TO_DEG > 30:
                filename = 'D:\Source\LeapPython3\GUI_outcome.csv'
                f = open(filename, 'w')
                f.write('8')

                print "PITCH UP"
            
            if direction.yaw * Leap.RAD_TO_DEG < -15:
                filename = 'D:\Source\LeapPython3\GUI_outcome.csv'
                f = open(filename, 'w')
                f.write('11')

                print "YAW LEFT"

            if direction.yaw * Leap.RAD_TO_DEG > 15:
                filename = 'D:\Source\LeapPython3\GUI_outcome.csv'
                f = open(filename, 'w')
                f.write('10')

                print "YAW RIGHT"
            


            

            

            """arm = hand.arm
            print "Arm Direction: " + str(arm.direction) \
                + " Wrist Position: " + str(arm.wrist_position) \
                + " Elbow Position: " + str(arm.elbow_position)"""

            """for finger in hand.fingers:  #convert finger number to name from list
                print "Type: " + self.finger_names[finger.type()]
                + " ID: " + str(finger.id) + " Length: " + str(finger.length) + " Width: " + str(finger.width)

                for b in range(0, 4):
                    bone = finger.bone(b)
                    print "Bone: " + self.bone_names[bone.type] + " Start: " + str(bone.prev_joint) + " End: " + str(bone.next_joint) + " Direction: " + str(bone.direction)"""



def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()
    
    controller.add_listener(listener)

    print "Press enter to quit"
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__== "__main__":
    main()
