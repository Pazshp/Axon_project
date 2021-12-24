import cv2
import imagezmq
import numpy
import time

class Streamer:
    def __init__(self, video_path, send_port="55555"):
        self.video_path = video_path
        self.send_port = send_port

    def validate_path(self):
        video_capture = cv2.VideoCapture(self.video_path)
        if not video_capture.isOpened():
            video_capture.release()
            return False
        return True

    def stream(self):
        video_capture = cv2.VideoCapture(self.video_path)

        sender = imagezmq.ImageSender(connect_to='tcp://*:' + self.send_port, REQ_REP=False)



        while True:
            flag, frame = video_capture.read()

            if not flag:
                self.quit(video_capture, sender)
                return False

            sender.send_image("", frame)

    def quit(self, video_capture, sender):
        frame = numpy.zeros(1)
        sender.send_image("quit", frame)
        video_capture.release()


