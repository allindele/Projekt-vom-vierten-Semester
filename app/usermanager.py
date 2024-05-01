# coding: utf-8

# UserManager to log in the user
import os
import codecs
import json
import cherrypy

#----------------------------------------------------------
class UserManager_cl(object):
#----------------------------------------------------------

   # pylint: disable=E1101
   #-------------------------------------------------------
   def __init__(self):
   #-------------------------------------------------------
      self.workingDir_s = cherrypy.Application.currentDir_s
      
      self.users = {}
      self.users_maxId = 0
      self.readUsers()


   #-------------------------------------------------------
   def authenticateUser(self, data):
   #-------------------------------------------------------
      username = data['username']
      password = data['password']

      for uid in self.users:
         if self.users[uid]['login'] == username and self.users[uid]['password'] == password:
            return True
      
      return None

   #-------------------------------------------------------
   def getUserIdentifier(self, data):
   #-------------------------------------------------------
      username = data['username']
      password = data['password']
      
      for uid in self.users:
         if self.users[uid]['login'] == username and self.users[uid]['password'] == password:
            return uid + ':' + self.users[uid]['role']

   #-------------------------------------------------------
   def userAuthenticated(self):
   #-------------------------------------------------------
      cookies = cherrypy.request.cookie
      if 'user' not in cookies:
         return False

      return True
   #-------------------------------------------------------
   def getCurrentUserRole(self):
   #-------------------------------------------------------
      user = self.getCurrentUser()
      return user['role']

   #-------------------------------------------------------
   def getCurrentUser(self):
   #-------------------------------------------------------
      cookies = cherrypy.request.cookie
      if 'user' in cookies:
         userCookieVal = cookies['user'].value
         splitted = userCookieVal.split(':')

         user = self.getUsers(str(splitted[0]))
         return user

# ------------------------------- User Management -------------------------------
   #-------------------------------------------------------
   def readUsers(self):
   #-------------------------------------------------------
      filePath = os.path.join(self.workingDir_s, 'data', 'users.json')

      self.users = self.readDataFromFile(filePath)
      self.users_maxId = self.getUsersMaxId()

   #-------------------------------------------------------
   def getUsers(self, id = None):
   #-------------------------------------------------------
      # alle projekkte zurückgeben
      if id == None:
         return self.users

      if id in self.users:
         return self.users[id]
      else:
         return self.getDefaultUser()

   #-------------------------------------------------------
   def getUserByUsername(self, username):
   #-------------------------------------------------------
      for id in self.users:
         if self.users[id]['username'] == username:
            return self.users[id]

      return {}
   #-------------------------------------------------------
   def getUsersByRole(self, role):
   #-------------------------------------------------------
      users = {}

      for key in self.users:
         if self.users[key]['role'] == role:
            users[key] = self.users[key]

      return users


   def getUserUnternehmen(self):
      user = self.getCurrentUser()
      return user['unternehmen']
   #-------------------------------------------------------
   def saveOrUpdateUsers(self, id, data):
   #-------------------------------------------------------
      self.readUsers()
      dataStored = False

      del data['id']

      id_s = str(id)
      if id == 0:
         self.users_maxId += 1
         id_s = str(self.users_maxId)
         self.users[id_s] = data
         dataStored = True

      if id_s in self.users and not dataStored:
         self.users[id_s] = data
         dataStored = True
      
      if dataStored:
         self.saveUsersToFile()
         return id_s
      else:
         return None

   #-------------------------------------------------------
   def saveUsersToFile(self):
   #-------------------------------------------------------
      filePath = os.path.join(self.workingDir_s, 'data', 'users.json')
      self.writeDataToFile(filePath, self.users)

   #-------------------------------------------------------
   def deleteUser(self, id):
   #-------------------------------------------------------      
      deleted = False
      id_s = str(id)
      if id_s in self.users:
         del self.users[id_s]
         deleted = True
      
      if deleted:
         self.saveUsersToFile()

      return deleted

   #-------------------------------------------------------
   def getUsersMaxId(self):
   #-------------------------------------------------------
      return len(self.users)

   #-------------------------------------------------------
   def getDefaultUser(self):
   #-------------------------------------------------------
      return {
         'login': '',
         'username': '',
         'password': '',
         'role': ''
      }

   #-------------------------------------------------------
   def writeDataToFile(self, path, data):
   #-------------------------------------------------------
      with codecs.open(path, 'w', 'utf-8') as fp_o:
         json.dump(data, fp_o, indent=3)

   #-------------------------------------------------------
   def readDataFromFile(self, path):
   #-------------------------------------------------------
      try:
         fp_o = codecs.open(path, 'r', 'utf-8')
      except Exception:
         # datei anlegen
         self.writeDataToFile(path, {})
      else:
         with fp_o:
            return json.load(fp_o)