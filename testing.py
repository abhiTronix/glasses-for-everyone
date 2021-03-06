import matplotlib.pyplot as plt
from imutils import face_utils
import numpy as np
import imutils
from scipy import misc
import pickle
import dlib
import cv2
import os

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

def haar_testing():
    img = cv2.imread('img/pos/170.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        print("face: x={}, y={}, w={}, h={}".format(x,y,w,h))
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

def dlib_testing():
    dlib_detector = dlib.get_frontal_face_detector()
    dlib_predictor = dlib.shape_predictor('src/dlib/shape_predictor_68_face_landmarks.dat')

    ## delet tis
    img_list_file = 'img/FDDB-folds/FDDB-fold-02.txt'
    with open(img_list_file, 'r') as f:
        file_list = [x.rstrip() for x in f.readlines()]

    ## and tis
    rectangle_file = 'img/FDDB-folds/FDDB-fold-02-rectangleList.pkl'
    with open(rectangle_file, 'rb') as f:
        face_list = pickle.load(f)

    index_num = 9
    image = cv2.imread('img/FDDB-pics/{}.jpg'.format(file_list[index_num]))
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # return
    faces = face_list[index_num]
    # round all face values to integers
    faces = [[int(round(x)) for x in face] for face in faces]

    # rects = []
    # for (x, y, w, h) in faces:
        # rect = dlib.rectangle(int(round(x)), int(round(y)), int(round(x+w)), int(round(y+h)))
        # rects.append(rect)
        # cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    # return

    # image = cv2.imread(args["image"])
    # image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rects = dlib_detector(gray, 1)

    # comparing face detectors
    clone = image.copy()
    for (x,y,w,h) in faces:
        cv2.rectangle(clone, (x,y), (x+w, y+h), (255,0,0), 1)
        # rect = dlib.rectangle(int(round(x)), int(round(y)), int(round(x+w)), int(round(y+h)))
        rect = dlib.rectangle(x, y, x+w, y+h)
        shape = dlib_predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        i, j = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
        (x1, y1, w1, h1) = cv2.boundingRect(np.array([shape[i:j]]))
        cv2.rectangle(clone, (x1,y1), (x1+w1, y1+h1), (255,0,0), 1)

    for rect in rects:
        cv2.rectangle(clone, (rect.left(), rect.top()), (rect.right(), rect.bottom()), (0,255,0), 1)
        shape = dlib_predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        i, j = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
        (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
        cv2.rectangle(clone, (x,y), (x+w, y+h), (0,255,0), 1)
    cv2.imshow("Image", clone)
    cv2.waitKey(0)
    return
    
    for (i, rect) in enumerate(rects):
        shape = dlib_predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        clone = image.copy()
        # NOTE: The right eye is the person's right eye, which appears as the left eye in photo
        i, j = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

        for (x, y) in shape[i:j]:
            cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)
            
        (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
        cv2.rectangle(clone, (x,y), (x+w, y+h), (0,255,0), 1)

        cv2.imshow("Image", clone)
        cv2.waitKey(0)
        return


        for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
            # clone the original image so we can draw on it, then
            # display the name of the face part on the image
            clone = image.copy()
            cv2.putText(clone, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 0, 255), 2)
     
            # loop over the subset of facial landmarks, drawing the
            # specific face part
            for (x, y) in shape[i:j]:
                cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)
            
            (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
            cv2.rectangle(clone, (x,y), (x+w, y+h), (0,255,0), 1)

            M = cv2.moments(shape[i:j])
            # print(M)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(clone, (cx, cy), 2, (0,255,0), 1)
            # print(x,y,w,h)
            roi = image[y:y + h, x:x + w]
            roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)
     
            # show the particular face part
            # cv2.imshow("ROI", roi)
            cv2.imshow("Image", clone)
            cv2.waitKey(0)
        
        # visualize all facial landmarks with a transparent overlay
        output = face_utils.visualize_facial_landmarks(image, shape)
        cv2.imshow("Image", output)
        cv2.waitKey(0)

    # print(rects[0][0])

# try detecting eyes only
# eyes = eye_cascade.detectMultiScale(gray)
# for (ex,ey,ew,eh) in eyes:
    # cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def pickle_eye_labels():
    lis = [[((207,153,20,14), (262,135,37,11))], [((79,80,18,7), (122,87,14,7)), ((171,125,9,4), (193,123,10,5)), ((315,113,17,8), (353,103,17,8))], [((121,70,15,8),(151,76,17,8))],
    [((81,94,14,7), (111,95,15,7)), ((271,58,14,8), (301,57,16,7))], [((111,169,32,15), (172,171,30,14))], [((105,162,37,13), (180,154,37,15))], [((111,182,50,20),(201,186,44,22))],
    [((118,67,16,6),(150,68,18,6))], [((105,96,20,9),(146,99,20,8)), ((253,85,17,7),(283,77,15,9))], [((198,102,22,10),(243,94,20,10))], [((185,122,23,9),(222,116,21,8))],
    [((137,154,30,14),(197,149,28,13))], [((151,94,26,12),(196,92,25,11))], [((81,146,31,18),(172,139,34,20))], [((82,185,42,17),(161,172,42,18))], [((154,130,30,10),(207,132,23,9))],
    [((102,111,27,12),(156,112,23,11))], [((186,95,16,10),(221,101,18,8))], [((115,97,19,9),(152,94,22,11))], [((114,112,23,12),(160,111,22,10))]]

    with open('img/manual/eye_labels.pkl', 'wb') as f:
        pickle.dump(lis, f)


if __name__ == "__main__":
    # dlib_testing()
    main()