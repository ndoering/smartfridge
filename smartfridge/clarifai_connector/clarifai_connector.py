import configparser

from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

if __name__ == "__main__":
    print("Start classification.")

    # TODO: call APIKey over ini file
    app = ClarifaiApp(api_key='b9a2de7676aa4fadb74a5c59ea15ecba')

    # initialize the trained clarifai model
    model = app.models.get('smartfridge')
    # pass filename of image to be predicted
    response = model.predict_by_filename('2017-12-06-1000.jpg')

    # prints the data for the defined concepts of the model
    print(response['outputs'][0]['data']['concepts'])
