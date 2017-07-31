#!/usr/bin/env python
import requests
import pickle
from bs4 import BeautifulSoup
import sys
import os.path

application_num = sys.argv[1]

url = "https://passporttracking.dfa.ie/PassportTracking/Home/GetStep"
payload = {'__RequestVerificationToken':'HlKl8OZQyCy6s9ZfqtjRpICSU9_Wf5BlC2MrGVgZvTBtj6cCJ3DaxgCAYOZWSDTG4TXCgzo-etzT0_LqfhE9DARHPKc1', 'search[Criteria][ReferenceNumber]': application_num }
cookies = {'__unam': '6c7a76c-15d92c462f9-3297fafc-4', "__RequestVerificationToken_L1Bhc3Nwb3J0VHJhY2tpbmc1": "6zQouq-h6YH6vb-Ca-APLktFcr3jlcgUkn6y58-e2jMKbShINajRZNacEDg5mpRF6dZLJHC6Q_7Fp0DTbVb_C2HPhn81"}
headers={"Host": "passporttracking.dfa.ie"}

r = requests.post(url, data=payload, cookies=cookies, headers=headers)
if r.status_code == 200:
    if os.path.isfile("last_updated_time.p"):
        previous_updated =  pickle.load( open( "last_updated_time.p", "rb") )
    else:
        previous_updated = "0"
    soup = BeautifulSoup(r.text, "html.parser")
    application_id=soup.findAll("h2")[0].text.strip().split(":", 1)[1].lstrip()
    current_status=soup.findAll("h2")[1].text.strip()
    estimated_date=soup.findAll("div", {"class", "status-date"})[0].text.strip()
    last_updated=soup.findAll("div", {"class": "lastUpdated" })[0].text.strip().split(":", 1)[1].lstrip()
    pickle.dump(last_updated, open( "last_updated_time.p", "wb" ) )
    if previous_updated!=last_updated:
        print("Application: " + application_id)
        print("Status: " + current_status)
        print("ETA: " + estimated_date)
        print("Last Updated: " + last_updated)
