import Leap
import sys, time, math, csv
from Leap import CircleGesture


class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        hands = frame.hands
        numHands = len(hands)
        # print("Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d" % (
        #     frame.id, frame.timestamp, numHands, len(frame.fingers), len(frame.tools)))

        if numHands > 1:
            # Get the first hand
            hand1 = hands[0]
            hand2 = hands[1]

            # index finger as 'pointable'
            pointable1 = hand1.pointables[1]
            pointable2 = hand2.pointables[1]

            # # Get the index finger position
            palm1 = pointable1.tip_position
            x1 = palm1[0]
            y1 = palm1[1]
            z1 = palm1[2]
            palm2 = pointable2.tip_position
            x2 = palm2[0]
            y2 = palm2[1]
            z2 = palm2[2]

            PalmDiff = palm1 - palm2
            PalmDistSquare = PalmDiff[0]**2 + PalmDiff[2]**2 #only x and z
            PalmDist = math.sqrt(PalmDistSquare)

            strength1 = hand1.pinch_strength
            strength2 = hand2.pinch_strength

            circle = len(frame.gestures())


            # direction = hand1.direction
            time.sleep(0.05)
            print("circle:", circle, x1, y1, z1, x2, y2, z2, strength2, strength2, PalmDist)
            
            with open('D:\Source\LeapPython37\handscoords.csv', 'w') as file:
                fieldnames = ['x1', 'y1', 'z1', 'x2', 'y2', 'z2', 's1', 's2', 'Circle', 'Dist']
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

                csv_writer.writeheader()
                csv_writer.writerow({'x1': x1, 'y1': y1, 'z1': z1, 'x2': x2, 'y2': y2, 'z2': z2, 's1': strength1, 's2': strength2, 'Circle': circle, 'Dist': PalmDist})

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
