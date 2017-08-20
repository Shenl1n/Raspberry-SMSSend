#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 发送短信
# Sample script to show how to send SMS
import gammu
import pyodbc
import datetime

cnxn = pyodbc.connect(
    'DRIVER=FreeTDS;SERVER=192.168.1.14\SQLHOME;DATABASE=test;UID=sa;PWD=19920530fF;port=49165;')

cursor = cnxn.cursor()
cursor.execute(
    "select top 1 id, phonenumber, smsdata from sms where sent='N' order by InsertDate")
row = cursor.fetchone()
try:
    id = row[0]
    phones = row[1]
    smsdata = row[2]
except Exception, e:
    raise Exception('No SMS Found!')
# send SMS
sm = gammu.StateMachine()
sm.ReadConfig()
sm.Init()
if ";" in phones:
    phoneList = phones.split(';',1)
    for phone in phoneList:
        message = {
        'Text': smsdata,
        'SMSC': {'Location': 1},
        'Number': phone.encode('utf-8'),
        'Coding': 'Unicode_No_Compression',
        }
        print message
        sm.SendSMS(message)
        print 'message sent'
else:
    message = {
        'Text': smsdata,
        'SMSC': {'Location': 1},
        'Number': phones.encode('utf-8'),
        'Coding': 'Unicode_No_Compression',
    }
    print message
    # Actually send the message
    sm.SendSMS(message)
    print 'message sent'
# update sent sms
cursor.execute(
    "UPDATE SMS SET Sent = ?, UpdateDate = ? where id = ?", 'Y', datetime.datetime.now(),id)
cnxn.commit()
cnxn.close()
