import multiprocessing

from streamer import Streamer
from detector import Detector
from show import Show


def main():
    streamer = Streamer("source/People - 6387 (2).mp4", "55555")
    detector = Detector("55555", "55556")
    show = Show("55556")

    p1 = multiprocessing.Process(target=streamer.stream, args=())
    p2 = multiprocessing.Process(target=detector.detect, args=())
    p3 = multiprocessing.Process(target=show.display, args=())

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.terminate()
    p3.terminate()
    p2.join()
    p3.join()

if __name__ == '__main__':
    main()