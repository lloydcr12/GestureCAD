import Leap, sys, threading, time
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
        
        for hand in frame.hands:
            handType = "Left Hand" if hand.is_left else "Right Hand"

            print handType + " Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)

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
