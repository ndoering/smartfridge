# from camera import camera_handler as ch
from clarifai_connector import clarifai_connector as cc
import configuration_management as conf
import io
import slack_connector as sc


if __name__ == "__main__":
    # slack stuff
    c = conf.Configuration()
    bot = sc.Slackbot(c)
    print("Slackbot initialized.")
    #bot.speak()


    # take picture (returns bytes)
    # streambuffer = ch.take_picture() # TO DO: use this line in production
    #############################################
    # the following generates a dummy bytefile for testing
    # as the above only works on a RaspberryPi with camera
    with open("test.jpg", "rb") as imagefile:
        f = imagefile.read()
        streambuffer = io.BytesIO(f).getbuffer()
    #############################################
    print("Photo shot.")


    # call clarifai API
    print("Start classification.")
    clarifaiApp = c.config["CLARIFAI"]["APIKey"]
    model = c.config["CLARIFAI"]["Model"]
    print("App and Model loaded.")
    ccall = cc.ClarifaiCall(clarifaiApp, model, streambuffer)
    clarifai_response = ccall.call() # JSON response


    bot.compute_message(clarifai_response)
