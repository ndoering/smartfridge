from camera import camera_handler as ch
from clarifai_connector import clarifai_connector as cc
import configuration_management as conf
import slack_connector as sc


if __name__ == "__main__":
    # slack stuff
    c = conf.Configuration()
    bot = sc.Slackbot(c)
    #bot.speak()


    # take picture (returns bytes)
    streambuffer = ch.take_picture()
    

    # call clarifai API
    print("Start classification.")
    clarifaiApp = c.config["CLARIFAI"]["APIKey"]
    model = c.config["CLARIFAI"]["Model"]
    print("App and Model loaded.")
    ccall = cc.ClarifaiCall(clarifaiApp, model, streambuffer)
    print(ccall.call()) # JSON response
