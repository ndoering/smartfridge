from clarifai.rest import ClarifaiApp

class ClarifaiCall():
    def __init__(self, key, model, imagebytes):
        # initialize clarifai app
        self.clarifaiApp = ClarifaiApp(api_key=key)
        # initialize trained model
        self.model = self.clarifaiApp.models.get(model)
        self.imagebytes = imagebytes
        self.json = None


    def call(self):
        print("Classification response incoming:")
        # ask for JSON and display only label and prediction results
        self.json = self.model.predict_by_bytes(self.imagebytes)['outputs'][0]['data']['concepts']
        return self.json


if __name__ == "__main__":
    pass
