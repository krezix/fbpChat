from fbchat import log, Client
from fbchat.models import *
import os
import datetime
import requests
import smtplib
from os.path import basename
from  email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from userdata import userdata

# Subclass fbchat.Client and override required methods
class fbLogger(Client):
    userinfo ={}
    threadsDir = "threads" + os.sep
    def send_mail(self,send_from,send_to,subject, text, files=None, server='127.0.0.1'):
        assert isinstance(send_to, list)
        msg = MIMEMultipart()
        msg['From']= send_from
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f,'rb') as fil:
                part = MIMEApplication(fil.read(),Name=basename(f))
            part['Content-Disposition']='attachment:filename="%s"' % basename(f)        
            msg.attach(part)

        smtp= smtplib.SMTP(server)
        smtp.sendmail(send_from,send_to, msg.as_string())
        smtp.close()

    def __init__(self,email,password,user_agent=None, max_tries=5,session_cookies=None, logging_level=20,GUI=None ):
        super().__init__(email,password,user_agent, max_tries,session_cookies, logging_level)
        if GUI is not None:
            print(GUI)
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        #self.markAsDelivered(thread_id, message_object.uid)
        #self.markAsRead(thread_id)
        #TODO criar ficheiro com userinfo 
        #ao iniciar verificar se existe o ficheiro e obter
        #isto se nao estiver na lista de users
        #nome = client.fetchUserInfo(author_id)[author_id].name
        
            
        dirn = self.threadsDir+ thread_id + os.sep
        if not os.path.exists(dirn):
            os.makedirs(dirn)
        filename =os.path.normpath( dirn + thread_id+'.txt')

        if author_id in self.userinfo:
            name = self.userinfo[author_id]
        else:
            userinfo_filename = dirn + "userinfo.txt"
            if os.path.exists(userinfo_filename):
                with open(userinfo_filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    l = line.split("=")
                    self.userinfo[l[0]] = l[1]
                if self.uid == author_id:
                    if self.uid not in self.userinfo:
                        with open (userinfo_filename,"a", encoding="utf-8") as f:
                            self.userinfo[self.uid] = client.fetchUserInfo(self.uid)[self.uid].name
                            f.write(self.uid + "=" + self.userinfo[self.uid] +"\n")
                else:
                    with open (userinfo_filename,"a", encoding="utf-8") as f:
                        self.userinfo[author_id] = client.fetchUserInfo(author_id)[author_id].name
                        f.write(author_id + "=" + self.userinfo[author_id] +"\n")
            else:

                self.userinfo[author_id] = client.fetchUserInfo(author_id)[author_id].name
                name = self.userinfo[author_id]
                with open(userinfo_filename, "w", encoding="utf-8") as f:
                    f.write(author_id + "=" + name +"\n")    
            self.userinfo[author_id] = client.fetchUserInfo(author_id)[author_id].name
            name = self.userinfo[author_id]

        if os.path.exists(filename):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not

        
                
        with open(filename, append_write, encoding="utf-8") as the_file:
            #the_file.write("{} from {} in {}\n".format(message_object, author_id, thread_type.name))
            files = []
            if self.uid != author_id:
                the_file.write("<otheruser> ({})</otheruser> <othertime>[{}] </othertime>: <othertext>{}</othertext>\n".format( name ,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message_object.text))
            else:
                the_file.write("<meuser> ({})</meuser> <metime>[{}] </metime>: <metext>{}</metext>\n".format( name ,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message_object.text))
            if len(message_object.attachments) >0:
                for a in message_object.attachments:
                    if isinstance(a, FileAttachment): # Check if it's a file
                        url = a.url # Get url to download
                    
                        filename =  dirn + a.name # Get file name (you can use custom file name, but remember to use a proper file format)
                        content = requests.get(url).content # Downloading the file
                        with open(filename, "wb") as file:
                            file.write(content) # Saving it

                    if isinstance(a, AudioAttachment): # Check if it's a file
                        url = a.url # Get url to download
                    
                        filename =  dirn + a.filename # Get file name (you can use custom file name, but remember to use a proper file format)
                        content = requests.get(url).content # Downloading the file
                        with open(filename, "wb") as file:
                            file.write(content) # Saving it
                            
                    if isinstance(a, ImageAttachment): # Check if it's a file
                        if a.large_preview_url is not None:
                            url = a.large_preview_url  # Get url to download
                        elif a.animated_preview_url is not None:
                            url = a.animated_preview_url
                        t =  url.split('/')[-1]
                        t = t.split('?')[0]
                        filename = dirn + t# Get file name (you can use custom file name, but remember to use a proper file format)
                        content = requests.get(url).content # Downloading the file
                        with open(filename, "wb") as file:
                            file.write(content) # Saving it

                    if isinstance(a, VideoAttachment): # Check if it's a file
                        #if a.preview_url is not None:
                        url = a.preview_url  # Get url to download
                        
                        t =  url.split('/')[-1]
                        t = t.split('?')[0]
                        filename = dirn + t# Get file name (you can use custom file name, but remember to use a proper file format)
                        print(filename)
                        content = requests.get(url).content # Downloading the file
                        with open(filename, "wb") as file:
                            file.write(content) # Saving it
                    the_file.write("ficheiro :  {}\n".format(filename))

        log.info("{} ({}) [{}]: {} in {}\n".format(author_id , name ,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message_object, thread_type.name))

        # If you're not the author, echo
        #if author_id != self.uid:
        #    self.send(message_object, thread_id=thread_id, thread_type=thread_type)
user = userdata()
user.getUserAndPassword()
user.getSession()

client = fbLogger( user.data["username"], user.data["password"], session_cookies = user.data["session"])#,  GUI=teste)
session_cookies = client.getSession()
user.saveSession(session_cookies)
client.listen()
