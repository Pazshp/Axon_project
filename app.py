import multiprocessing

from streamer import Streamer
from detector import Detector
from show import Show


def main():
    streamer = Streamer("source/People - 6387 (2).mp4", "55555")
    if not streamer.validate_path():
        print("wrong video path")
    else:
        detector = Detector("55555", "55556")
        show = Show("55556")

        p3 = multiprocessing.Process(target=show.display, args=())
        p2 = multiprocessing.Process(target=detector.detect, args=())
        p1 = multiprocessing.Process(target=streamer.stream, args=())

        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()

    print("finished")

if __name__ == '__main__':
    main()