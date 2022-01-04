import pandas as pd
import numpy as np
import urllib.request
from bs4 import BeautifulSoup
import requests
import json
import re

main = {'ANDAMAN & NICOBAR ISLANDS': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/113/35/{}',
 'ANDHRA PRADESH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/3914/28/{}',
 'ARUNACHAL PRADESH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/389/12/{}',
 'ASSAM': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/1793/18/{}',
 'BIHAR': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/3496/10/{}',
 'CHANDIGARH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/178/4/{}',
 'CHHATTISGARH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/1517/22/{}',
 'DADRA & NAGAR HAVELI': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/24/26/{}',
 'DAMAN & DIU': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/15/25/{}',
 'DELHI': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/7865/7/{}',
 'GOA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/209/30/{}',
 'GUJARAT': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/5010/24/{}',
 'HARYANA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/2223/6/{}',
 'HIMACHAL PRADESH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/620/2/{}',
 'JAMMU & KASHMIR': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/1235/1/{}',
 'JHARKHAND': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/1746/20/{}',
 'KARNATAKA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/5827/29/{}',
 'KERALA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/3037/32/{}',
 'LADAKH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/144/37/{}',
 'LAKSHADWEEP': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/2/31/{}',
 'MADHYA PRADESH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/5230/23/{}',
 'MAHARASHTRA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/13933/27/{}',
 'MANIPUR': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/2064/14/{}',
 'MEGHALAYA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/234/17/{}',
 'MIZORAM': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/196/15/{}',
 'NAGALAND': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/352/13/{}',
 'ORISSA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/3137/21/{}',
 'PUDUCHERRY': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/248/34/{}',
 'PUNJAB': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/1307/3/{}',
 'RAJASTHAN': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/3911/8/{}',
 'SIKKIM': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/91/11/{}',
 'TAMIL NADU': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/7287/33/{}',
 'TELANGANA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/2301/36/{}',
 'TRIPURA': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/397/16/{}',
 'UTTAR PRADESH': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/14418/9/{}',
 'UTTARAKHAND': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/1500/5/{}',
 'WEST BENGAL': 'https://ngodarpan.gov.in/index.php/home/statewise_ngo/7900/19/{}'}

state = input('Enter state').upper()

def get_token(sess):
    req_csrf = sess.get('https://ngodarpan.gov.in/index.php/ajaxcontroller/get_csrf')
    return req_csrf.json()['csrf_token']

url = main[state]
detail_url = 'https://ngodarpan.gov.in/index.php/ajaxcontroller/show_ngo_info'

url

sess = requests.Session()

first = int(input('Enter starting page: '))
last = int(input('Enter ending page: '))
lis = []

for i in range(first, last + 1):
    html = urllib.request.urlopen(url.format(i)).read()
    soup = BeautifulSoup(html)
    table = soup.find_all('table')
    all_a = table[0].find_all('a')
    for j in range(len(all_a)):
        file = {}
        link = re.findall("show_ngo_info\(\"(\S+)\"\);", all_a[j]['onclick'])[0]
        req_details = sess.post(detail_url, headers={'X-Requested-With' : 'XMLHttpRequest'}, data={'id' : link, 'csrf_test_name' : get_token(sess)}).json()
        file['Unique ID of VO/NGO'] = req_details['infor']['0']['UniqueID']
        file['NGO Name'] = req_details['infor']['0']['ngo_name']
        file['NGO Type'] = req_details['registeration_info'][0]['TypeDescription']
        file['Registration No'] = req_details['registeration_info'][0]['nr_regNo']
        file['Date of Registration'] = req_details['registeration_info'][0]['ngo_reg_date']
        file['Email ID'] = req_details['infor']['0']['Email']
        file['Contact #'] = req_details['infor']['0']['Mobile']
        file['Members'] = req_details['member_info'][0]
        file['City'] = req_details['registeration_info'][0]['nr_city']
        file['State'] = state
        file['Sector'] = req_details['infor']['issues_working_db']
        file['Website URL'] = req_details['infor']['0']['ngo_url']
        lis.append(file)
        
    print(i)

df = pd.DataFrame(lis)

df.to_csv('NGO_Data of State- {}, from {} to {}.csv'.format(state, first, last))