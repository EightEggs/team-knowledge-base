import numpy as np
import cv2


class Sketcher:
    __slots__ = ('prev_pt', 'windowname', 'dests')

    def __init__(self, windowname, dests):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.show()
        cv2.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv2.imshow(self.windowname, self.dests[0])

    def on_mouse(self, event, x, y, flags, params):
        pt = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv2.EVENT_LBUTTONUP:
            self.prev_pt = None
        if self.prev_pt and flags and cv2.EVENT_FLAG_LBUTTON:
            for dst in self.dests:
                cv2.line(dst, self.prev_pt, pt, (255, 64, 64), 14)
            self.prev_pt = pt
            self.show()


def main(filename):
    img = cv2.imread(filename)
    if type(img) != np.ndarray:
        return
    img_copy = img.copy()
    mask = np.zeros(img.shape[:2], np.uint8)

    sketch = Sketcher('image', [img, mask])
    while True:
        ch = cv2.waitKey()
        if ch == ord('q'):
            break
        if ch == ord('o'):
            res = cv2.inpaint(img, mask, inpaintRadius=8, flags=cv2.INPAINT_NS)
            cv2.imshow('output', res)
        if ch == ord('r'):
            img[:] = img_copy
            mask[:] = 0
            sketch.show()


if __name__ == '__main__':
    print('-'*10, 'INSTRUCTION', '-'*10)
    print('mouse left: draw\tq: quit\no: output\t\tr: reset')
    print('-'*33)
    file = input("Input the image file's name: ")
    main(file)
    cv2.destroyAllWindows()
