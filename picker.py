import cv2
import pickle

width, height = 107, 48


def updateImg(xyList):
    for box in xyList:
        cv2.line(img, box[0], box[1], (255, 0, 0), 1)
        cv2.line(img, box[1], box[2], (255, 0, 0), 1)
        cv2.line(img, box[2], box[3], (255, 0, 0), 1)
        cv2.line(img, box[3], box[0], (255, 0, 0), 1)


try:
    with open('CarCoordinates', 'rb') as file:
        xyList = pickle.load(file)
        print(xyList)
except:
    xyList = []

singlePosition = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        singlePosition.append([x, y])
        print(len(singlePosition))

        if len(singlePosition) % 4 == 0:
            xyList.append([singlePosition.pop(), singlePosition.pop(), singlePosition.pop(), singlePosition.pop()])
            print(xyList, 9238190)
            with open('CarCoordinates', 'wb') as file:
                pickle.dump(xyList, file)
            singlePosition.clear()
            print(xyList)

    if events == cv2.EVENT_RBUTTONDOWN and len(singlePosition) == 0:
        xyList.pop()
        with open('CarCoordinates', 'wb') as file:
            pickle.dump(xyList, file)


img = cv2.imread('carParkImg.png')
while True:
    cv2.imshow("Image", img)
    updateImg(xyList)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
