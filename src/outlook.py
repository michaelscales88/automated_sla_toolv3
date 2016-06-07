import email
import email.mime.multipart
import imaplib
import re
from collections import defaultdict


class Outlook:
    def __init__(self, use_date, login_type):
        self.my_date = use_date
        self.today = self.my_date.strftime("%d-%b-%Y")
        self.IMAP = imaplib.IMAP4_SSL(login_type)

    def login(self, username, password):
        while True:
            try:
                r, d = self.IMAP.login(username, password)
                assert r == 'OK', 'login failed'
                print(" > Sign as ", d)
            except:
                print(" > Sign In ...")
                continue
            break

    def get_voice_mail_info(self, all_emails):
        voice_mails = defaultdict(list)
        for subject_line in all_emails:
            client_number, phone_number, time_of_call = self.get_tokens(subject_line)
            self.get_tokens(subject_line)
            if client_number != 0:
                voice_mails[client_number].append(phone_number + " + " + time_of_call)
        return voice_mails

    def all_ids(self):
        result, data = self.IMAP.uid('search', None, "ALL")
        all_list = []
        if result == 'OK':
            for num in data[0].split():
                result, data = self.IMAP.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    email_message = email.message_from_bytes(data[0][1])
                    all_list.append(email_message['Subject'])
        return all_list

    def read_ids(self):
        date_sent_on = "ON " + self.today
        result, data = self.IMAP.uid('search', date_sent_on, "ALL")
        read_list = []
        if result == 'OK':
            for num in data[0].split():
                result, data = self.IMAP.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    email_message = email.message_from_bytes(data[0][1])
                    read_list.append(email_message['Subject'] + email_message['Date'])
        return read_list

    def get_tokens(self, search_string):
        search_object = re.search(r'(.*) > (.*?) .*', search_string, re.M | re.I)
        search_object2 = re.search(r'(.*)' + self.my_date.strftime("%Y") + ' (.*?) .*', search_string, re.M | re.I)
        if search_object:
            phone_number = search_object.group(1).replace('Voicemail', "")
            phone_number = phone_number.replace('Message', "")
            phone_number = phone_number.replace(' ', "")
            phone_number = phone_number.replace('(', "")
            client_number = search_object.group(2).replace(')', "")
            return client_number, phone_number[-4:], search_object2.group(2)
        else:
            return 0, 0, 0

    def inbox(self):
        return self.IMAP.select("Inbox")

'''

Unmodified functions below. Likely do not work

    def sendEmailMIME(self,recipient,subject,message):
        msg = email.mime.multipart.MIMEMultipart()
        msg['to'] = recipient
        msg['from'] = self.username
        msg['subject'] = subject
        msg.add_header('reply-to', self.username)
        #headers = "\r\n".join(["from: " + "sms@kitaklik.com","subject: " + subject,"to: "
                                + recipient,"mime-version: 1.0","content-type: text/html"])
        #content = headers + "\r\n\r\n" + message
        try:
            self.smtp = smtplib.SMTP('smtp-mail.outlook.com',587)
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.login(self.username, self.password)
            self.smtp.sendmail(msg['from'], [msg['to']], msg.as_string())
            print("   email replied")
        except smtplib.SMTPException:
            print("Error: unable to send email")

    def sendEmail(self,recipient,subject,message):
        headers = "\r\n".join(["from: " + self.username,"subject: " + subject,"to: "
                                + recipient,"mime-version: 1.0","content-type: text/html"])
        content = headers + "\r\n\r\n" + message
        while True:
            try:
                self.smtp = smtplib.SMTP('smtp-mail.outlook.com',587)
                self.smtp.ehlo()
                self.smtp.starttls()
                self.smtp.login(self.username, self.password)
                self.smtp.sendmail(self.username, recipient, content)
                print("   email replied")
            except:
                print("   Sending email...")
                continue
            break

    def list(self):
        #self.login()
        return self.IMAP.list()

    def select(self,str):
        return self.IMAP.select(str)

    def junk(self):
        return self.IMAP.select("Junk")

    def logout(self):
        return self.IMAP.logout()

    def today(self):
        mydate = datetime.datetime.now()
        return mydate.strftime("%d-%b-%Y")

    def unreadIdsToday(self):
        r, d = self.IMAP.search(None, '(SINCE "' + self.today + '")', 'UNSEEN')
        list = d[0].split(' ')
        return list

    def unreadIds(self):
        r, d = self.IMAP.search(None, "UNSEEN")
        list = d[0].split(' ')
        return list

    def readIdsToday(self):
        r, d = self.IMAP.search(None, '(SINCE "' + self.today + '")', 'SEEN')
        list = d[0].split(' ')
        return list

    def getEmail(self,id):
        r, d = self.IMAP.fetch(id, "(RFC822)")
        self.raw_email = d[0][1]
        self.email_message = email.message_from_string(self.raw_email)
        return self.email_message

    def unread(self):
        list = self.unreadIds()
        latest_id = list[-1]
        return self.getEmail(latest_id)

    def read(self):
        list = self.read_ids()
        latest_id = list[-1]
        return self.getEmail(latest_id)

    def readToday(self):
        list = self.readIdsToday()
        latest_id = list[-1]
        return self.getEmail(latest_id)

    def unreadToday(self):
        list = self.unreadIdsToday()
        latest_id = list[-1]
        return self.getEmail(latest_id)

    def readOnly(self,folder):
        return self.IMAP.select(folder, readonly = True)

    def writeEnable(self,folder):
        return self.IMAP.select(folder, readonly = False)

    def rawRead(self):
        list = self.read_ids()
        latest_id = list[-1]
        r, d = self.IMAP.fetch(latest_id, "(RFC822)")
        self.raw_email = d[0][1]
        return self.raw_email

    def mailbody(self):
        if self.email_message.is_multipart():
            for payload in self.email_message.get_payload():
            # if payload.is_multipart(): ...
                body = payload.get_payload().split(self.email_message['from'])[0].split('\r\n\r\n2015')[0]
            return body
        else:
            body = self.email_message.get_payload().split(self.email_message['from'])[0].split('\r\n\r\n2015')[0]
            return body

    def mailsubject(self):
        return self.email_message['Subject']

    def mailfrom(self):
        return self.email_message['from']

    def mailto(self):
        return self.email_message['to']

    def mailreturnpath(self):
        return self.email_message['Return-Path']

    def mailreplyto(self):
        return self.email_message['Reply-To']

    def mailall(self):
        return self.email_message
'''