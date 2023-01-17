import cv2
import datetime
import ffmpeg
import logging


logging.basicConfig(level=logging.INFO, filemode='a', filename='log.log',
                    format='%(asctime)s %(levelname)s %(message)s')

VIDEO_LENGTH_SEC = 30 # пока не удалось избавиться от погрешности

cam_number = 0
cap = cv2.VideoCapture(cam_number)
logging.info(f'The camera value is set to {cam_number}')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

start = datetime.datetime.now()
end = start + datetime.timedelta(seconds=VIDEO_LENGTH_SEC)

while cap.isOpened() and end > datetime.datetime.now(): # программа выполняется, пока (1)работает соединение и (2)не кончилось установленное время
    ret, frame = cap.read()
    if ret == True:
        out.write(frame)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): # время записи может устанавливаться константой или прерываться с клавиатуры
            logging.info('The recording was stopped from the keyboard')
            break
    else:
        logging.error('Error by reading from the stream source')
        break

logging.info('The recording was finished successfully')
video = ffmpeg.input('output.avi')
video = video.trim(start=10, duration=10)
video = ffmpeg.output(video, 'output_cut.avi')
out, err = ffmpeg.run(video, quiet=True)
logging.info('ffmpeg stdout: %s', out.decode())
logging.info('ffmpeg stderr: %s', err.decode())

cap.release()
out.release()
cv2.destroyAllWindows()
