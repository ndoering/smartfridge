import cv2 as c


class PipelineStage(object):
    def __init__(self):
        self.id = None

    def process(self, image):
        return image


class DummyStage(PipelineStage):
    def __init__(self):
        super()
        self.desc = 'Dummy image pipeline stage'

    def process(self, image):
        return image


class GreyScaleStage(PipelineStage):
    def __init__(self):
        super()
        self.desc = 'Greyscale image pipeline stage'

    def process(self, image):
        img = c.imread(image)

        processedImg = c.cvtColor(img, c.BGR2GRAY)
        
        return processedImg


pipelineTypes = {
    'dummy': DummyStage,
    'greyscale': GreyScaleStage,
}


def createStage(stageName):
    return pipelineTypes[stageName]()


class Pipeline(object):
    def __init__(self, stagesList):
        self.stages = []
        for stage in stagesList:
            self.stages.append(createStage(stage))

    def addStage(self, stage):
        self.stages.append(createStage(stage))

    def describe(self):
        for stage in self.stages:
            print(stage.desc)

    def process(self, image):
        curImage = image

        for stage in self.stages:
            curImage = stage.process(curImage)

        return curImage


if __name__ == '__main__':
    stageList = ('dummy', 'greyscale', 'dummy')
    pipeline = Pipeline(stageList)
    pipeline.addStage('greyscale')

    pipeline.describe()
    
