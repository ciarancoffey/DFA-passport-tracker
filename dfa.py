#!/usr/bin/env python
import requests
import pickle
from bs4 import BeautifulSoup
import sys
import os.path

application_num = sys.argv[1]

payload = {'application_number': application_num }

r = requests.post("https://www.dfa.ie/irish-embassy/great-britain/passports/track-my-passport-application/", data=payload)
if r.status_code == 200:
    if os.path.isfile("last_updated_time.p"):
        previous_updated =  pickle.load( open( "last_updated_time.p", "rb") )
    else:
        previous_updated = "0"
    soup = BeautifulSoup(r.text, "html.parser")
    status=soup.find("table", {"class": "passportTracking"})
    last_updated=status.findAll("td")[3]
    #print(last_updated.text)
    pickle.dump(last_updated.text, open( "last_updated_time.p", "wb" ) )
    if previous_updated!=last_updated.text:
        print("Application: " + status.findAll("td")[0].text)
        print("Status: " + status.findAll("td")[1].text)
        print("ETA: " + status.findAll("td")[2].text)
        print("Last Updated: " + status.findAll("td")[3].text)


