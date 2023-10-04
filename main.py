import cv2
import pickle
import cvzone
import numpy as np
import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('./parking-system-365621-firebase-adminsdk-zu6ae-821ee276c5.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://parking-system-365621-default-rtdb.firebaseio.com'
})

ref = db.reference('/')

cap = cv2.VideoCapture('carPark.mp4')
width, height = 103, 43
with open('CarCoordinates', 'rb') as f:
    posList = pickle.load(f)


def empty(a):
    pass


cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 240)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)

freelist = []


def checkSpaces():
    spaces = 0
    marker = 1
    freelist.clear()
    print(posList)

    for pos in posList:
        print(pos)
        pts = np.array(pos)
        rect = cv2.boundingRect(pts)
        x, y, w, h = rect
        imgCrop = img[y:y + h, x:x + w].copy()
        ## (2) make mask
        pts = pts - pts.min(axis=0)

        mask = np.zeros(imgCrop.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
        dst = cv2.bitwise_and(imgCrop, imgCrop, mask=mask)
        dimensions = dst.shape

        # height, width, number of channels in image
        height = dst.shape[0]
        width = dst.shape[1]
        imgCrop = imgThres[dst]

        count = cv2.countNonZero(imgCrop)/(width*height)
        #cv2.imshow(str(x*y), imgCrop)
        #count = cv2.countNonZero(dst)

        #count = 0
        if count > 550:
            color = (0, 200, 0)
            thic = 5
            spaces += 1
            freelist.append({'slot': marker, 'state': "free"})

        else:
            color = (0, 0, 200)
            thic = 2
            freelist.append({'slot': marker, 'state': "occupied"})

        #cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)

        # Parking Lot Position Display
        cv2.putText(img, str(marker), (x + w - 50, y + h - 10), cv2.FONT_HERSHEY_PLAIN, 2,
                    (200, 0, 0), 2)

        # Parking Lot Fill Rate Display
        cv2.putText(img, str(int(count)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                    color, 2)

        marker = marker + 1

    #cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20,
                       #colorR=(0, 200, 0))


while True:

    # Get image frame
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    # img = cv2.imread('img.png')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    # ret, imgThres = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY)

    val1 = cv2.getTrackbarPos("Val1", "Vals")
    val2 = cv2.getTrackbarPos("Val2", "Vals")
    val3 = cv2.getTrackbarPos("Val3", "Vals")
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)

    checkSpaces()
    # Display Output
    ref.set({
        'occupancy': freelist
    })

    print(freelist)

    cv2.imshow("Image", imgThres)
    cv2.imshow("Image2", img)
    # cv2.imshow("ImageGray", imgThres)
    # cv2.imshow("ImageBlur", imgBlur)
    key = cv2.waitKey(1)
    if key == ord('r'):
        pass
