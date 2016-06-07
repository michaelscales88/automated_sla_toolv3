import re
import os
import datetime
import sys
from test_client import test_client
import openpyxl

from subprocess import call, Popen, PIPE
from os import path

os.path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from src.email_reader import (get_downloads, get_voice_mail)

now = datetime.datetime.today() - datetime.timedelta(days=2)


'''
test_string = "Voicemail Message (7586 > AAP) From:7586"
searchObj = re.search( r'(.*) > (.*?) .*', test_string, re.M|re.I)
telNumber = searchObj.group(1).replace('Voicemail',"")
telNumber = telNumber.replace('Message',"")
telNumber = telNumber.replace(' ',"")
telNumber = telNumber.replace('(',"")
print(telNumber)
clientNumber = searchObj.group(2).replace(')',"")
print(clientNumber)

date = '06-06-2016'
text_file = open('C:\\Uses\\mscales\\Desktop\\' + 'voiceMails.txt', 'a')
voiceMails = {'a':'a','b':'b','c':'c','d':'d'}
for client in voiceMails:
    text_file.write("Client: %s Number %s\n" % (client, voiceMails[client]))
    #print("Client: %s Number %s" % (client, voiceMails[client]))
text_file.close()


getVoicemails(now)
'''
call_details_file = openpyxl.load_workbook(os.path.dirname(path.dirname(path.abspath(__file__))) + '/raw/Call Details.xlsx')
ws = call_details_file.active
print(ws.max_row)
t1 = test_client()
t1.__str__()
'''
print(os.getcwd())
ARG_PATH = os.path.dirname(path.dirname(path.abspath(__file__))) + '\\converter\\tools\\ofc.ini'
EXC_PATH = os.path.dirname(path.dirname(path.abspath(__file__))) + '\\converter\\tools\\ofc.exe'
#print(ARG_PATH)
#print(EXC_PATH)
#subprocess.call([EXC_PATH, ARG_PATH], shell=False)
#print("popen")
date = '12042015'
archive_date = '/Archive/%s/%s' % (date,date)
print(archive_date)
print(type(archive_date))

proc = subprocess.Popen([EXC_PATH, ARG_PATH, 'command'])
proc.wait()
print(proc.returncode)
'''
