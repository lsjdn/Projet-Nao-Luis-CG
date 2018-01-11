import mysql.connector
import requests
#from luis_sdk import LUISClient

cnn = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1', port=8889,
                              database='sakila')

cursor = cnn.cursor(dictionary=True)

var = raw_input(u'Please input the text to predict:\n')

r= requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/48bb4ab4-82ee-4b67-9b5a-e618a8aecc8b?subscription-key=309fa2d4b3d74d999cce7eb84b2f97a6&verbose=true&timezoneOffset=0&q=%s'% var)

res = r.json()

lastname = res["entities"][0]['entity']

#print lastname

e_mail = res["entities"][1]['entity']

firstname = res["entities"][2]['entity']

#print firstname

query = ("""SELECT * FROM customer WHERE LOWER(first_name) LIKE '%s' AND LOWER(last_name) LIKE '%s' """ % (firstname, lastname))

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
  print "%s" % (row["email"])

cursor.close()
cnn.close()
