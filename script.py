import datetime
import cv2

VIDEO_LENGTH = 30  # пока не удалось избавиться от погрешности

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

start = datetime.datetime.now()
end = start + datetime.timedelta(seconds=VIDEO_LENGTH)

while cap.isOpened() and end > datetime.datetime.now(): # программа выполняется, пока работает соединение
    ret, frame = cap.read()
    if ret == True:
        out.write(frame)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


cap.release()
out.release()
cv2.destroyAllWindows()