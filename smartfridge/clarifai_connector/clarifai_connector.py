from clarifai.rest import ClarifaiApp

class ClarifaiCall():
    def __init__(self, key, model, imagebytes):
        # initialize clarifai app
        self.clarifaiApp = ClarifaiApp(api_key=key)
        # initialize trained model
        self.model = self.clarifaiApp.models.get(model)
        self.imagebytes = imagebytes


    def call(self):
        print("Classification response incoming:")
        # ask for JSON and display only label and prediction results
        return self.model.predict_by_bytes(self.imagebytes)['outputs'][0]['data']['concepts']



if __name__ == "__main__":
    pass
