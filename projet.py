#!/usr/include/python2.7
#coding=utf-8

import mysql.connector
import requests
#from luis_sdk import LUISClient


import argparse
from naoqi import *
import time
import os
from ftplib import FTP
import string
import speech_recognition as sr

import types
import urllib
import json

robot_IP = "172.30.185.102" #ip du nao a mettre avant
robot_PORT= 9559


#connexion au robot
tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
record = ALProxy("ALAudioRecorder", robot_IP, robot_PORT)
channels = [1,0,0,0] #ne prend que le micro avant
ftp = FTP(robot_IP)
ftp.login('nao', 'lannister') 
ftp.delete('record.wav')   	
#enregistrement
#TODO allumage des leds quand il lance l'enregistrement
tts.say("What do you want")    
record.startMicrophonesRecording("/home/nao/record.wav","wav",16000, channels)
record_path = '/home/nao/record.wav'
time.sleep(6)
record.stopMicrophonesRecording()
print 'record over'
tts.say("record over")


# transfert de document .wav a l'ordi
    	
#ftp.retrlines('LIST') pour voir la liste des fichiers 
ftp.retrbinary('RETR record.wav', open('record.wav', 'wb').write)
ftp.close()
#speech to text
r = sr.Recognizer()
with sr.AudioFile("record.wav") as source:
	audio = r.record(source)
	sptote = r.recognize_google(audio)
try:
	print("I think you said " + sptote)
except sr.UnknownValueError:
	print("I could not understand audio")
except sr.RequestError as e:
	print("I Could not request results from Google Speech Recognition service; {0}".format(e))
#TODO joue ce que sors le speech to text
verif = str(sptote)

#verif oui/non
ftp = FTP(robot_IP)
ftp.login('nao', 'lannister') 
ftp.delete('verif.wav')
tts.say("Did you say " + verif)
record.startMicrophonesRecording("/home/nao/verif.wav","wav",16000, channels)
record_path = '/home/nao/verif.wav'
time.sleep(3)
record.stopMicrophonesRecording()
ftp.retrbinary('RETR verif.wav', open('verif.wav', 'wb').write)
ftp.close()
with sr.AudioFile("verif.wav") as source:
	audio = r.record(source)
	yeno = str(r.recognize_google(audio))
if yeno == "yes":
	#send a Luis
	tts.say("Sending to Luis")

	# Get the dataflow from URL
	'''
	def URL_GetData(url):

	    try:

		ReplyData = urllib.urlopen(url).read()



		return ReplyData

	    

	    except Exception, e:

		print e


	# Put what we get from the LUIS app in a JSON file

	def JSON_Write(data):

	    file = open("reply.json", "w")

	    file.write(data)

	    file.close


	# Find out the top scoring intent and entity, and print out

	res = r.json()

	#recoginize entities
	lastname = res["entities"][0]['entity']
	#print lastname

	e_mail = res["entities"][1]['entity']

	firstname = res["entities"][2]['entity']
	#print firstname

	def JSON_Parse(data):

	    dataflow = json.loads(data)
	    
	    # Attention: if any of needed datas cannot be found, the program will return an error
	    #try : 
		#print "Intent: " + dataflow['topScoringIntent']['intent']
		#print "Entities :"
	    	#print dataflow['entities'][0]['type'] + " : " + dataflow['entities'][0]['entity']
	    	#print dataflow['entities'][1]['type'] + " : " + dataflow['entities'][1]['entity']
	    	#print dataflow['entities'][2]['type'] + " : " + dataflow['entities'][2]['entity']
		#print dataflow['entities'][3]['type'] + " : " + dataflow['entities'][3]['entity']
	    except : 
		IndexError
	


	# Main method

	if __name__ == "__main__":

	    URLbase = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/48bb4ab4-82ee-4b67-9b5a-e618a8aecc8b?subscription-key=309fa2d4b3d74d999cce7eb84b2f97a6&verbose=true&timezoneOffset=0&q='

	   

	    URLcomplete = URLbase + sptote



	    data = URL_GetData(URLcomplete)

	    JSON_Write(data)

	    JSON_Parse(data)
	    #mysql connector

	'''

	cnn = mysql.connector.connect(user='root', password='root',
			              host='127.0.0.1',
			              database='sakila')

	cursor = cnn.cursor(dictionary=True)


	#luis api
	r= requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/48bb4ab4-82ee-4b67-9b5a-e618a8aecc8b?subscription-key=309fa2d4b3d74d999cce7eb84b2f97a6&verbose=true&timezoneOffset=0&q=%s'% verif)

	#get json
	res = r.json()

	#recoginize entities
	lastname = res["entities"][0]['entity']
	#print lastname

	e_mail = res["entities"][1]['entity']

	firstname = res["entities"][2]['entity']
	#print firstname

	#search answers in mysql database
	query = ("""SELECT * FROM customer WHERE LOWER(first_name) LIKE '%s' AND LOWER(last_name) LIKE '%s' """ % (firstname, lastname))
	cursor.execute(query)
	rows = cursor.fetchall()

	#print answer as text (prepare for translating into voice)
	for row in rows:
		result = str(row["email"])
		print "%s" % (result)

		cursor.close()
		cnn.close()
	
	tts.say(result)

		
else : 
	tts.say("I didn't understant please try again")
