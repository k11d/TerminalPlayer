#!/usr/bin/env python3
import os, time
import cv2
import numpy as np
import itertools as it


MOVIE_EXTENSIONS = ['.mov', '.mp4', '.mkv', '.avi']
IMAGE_EXTENSIONS = ['.jpg', '.bmp', '.png', '.tiff']
FPS = 15.0
# _TMP_LOC = "/mnt/ram/tmp_#.jpg"
_TMP_LOC = "/tmp/tmp_#.jpg"
# os.system('/home/kid/bin/ramdisk.sh')


def image2ascii(fp=None):

    def G():
        while True:
            frame = yield
            if frame is None:
                print("Quitting")
                break
            tf = next(next_name)
            cv2.imwrite(tf, frame)
            _ = os.system(f"chafa --watch {tf}")
            # _ = os.system(f"rm {tf}")

    def gennames():
        while True:
            yield _TMP_LOC
        # for n in it.count(start=1):
            # yield _TMP_LOC.replace("#", str(n))



    next_name = gennames()
    g = G()
    g.send(None)
    if fp is None: return g
    else:
        if type(fp) == str:
            return g.send(cv2.imread(fp))
        elif type(fp) == np.ndarray:
            return g.send(fp)


def stream2ascii(fp, FPS=FPS):
    cap = cv2.VideoCapture(fp)
    ia = image2ascii()
    t0 = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ia.send(frame)
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        dt_left = max(1.0, (1.0 / FPS) - dt)
        time.sleep(dt_left)


def main(*args):
    ia = image2ascii()
    for elem in args[0]:
        try:
            if os.path.splitext(elem)[1].lower() in MOVIE_EXTENSIONS or elem.startswith('/dev'):
                stream2ascii(elem)
            if os.path.splitext(elem)[1].lower() in IMAGE_EXTENSIONS:
                ia.send(elem)
        except KeyboardInterrupt:
            for f in (os.path.join(os.path.dirname(_TMP_LOC), _f) for _f in os.listdir(os.path.dirname(_TMP_LOC))):
                print(f"Cleaning: {f}")
                os.remove(f)
            break
    return 0



if __name__=='__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
