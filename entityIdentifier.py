#!/usr/bin/python


import types

import urllib

import json


# Get the dataflow from URL

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

def JSON_Parse(data):

    dataflow = json.loads(data)
    
    # Attention: if any of needed datas cannot be found, the program will return an error

    print "Main Intent: " + dataflow['topScoringIntent']['intent']
    print "Main Entity: " + dataflow['entities'][0]['entity']


# Main method

if __name__ == "__main__":

    URLbase = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/e53cdca5-4c82-4d0c-b671-913314c95fe4?subscription-key=309fa2d4b3d74d999cce7eb84b2f97a6&verbose=true&timezoneOffset=0&q='

    QuoteText = raw_input() # Please give the query via keyboard

    URLcomplete = URLbase + QuoteText



    data = URL_GetData(URLcomplete)

    JSON_Write(data)

    JSON_Parse(data)

