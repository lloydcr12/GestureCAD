import Leap
import sys, time, math, csv


class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        hands = frame.hands
        numHands = len(hands)

        if numHands == 2:
            # Get the first hand
            hand1 = hands[0]
            hand2 = hands[1]


            # Get the palm position
            palm1 = hand1.palm_position
            palm2 = hand2.palm_position
            x1 = palm1[0]
            y1 = palm1[1]
            x2 = palm2[0]
            y2 = palm2[1]
            z1 = palm1[2]
            z2 = palm2[2]

            # Get the grab strength, closed fist = 1, open fist = 0
            strength1 = hand1.grab_strength
            strength2 = hand2.grab_strength

            # Angles of line connecting palms with respect to Leap device's coordinate system
            rollangle = math.tan(-(y2-y1)/(x2-x1))
            yawangle = math.tan(-(z2-z1)/(x2-x1))

            # Distance between palms for zoom
            PalmDiff = palm1 - palm2
            PalmDistSquare = PalmDiff[0]**2 + PalmDiff[1]**2 + PalmDiff[2]**2
            PalmDist = math.sqrt(PalmDistSquare)

            # Stop updating csv if fists are closed >50%
            if strength1 < 0.5 or strength2 < 0.5:

                # print("Palm 1 position:", palm1, "Palm 2 Position:", palm2, "Palm Diff:", PalmDiff, "Palm Dist:", PalmDist)
                print("Roll:", rollangle * Leap.RAD_TO_DEG, "Yaw:", yawangle,"Palm Dist:", PalmDist)

                time.sleep(0.05)
                # write parameters to csv
                with open('D:\Source\LeapPython37\handroll.csv', 'w') as file:
                    fieldnames = ['Roll', 'Yaw', 'Zoom']
                    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

                    csv_writer.writeheader()
                    csv_writer.writerow({'Roll': rollangle, 'Yaw': yawangle, 'Zoom': PalmDist})


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
