import cv2
import numpy as np
import os, glob


class learnRecognition:

    def __init__(self, tempDirPath):
        self.trainData, self.trainLabels = [], []
        self.dirs = [d for d in glob.glob(os.path.join(tempDirPath, "gathering")) if os.path.isdir(d)]
        self.id = 0

    def process(self, tempDirPath, datetimeFileName):
        modelFile = open(os.path.join(tempDirPath, 'model\\'+datetimeFileName+'.xml'), 'w')
        modelFile.close()

        for dir in self.dirs: # data import processing
            files = glob.glob(dir + '/*.jpg')
            for file in files:
                img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
                self.trainData.append(np.asarray(img, dtype=np.uint8))
                self.trainLabels.append(self.id)

        # model learning processing
        trainData = np.asarray(self.trainData)
        trainLabels = np.int32(self.trainLabels)

        model = cv2.face.LBPHFaceRecognizer_create()
        model.train(trainData, trainLabels)
        model.write(os.path.join(tempDirPath, 'model\\'+datetimeFileName+'.xml'))