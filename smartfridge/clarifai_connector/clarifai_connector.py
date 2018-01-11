from clarifai.rest import ClarifaiApp

class ClarifaiCall():
    def __init__(self, key, model):
        # initialize clarifai app
        self.clarifaiApp = ClarifaiApp(api_key=key)
        # initialize trained model
        self.model = self.clarifaiApp.models.get(model)


    def call(self):
        print("Classification response incoming:")
        # ask for JSON and display only label and prediction results
        print(self.model.predict_by_filename('2017-12-06-1000.jpg')['outputs'][0]['data']['concepts'])



if __name__ == "__main__":
    pass
