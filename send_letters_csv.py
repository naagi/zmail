# coding: utf-8 

import sys
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


g_messages = []
g_states = []
g_to = []
g_from = []

#move lines 16-24 and encoding to config.py and import them?
backupemail = 'register.kruzhki30@gmail.com'
#encoding of all this files should be windows-1251 for now
fl_ok = 'patterns\\letter_ok_blank.txt'
fl_rj = 'patterns\\letter_reject_blank.txt'
fs_ok = 'patterns\\subject_ok_blank.txt'        #move subjects to config.py
fs_rj = 'patterns\\subject_reject_blank.txt'    

servername = 'smtp.mail.ru'
serverport = 2525


def create_text (filename, name, parallel, school, city, code, comment):
  text = ''
  with open (filename, 'rt') as f:
    text = ''.join(f.readlines())
    f.close()
  text = re.sub ('%NAME%', name, text)
  text = re.sub ('%PARALLEL%', parallel, text)
  text = re.sub ('%SCHOOL%', school, text)
  text = re.sub ('%CITY%', city, text)
  text = re.sub ('%CODE%', code, text)
  text = re.sub ('%COMMENT%', comment, text)

  return text

def create_emails():
  import csv
  with open (fs_ok, 'rt') as f:
    subject_ok = f.readline()
    f.close()
  with open (fs_rj, 'rt') as f:
    subject_reject = f.readline()
    f.close()
  with open (fs_rj, 'rt') as f:
    subject_unknown = f.readline()
    f.close()

  with open (sys.argv[1], 'r') as letterfile:
    letterreader = csv.reader (letterfile)
    for line in letterreader:
      name     = line[1]
      parallel = line[3]
      school   = line[4]
      city     = line[5]
      email    = line[8]
      code     = line[12]
      if len(line) > 14:
        comment  = line[14]
      else:
        comment = ''
      
      state = 0
      Subject = subject_unknown
      if code[0] == 'z':
        text = create_text (fl_ok, name, parallel, school, city, code, comment)
        state = 1
        Subject = subject_ok
      elif code[0] == 'n':
        text = create_text (fl_rj, name, parallel, school, city, code, comment)
        state = 2
        Subject = subject_reject
      else:
        print ('Unknown code type')
        state = 0
        Subject = subject_unknown
        text = ""

      # Prepare actual message
      To = [ email, backupemail ] #must be a list
      From = sys.argv[2]

      msg = MIMEMultipart("alternative")
      msg['Subject'] = Header(Subject, 'utf-8')
      msg['From'] = From
#      msg['To'] = ", ".join(To)
      msg['To'] = email
      part1 = MIMEText(text, "plain", "utf-8")
      msg.attach(part1)

      g_messages.append(msg)
      g_from.append(From)
      g_states.append(state)
      g_to.append (To)

    letterfile.close()


def send_emails():
  import smtplib

  if len(sys.argv) < 4:
    print ("Format: send_letters_csv.py File MailLogin MailPassword")
    exit()
  #add hash check of login-password here?
  #Useless if the script is viewable - anyone can remove the check.
  #Useful if it runs on server and isn't editable.

  mail_user = sys.argv[2]
  mail_pwd = sys.argv[3]

  try:
    server = smtplib.SMTP(servername, serverport)
    server.ehlo()
    server.starttls()

    server.login(mail_user, mail_pwd)
    #print (mail_user, mail_pwd)

    for i in range (len(g_messages)):
 
      if g_states[i] != 0:
        try:
           
           #print (g_from[i], g_to[i])
           
           server.sendmail(g_from[i], g_to[i], g_messages[i].as_string().encode('ascii'))
           print (str(i + 1) + '. ' + g_to[i][0] + ' ' + str(g_states[i]))
        except Exception as e:
           print (str(i + 1) + '. ' + g_to[i][0] + ' ' + 'FAILED TO SEND MAIL!')
           print (e)
    server.close()
  except Exception as e:
    print ("FAILED TO SEND ALL!!!")
    print (e)


  server.close()


create_emails()
send_emails()