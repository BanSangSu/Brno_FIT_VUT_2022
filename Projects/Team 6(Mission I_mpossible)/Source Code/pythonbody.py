import socket
import os
import threading
import datetime
from pyimagesearch import *

def serverStart(address, connect):

    print("Connect!")


    print("mail receive... ")
    # 이메일
    buffSize = 4096
    count = connect.recv(buffSize)
    userEmail = count.decode('utf-8')

    connect.send('ok'.encode('utf-8'))

    print(userEmail, end=' ')

    print("mail receive success!")

    ####################################################################################


    # 폴더 생성
    userEmailPath = os.path.join("C:\\Users\\leonilpark\\Documents\\Final_Project\\mosaic\\user\\", userEmail)
    if not os.path.isdir(userEmailPath):
        print("Make", userEmail, "directory")
        os.mkdir(userEmailPath)
        os.mkdir(os.path.join(userEmailPath, "video"))
        os.mkdir(os.path.join(userEmailPath, "temp"))
    else:
        print(userEmail, "directory exists")

    now = datetime.datetime.now()
    datetimeFileName = now.strftime('%y%m%d_%H%M%S')
    print("datetime", datetimeFileName)
    tempPath = os.path.join(userEmailPath, "temp\\")
    videoPath = os.path.join(userEmailPath, "video\\")

    ####################################################################################


    # 학습용 데이터
    buffSize = 1024
    lCount = connect.recv(buffSize)
    learnData = lCount.decode('utf-8')

    connect.send('ok'.encode('utf-8'))

    faceVideoName = 'L_' + datetimeFileName + '.mp4'

    for i in range(0, int(learnData)):
        video = connect.recv(1024)
        with open(os.path.join(tempPath, faceVideoName), "ab") as f:
            f.write(video)

    connect.send('ok'.encode('utf-8'))
    print("receive learn video")
    ####################################################################################

    # 처리용 데이터
    buffSize = 1024
    tCount = connect.recv(buffSize)

    connect.send('ok'.encode('utf-8'))
    processData = tCount.decode('utf-8')

    targetVideoName = 'T_' + datetimeFileName + '.mp4'

    for i in range(0, int(processData)):
        video = connect.recv(1024)
        with open(os.path.join(tempPath, targetVideoName), "ab") as f:
            f.write(video)

    connect.send('ok'.encode('utf-8'))
    print("receive target video")
    gatheringData = sampleGathering(os.path.join(tempPath, faceVideoName), tempPath, userEmail)
    gatheringData.videoCapture()
    recogModel = learnRecognition(tempPath)
    recogModel.process(tempPath, datetimeFileName)
    processModel = pythonModel(targetVideoName, datetimeFileName, userEmailPath)
    processModel.process(videoPath)
