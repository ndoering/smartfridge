# from camera import camera_handler as ch # TO DO: use this line in production
from clarifai_connector import clarifai_connector as cc
import sql_connector as dbcon
import configuration_management as conf
import io # TO DO: delete this import in production if not needed 
import slack_connector as sc
import cli_parser as cp
from datetime import datetime


if __name__ == "__main__":
    cliparser = cp.CliParser()

    ### SLACK ##################################################################
    c = conf.Configuration(cliparser.args.config)

    bot = sc.Slackbot(c)
	print("Slackbot initialized.")
    #bot.speak()


    ### CAMERA #################################################################
    # take picture (returns bytes)
    # streamvalue = ch.take_picture() TO DO: use this line in production
    #############################################
    # the following generates a dummy bytefile for testing
    # as the above only works on a RaspberryPi with camera
    with open("test.jpg", "rb") as imagefile:
        f = imagefile.read()
        streambuffer = io.BytesIO(f).getbuffer()
    #############################################
    print("Photo shot.")


    ### PIPELINE ###############################################################
    # TO DO


    ### CLARIFAI ###############################################################
    print("Start classification.")
    clarifaiApp = c.config["CLARIFAI"]["APIKey"]
    model = c.config["CLARIFAI"]["Model"]
    print("App and Model loaded.")
    # instantiate Clarifai object
    ccall = cc.ClarifaiCall(clarifaiApp, model, streamvalue)
    # call clarifai API
    ccall.call()
    print(ccall.json) # JSON response
	bot.compute_message(ccall.json)


    ### DATABASE ###############################################################
    ## Load DB configuration from config.ini within module package
    c = conf.Configuration()
    host = c.config["MYSQL"]["Host"]
    user = c.config["MYSQL"]["User"]
    pw = c.config["MYSQL"]["Password"]
    dbc = c.config["MYSQL"]["Database"]
    ## Open database connection with Database Handle
    dbhdl = dbcon.MySQLConnector(host, user, pw, dbc)
    dbhdl.connect()

    #dbhdl.drop_tables()
    #dbhdl.db_create_tables()

    # create entry in fridgelog for whole image
    data = (streamvalue, 'note')
    #data = ('NULL', 'note')
    dbhdl.insert_fridgelog(data)

    # create entry in all_fruits for each detected fruit status
    dbhdl.insert_all_fruits(ccall.json)

