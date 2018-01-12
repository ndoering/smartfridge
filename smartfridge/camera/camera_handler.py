import picamera

# create instance of PiCamera class
camera = picamera.PiCamera()

# flip camera, because it is mounted upside down
camera.hflip = True
camera.vflip = True

# take a picture
camera.capture('image.jpg')
