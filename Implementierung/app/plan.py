import json
import cherrypy

from .usermanager import UserManager_cl
from .database import Database_cl,DB_Table

class plan_Cl(object):
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
   def GET(self,cmd="",arg1=""):
   #-------------------------------------------------------

      if not self.usermanager.userAuthenticated():
         raise cherrypy.HTTPError(401)
      data = {}
      if(self.usermanager.getCurrentUserRole() == "Admin"):
         if(cmd=="detail"):
            if(arg1=="0"):
               pass
            else:
               data = self.db.getData(DB_Table.Einsatzplan,arg1)
         elif(cmd=="getPersonal"):
            data = self.getAvailablePersonal()
      else:
         data = self.db.searchData(DB_Table.Einsatzplan,"`userID`="+self.usermanager.getUserID())         
      
      return json.dumps(data,ensure_ascii=False,default=str)

   def PUT(self,cmd=""):
      if not self.usermanager.userAuthenticated() and self.usermanager.getCurrentUserRole() != "Admin":
         raise cherrypy.HTTPError(401)
      # create termin

      

   def DELETE(self,cmd="",arg1=""):
      if not self.usermanager.userAuthenticated() and self.usermanager.getCurrentUserRole() != "Admin":
         raise cherrypy.HTTPError(401)
      # delete termin
      
   def getAvailablePersonal(self):
      return