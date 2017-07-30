#!/usr/bin/env python
import requests
import pickle
from bs4 import BeautifulSoup
import sys
import os.path

application_num = sys.argv[1]

payload = {'__RequestVerificationToken':'HlKl8OZQyCy6s9ZfqtjRpICSU9_Wf5BlC2MrGVgZvTBtj6cCJ3DaxgCAYOZWSDTG4TXCgzo-etzT0_LqfhE9DARHPKc1', 'search[Criteria][ReferenceNumber]': application_num }

cookies = {'__unam': '6c7a76c-15d92c462f9-3297fafc-4', "__RequestVerificationToken_L1Bhc3Nwb3J0VHJhY2tpbmc1": "6zQouq-h6YH6vb-Ca-APLktFcr3jlcgUkn6y58-e2jMKbShINajRZNacEDg5mpRF6dZLJHC6Q_7Fp0DTbVb_C2HPhn81"}

headers={"Host": "passporttracking.dfa.ie"}

#curl 'https://passporttracking.dfa.ie/PassportTracking/Home/GetStep' -H 'Host: passporttracking.dfa.ie'  -H 'Cookie: __unam=6c7a76c-15d92c462f9-3297fafc-4; __RequestVerificationToken_L1Bhc3Nwb3J0VHJhY2tpbmc1=6zQouq-h6YH6vb-Ca-APLktFcr3jlcgUkn6y58-e2jMKbShINajRZNacEDg5mpRF6dZLJHC6Q_7Fp0DTbVb_C2HPhn81'  --data '__RequestVerificationToken=HlKl8OZQyCy6s9ZfqtjRpICSU9_Wf5BlC2MrGVgZvTBtj6cCJ3DaxgCAYOZWSDTG4TXCgzo-etzT0_LqfhE9DARHPKc1&search%5BCriteria%5D%5BReferenceNumber%5D=30104684499'

r = requests.post("https://passporttracking.dfa.ie/PassportTracking/Home/GetStep", data=payload, cookies=cookies, headers=headers)
if r.status_code == 200:
    if os.path.isfile("last_updated_time.p"):
        previous_updated =  pickle.load( open( "last_updated_time.p", "rb") )
    else:
        previous_updated = "0"
    soup = BeautifulSoup(r.text, "html.parser")
    status=soup.find("div", {"class": "jumbotron text-center s-jumbotron"})
    progress=soup.find("div", {"class": "row progress-container"})
    print (progress.text)
    last_updated=status.find("div", {"class": "lastUpdated"})
    pickle.dump(last_updated.text, open( "last_updated_time.p", "wb" ) )
    if previous_updated!=last_updated.text:
        exit(0)
        #print("Application: " + progress.find("div", {"class": "col-md-2 text-center progress-tracking-left"}).text)
        #print("Status: " + progress.findAll("td")[1].text)
        #print("ETA: " + progress.findAll("td")[2].text)
        #print("Last Updated: " + progress.findAll("td")[3].text)
