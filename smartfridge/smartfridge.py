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
    #bot.speak()

    # take picture (returns bytes)
    streamvalue = ch.take_picture()

    '''
    # call clarifai API
    print("Start classification.")
    clarifaiApp = c.config["CLARIFAI"]["APIKey"]
    model = c.config["CLARIFAI"]["Model"]
    print("App and Model loaded.")
    ccall = cc.ClarifaiCall(clarifaiApp, model, streambuffer)
    print(ccall.call()) # JSON response
    '''

    # Database connection
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

    # data = (streamvalue, 4, 'streamed')
    data = ('NULL', 4, 'streamed')
    dbhdl.insert_fridgelog(data)

    foreign_key = dbhdl.retrieve("MAX(fid)", "fridgelog")[0][0]
    data = (foreign_key, 'NULL', 1, 0.6, 0.5, 'this is a note')
    dbhdl.insert_all_fruits(data)
