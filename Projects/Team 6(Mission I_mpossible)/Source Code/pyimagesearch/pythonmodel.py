import os
from pyimagesearch.centroidtracker import centroidTracker
from pyimagesearch.recognition import recognition
from moviepy.editor import *
import numpy as np
import cv2

class pythonModel:

	def __init__(self, loadFileName, saveFileName, userEmailPath):
		self.prototxt = 'model\\deploy.prototxt.txt'
		self.detectModel = 'model\\res10_300x300_ssd_iter_140000.caffemodel'
		self.threshold = 0.5
		self.userEmailPath = userEmailPath
		self.saveFileName = saveFileName
		self.videoPath = os.path.join(userEmailPath, 'temp\\'+loadFileName)
		self.recogModelPath = os.path.join(userEmailPath, "temp\\model\\"+saveFileName+'.xml')

	def process(self, videoPath):
		centTrac = centroidTracker()
		(H, W) = (None, None)

		net = cv2.dnn.readNetFromCaffe(self.prototxt, self.detectModel)

		vfaudio = VideoFileClip(self.videoPath).audio
		videoCapture = cv2.VideoCapture(self.videoPath)

		fcc = cv2.VideoWriter_fourcc(*'DIVX')
		fps = round(videoCapture.get(cv2.CAP_PROP_FPS), 2)
		outPath = os.path.join(os.path.join(self.userEmailPath, "temp"), self.videoPath.split('\\')[-1].split('.')[0]+'.avi')
		videoWriter = cv2.VideoWriter(outPath, fcc, fps,
			(int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))))


		recogModel = recognition(self.recogModelPath)
		while videoCapture.isOpened():
			ret, frame = videoCapture.read()
			if not ret:
				break
			if W is None or H is None:
				(H, W) = frame.shape[:2]

			blob = cv2.dnn.blobFromImage(frame, 1.0, (W, H),
										 (104.0, 177.0, 123.0))
			net.setInput(blob)
			detections = net.forward()
			rects = []

			for i in range(0, detections.shape[2]):
				if detections[0, 0, i, 2] > self.threshold:

					box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])

					(startX, startY, endX, endY) = box.astype("int")
					if startX > frame.shape[0] or endX > frame.shape[0] or startY > frame.shape[1] or endY > frame.shape[1]:
						continue
					rects.append(box.astype("int"))

			objects = centTrac.update(rects)
			for (_, coordinate) in objects.items():
				frame = recogModel.recognization(coordinate[0], coordinate[1], coordinate[2] - coordinate[0], coordinate[3] - coordinate[1], frame)


			videoWriter.write(frame)

		videoCapture.release()
		videoWriter.release()
		cv2.destroyAllWindows()

		videoFileClip = VideoFileClip(outPath)
		videoFileClip.audio = vfaudio
		videoFileClip.write_videofile(os.path.join(self.userEmailPath, os.path.join("video", self.saveFileName+'.mp4')))