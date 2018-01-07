#NAO sound recording avec ALAudioRecorder

import argparse
from naoqi import ALProxy
import time
import os

robot_IP = "XXX.XXX.X.XXX"
tts = audio = record = aup = None

def record_NAO(robot_IP, robot_PORT= XXXX):
    global tts, audio, record, aup
    #connexion au robot
    tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
    record = ALProxy("ALAudioRecorder", robot_IP, robot_PORT)
    #enregistrement
    record.stopMicrophonrdRecording()
    print 'start recordng...'
    tts.say("start recording...")
    record_path = '/home/nao/record.wav'
    record.startMicrophonesRecording(record_path, 'wav', 16000, (0,0,1,0))
    time.sleep(4)
    record.stopMicrophonesRecording()
    print.stopMicrophonesRecording()
    print 'record over'
    tts.say("record over")
    return
