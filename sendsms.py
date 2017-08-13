#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 发送短信
# Sample script to show how to send SMS
import gammu
import pyodbc
import datetime
smsdata = ""
cnxn = pyodbc.connect(
    'DRIVER=FreeTDS;SERVER=192.168.1.14\SQLHOME;DATABASE=test;UID=sa;PWD=19920530fF;port=49165;')

cursor = cnxn.cursor()
cursor.execute(
    "select top 1 id, smsdata from sms where sent='N' order by InsertDate")
row = cursor.fetchone()
id = row[0]
smsdata = row[1]
# send SMS
sm = gammu.StateMachine()
sm.ReadConfig()
sm.Init()

message = {
    'Text': smsdata,
    'SMSC': {'Location': 1},
    'Number': '+8613032163799',
    'Coding': 'Unicode_No_Compression',
}

# Actually send the message
sm.SendSMS(message)
# update sent sms
cursor.execute(
    "UPDATE SMS SET Sent = ?, UpdateDate = ? where id = ?", 'Y', id, datetime.datetime.now())
cnxn.commit()
cnxn.close()
