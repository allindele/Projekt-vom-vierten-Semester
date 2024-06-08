import json
import cherrypy

from .usermanager import UserManager_cl
from .database import Database_cl,DB_Table

class Krankmeldung_cl(object):
#----------------------------------------------------------
   exposed = True # gilt für alle Methoden


   #-------------------------------------------------------
   def __init__(self,userman:UserManager_cl,database:Database_cl):
   #-------------------------------------------------------
      # spezielle Initialisierung können hier eingetragen werden
      self.usermanager = userman
      self.loggedIn = False
      self.db = database

   #-------------------------------------------------------
   def GET(self,cmd=""):
   #-------------------------------------------------------

      if not self.usermanager.userAuthenticated():
         raise cherrypy.HTTPError(401)
      data = self.db.getData(DB_Table.KrankMeldung)
      return json.dumps(data,ensure_ascii=False,default=str)

   def PUT(self,cmd=""):
      if not self.usermanager.userAuthenticated():
         raise cherrypy.HTTPError(401)
      corruptData = False
      try:
         jsonData =json.loads(cherrypy.request.body.read())
         jsonData = json.loads(jsonData)
      except:
         corruptData = True
         jsonData={}

      if not corruptData:
         if (cmd=="create"):
            jsonData["userID"] = self.usermanager.getUserID()

            self.db.updateData(DB_Table.KrankMeldung,jsonData,True)

   def DELETE(self,cmd="",arg1=""):
      if not self.usermanager.userAuthenticated():
         raise cherrypy.HTTPError(401)
      
      if cmd=="reject":
         self.db.deleteEntry(DB_Table.KrankMeldung,'`Knr`='+arg1)
      return