import os
import cv2
import datetime
import ffmpeg
import logging


logging.basicConfig(level=logging.INFO, filemode='a', filename='log.log',
                    format='%(asctime)s %(levelname)s %(message)s')


def trim(in_file, out_file, start, end):
    if os.path.exists(out_file):
        os.remove(out_file)

    input_stream = ffmpeg.input(in_file)
    
    pts = 'PTS-STARTPTS'
    video = input_stream.trim(start=start, end=end).setpts(pts)
    audio = (input_stream
             .filter_('atrim', start=start, end=end)
             .filter_('asetpts', pts))
    video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
    output = ffmpeg.output(video_and_audio, out_file) # format=?
    out, err = output.run()

    logging.info('ffmpeg_trim stdout: %s', out.decode())
    logging.info('ffmpeg_trim stderr: %s', err.decode())


def convert(in_file):
    name, ext = os.path.splitext(in_file)
    out_name = name + '.mp4'
    out, err = ffmpeg.input(in_file).output(out_name).run()

    logging.info('ffmpeg_convert stdout: %s', out.decode())
    logging.info('ffmpeg_convert stderr: %s', err.decode())
    

def record_from_cam(cam_number, out_file, vid_length = 1000000000000): # default value для vid_length
    cap = cv2.VideoCapture(cam_number)
    logging.info(f'The camera value is set to {cam_number}')
    logging.info('The recording has started')
    
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('temp.avi', fourcc, 25, (640,480))

#    start = datetime.datetime.now()
#    end = start + datetime.timedelta(seconds=vid_length)

# and end > datetime.datetime.now()

    while cap.isOpened(): # программа выполняется, пока (1)работает соединение и (2)не кончилось установленное время
        ret, frame = cap.read()
        if ret == True:
            out.write(frame)

            cv2.imshow('video', frame)

            if cv2.waitKey(1) & 0xFF == 27: # время записи может устанавливаться аргументом или прерываться с клавиатуры
                logging.info('The recording was stopped from the keyboard')
                break
        else:
            logging.error('Error by reading from the stream source')
            break

    logging.info('The recording was finished successfully')

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    os.system('start cmd_.bat')
    record_from_cam(0, 'ouput.avi') # Запустить камеру и начать запись 30-секундного видео (имеется погрешность)
    os.system('ffmpeg -i temp.avi -i temp.wav -strict -2 -f avi ' + 'result.avi')  # ffmpeg для слияния
    os.remove('temp.avi') # Удалить промежуточный видеофайл
    os.remove('temp.wav') # Удалить промежуточный аудиофайл