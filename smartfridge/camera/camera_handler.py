import io
import picamera


def take_picture():
    ''' triggers the Pi's camera and returns the images as bytes '''
    
    # create instance of PiCamera class
    camera = picamera.PiCamera()
    
    # flip camera, because it is mounted upside down
    camera.hflip = True
    camera.vflip = True

    # only for testing: take picture and save as jpg
    # camera.capture('image.jpg')

    # create stream using in-memory byte buffer
    stream = io.BytesIO()
    camera.capture(stream, 'jpeg')
    stream = stream.getbuffer()

    # only for testing: take bytes and save as jpg
    # fobj = open("byte_to_jpg.jpg", "wb")
    # fobj.write(stream)
    # fobj.close()
    
    return stream
