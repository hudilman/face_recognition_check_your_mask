import cv2
import winsound


face_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")
noseCascade = cv2.CascadeClassifier("./haarcascade/Nariz.xml")
mouth_cascade = cv2.CascadeClassifier('./haarcascade/haarcascade_mcs_mouth.xml')
bw_threshold = 80
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    img = cv2.flip(img,1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    #cv2.imshow('black_and_white', black_and_white)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)

    if(len(faces) == 0 and len(faces_bw) == 0):
        cv2.putText(img,'Tidak Ada Orang',(250,50),font,1,(255,0,0),2)
    else:
        for (x, y, w, h) in faces:
           
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
            
            nose_rects = noseCascade.detectMultiScale(gray, 1.5, 5)
            
        if(len(mouth_rects) == 0 and len(nose_rects) == 0):
            cv2.putText(img,'Menggunakan Masker',(170,50),font,1,(0,255,0),2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), 5)
        elif(len(mouth_rects) == 0 and len(nose_rects) != 0):
            cv2.putText(img,'Pengunaan Masker Salah',(150,50),font,1,(0, 255, 255),2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,255), 5)
        elif(len(mouth_rects) != 0 and len(nose_rects) == 0):
            cv2.putText(img,'Pengunaan Masker Salah',(150,50),font,1,(0, 251, 255),2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,255), 5)
        else:
            for (mx, my, mw, mh) in mouth_rects:
                if(y < my < y + h):
                    cv2.rectangle(img, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                    break
                    
            for (mx, my, mw, mh) in nose_rects:
                if(y < my < y + h):
                    cv2.rectangle(img, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                    break
                    
            cv2.putText(img,'Tidak Menggunakan Masker',(150,50),font,1,(0, 0, 255),2)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 5)
            duration = 1000  # milliseconds
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            

    cv2.imshow('Deteksi Masker', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()