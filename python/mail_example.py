#!/usr/bin/pythonTt

import smtplib

from  email.mime.text import MIMEText
sender = 'anto.daniel@localhost'
receivers = ['anto.daniel@inmobi.com','manzoor.ahamed@inmobi.com']
fp = open('file1','rb')
msg = MIMEText(fp.read())
fp.close()
message = """From: Anto Daniel <antodaniel@antodaniel.mygiz.com>
To: To Person <antexo.daniel@inmobi.com>
Subject: SMTP e-mail test 2

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, msg.as_string())         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"
