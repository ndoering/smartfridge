from camera import camera_handler as ch
from clarifai_connector import clarifai_connector as cc
import sql_connector as dbcon
import configuration_management as conf
import slack_connector as sc
import cli_parser as cp
from datetime import datetime


if __name__ == "__main__":
    cliparser = cp.CliParser()

    # slack stuff
    c = conf.Configuration(cliparser.args.config)
    bot = sc.Slackbot(c)
    bot.speak()

    # take picture (returns bytes)
    streambuffer = ch.take_picture()

    # call clarifai API
    print("Start classification.")
    clarifaiApp = c.config["CLARIFAI"]["APIKey"]
    model = c.config["CLARIFAI"]["Model"]
    print("App and Model loaded.")
    ccall = cc.ClarifaiCall(clarifaiApp, model, streambuffer)
    print(ccall.call()) # JSON response

    # Database connection
    ## Load DB configuration from config.ini within module package
    c = conf.Configuration()
    host = c.config["MYSQL"]["Host"]
    user = c.config["MYSQL"]["User"]
    pw = c.config["MYSQL"]["Password"]
    dbc = c.config["MYSQL"]["Database"]
    ## Open database connection with Database Handle
    dbhdl = dbcon(host, user, pw, dbc)
    dbhdl.connect()

    # ToDo: Using the Clarifai, along with the buffered stream data as parameters to save it into the database.
    # capturetime, full_image, manual_labeled, note
    dbhdl.insert_fridgelog(datetime.now(), streambuffer, 0, "Pic from streambuffer")
    # fid, half_image, fruit_class, confidence, prediction, note
    dbhdl.insert_all_fruits(1, streambuffer, "T", 0.25, 0.65, "ha")