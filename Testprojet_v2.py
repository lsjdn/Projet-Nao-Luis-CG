#!/usr/include/python2.7
#coding=utf-8


import argparse
from naoqi import *
import time
import os
from ftplib import FTP
import string
#import speech_recognition as sr

robot_IP = "172.30.185.103" #ip du nao a mettre avant
robot_PORT= 9559


#def record_NAO(robot_IP, robot_PORT):
#connexion au robot
tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
record = ALProxy("ALAudioRecorder", robot_IP, robot_PORT)
channels = [1,0,0,0] #ne prend que le micro avant
ftp = FTP(robot_IP)
ftp.login('nao', 'stark') 
ftp.delete('record.wav')   	
#enregistrement
#TODO allumage des leds quand il lance l'enregistrement
tts.say("What do you want")    
record.startMicrophonesRecording("/home/nao/record.wav","wav",16000, channels)
record_path = '/home/nao/record.wav'
time.sleep(10)
record.stopMicrophonesRecording()
#print.stopMicrophonesRecording()
print 'record over'
tts.say("record over")


# transfert de document .wav a l'ordi
    	
#ftp.retrlines('LIST') pour voir la liste des fichiers 
ftp.retrbinary('RETR record.wav', open('record.wav', 'wb').write)
ftp.close()
r + sr.Recognizer()
#os.system("aplay record.wav") #joue l'enregistrement (programmer un oui/non et voir la qualité)
#speech to text
#with sr.WavFile("record.wav") as source:
#	audio = r.record(source)
#try:
#	print("Transcription: " +r.recognize(audio))
#except LookupError:
#	print("Could not understand audio")

