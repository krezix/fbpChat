import os
from os.path import basename

class userdata:
    userdata_dir = "userdata" + os.sep
    file_with_user_and_pass = userdata_dir + "userandpass.txt"
    file_with_session = userdata_dir + "session.sss"

    data = {}

    def __init__(self):
        self.createDir(self.userdata_dir)
        self.createFile(self.file_with_session)
        self.createFile(self.file_with_user_and_pass)
    
    def createDir(self, dirName):
        if not os.path.exists(dirName):
            os.makedirs(dirName)

    def createFile(self,filename):
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                pass
        
    def getUserAndPassword(self):
        # user=username
        # password=password

        with open(self.file_with_user_and_pass, 'r',  encoding="utf-8") as f:
            for line in f :
                v = line.split("=")
                self.data[v[0].lower()] = v[1].strip("\n").strip("\t")
        return self
    
    def getSession(self):
        with open(self.file_with_session, 'r', encoding="utf-8") as f:
            sss = f.readline().strip("\n").strip("\t")
            
            if sss:
                self.data['session'] = eval(sss)
            else:
                self.data['session'] = ""
        return self
    
    def saveSession(self, data):
        with open(self.file_with_session, 'w', encoding="utf-8") as f:
            f.write(str(data))
        return self 

if __name__ == "__main__" : 
    user = userdata()
    user.getUserAndPassword()
    #session="alasldjdklaslado"
    #user.saveSession(session)
    user.getSession()
    print(user.data)
    print(user.data["username"], user.data["password"], user.data["session"])