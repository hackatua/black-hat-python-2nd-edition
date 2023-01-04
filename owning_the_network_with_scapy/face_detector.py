import cv2
import os
import sys

# wget http://eclecti.cc/files/2008/03/haarcascade_frontalface_alt.xml

ROOT = '.'
FACES = '.'
TRAIN_XML = 'haarcascade_frontalface_alt.xml'

def detect(src_dir=ROOT, tgt_dir=FACES, train_xml=TRAIN_XML):
    for fname in os.listdir(src_dir):
        if (
            not fname.upper().endswith('.JPG') and
            not fname.upper().endswith('.JPEG')
        ):
            continue
        fullname = os.path.join(src_dir, fname)
        newname = os.path.join(tgt_dir, f'faces_{fname}')

        img = cv2.imread(fullname)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        training = os.path.join(train_xml)
        cascade = cv2.CascadeClassifier(training)
        rects = cascade.detectMultiScale(gray, 1.3, 5)
        try:
            if rects.any:
                print('Got a face!')
                rects[:, 2:] += rects[:, :2]
        except AttributeError:
            print(f'No faces found in {fname}.')
            continue

        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)

        cv2.imwrite(newname, img)

def main():
    (src_dir, tgt_dir, train_xml) = (
        sys.argv[1], sys.argv[2], sys.argv[3]
    )
    detect(src_dir, tgt_dir, train_xml)

if __name__ == '__main__':
    main()