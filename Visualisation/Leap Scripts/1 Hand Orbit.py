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

        if numHands == 1:
            # Get the first hand
            hand1 = hands[0]


            # Get the palm position
            palm1 = hand1.palm_position
            x1 = palm1[0]
            y1 = palm1[1]
            z1 = palm1[2]

            # Get the grab strength, closed fist = 1, open fist = 0
            strength1 = hand1.grab_strength

            normal = hand1.palm_normal
            direction = hand1.direction


            rollangle = -normal.roll
            yawangle = -direction.yaw


            PalmDist = -5*y1 + 1000

            # Stop updating csv if fists are closed >50%
            if strength1 < 0.5:

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
