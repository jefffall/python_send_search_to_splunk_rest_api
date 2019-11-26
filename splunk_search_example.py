import time # need for sleep
from xml.dom import minidom

import json 

import requests

import urllib3
urllib3.disable_warnings()


#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


base_url = 'https://splunkdevmint.test.com:8089'
username = 'admin'
password = 'password'

#search_query = "search=search index=* test123"
#search_query = "test123"
search_query = "search=search test123"


r = requests.get(base_url+"/servicesNS/admin/search/auth/login",
    data={'username':username,'password':password}, verify=False)

session_key = minidom.parseString(r.text).getElementsByTagName('sessionKey')[0].firstChild.nodeValue
print ("Session Key:", session_key)

r = requests.post(base_url + '/services/search/jobs/', data=search_query,
    headers = { 'Authorization': ('Splunk %s' %session_key)},
    verify = False)

sid = minidom.parseString(r.text).getElementsByTagName('sid')[0].firstChild.nodeValue
print ("Search ID", sid)

done = False
while not done:
    r = requests.get(base_url + '/services/search/jobs/' + sid,
        headers = { 'Authorization': ('Splunk %s' %session_key)},
        verify = False)
    response = minidom.parseString(r.text)
    for node in response.getElementsByTagName("s:key"):
        if node.hasAttribute("name") and node.getAttribute("name") == "dispatchState":
            dispatchState = node.firstChild.nodeValue
            print ("Search Status: ", dispatchState)
            if dispatchState == "DONE":
                done = True
            else:
                time.sleep(1)





r = requests.get(base_url + '/services/search/jobs/' + sid + '/results/',
    headers = { 'Authorization': ('Splunk %s' %session_key)},
    data={'output_mode': 'json'},
    verify = False)

#print r.text
r_json = json.loads(r.text)
raw =  r_json['results'][0]['_raw']
print raw
#pprint.pprint(json.loads(r.text))