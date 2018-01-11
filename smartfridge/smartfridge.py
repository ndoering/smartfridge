from clarifai_connector import clarifai_connector as cc
import configuration_management as conf
import slack_connector as sc




if __name__ == "__main__":
    c = conf.Configuration()
    bot = sc.Slackbot(c)
    bot.speak()

    # call clarifai API
    print("Start classification.")
    clarifaiApp = c.config["CLARIFAI"]["APIKey"]
    model = c.config["CLARIFAI"]["Model"]
    print("App and Model loaded.")
    ccall = cc.ClarifaiCall(clarifaiApp, model)
    ccall.call()
