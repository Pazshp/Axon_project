import cv2
import imagezmq
import datetime


class Show:
    def __init__(self, receive_port="55556"):
        self.receive_port = receive_port

    def display(self):
        receiver = imagezmq.ImageHub(open_port='tcp://127.0.0.1:' + self.receive_port, REQ_REP=False)

        while True:
            rectangle_list, frame = receiver.recv_image()

            if "quit" in rectangle_list:
                self.quit()
                return False

            blurred_frame = cv2.blur(frame, (10, 10))
            for rectangle in rectangle_list:
                cv2.rectangle(frame, rectangle[0], rectangle[1], (0, 255, 0), 2)
                y1, x1 = rectangle[0]
                y2, x2 = rectangle[1]
                frame[x1:x2, y1:y2] = blurred_frame[x1:x2, y1:y2]

            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 0, 0), 1)

            cv2.imshow("Security Feed", frame)
            cv2.waitKey(33)  # no time to implement fps detection - made for most common videos 30 fps

    def quit(self):
        cv2.destroyAllWindows()
