import cv2
import imagezmq
import datetime

class Show:
    def __init__(self, receive_port="55555"):
        self.receive_port = receive_port

    def display(self):
        receiver = imagezmq.ImageHub(open_port='tcp://127.0.0.1:' + self.receive_port, REQ_REP=False)

        while True:
            msg, frame = receiver.recv_image()

            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 0, 0), 1)

            cv2.imshow("Security Feed", frame)
            cv2.waitKey(100)

    def quit(self):
        pass
