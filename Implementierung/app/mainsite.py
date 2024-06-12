import json
import cherrypy

from .usermanager import UserManager_cl
from .database import Database_cl,DB_Table

class mainsite_cl(object):
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
      data = {"b2":'<button data-action="Einsatzplan">Einsatzplan </button>'}
      if self.usermanager.getCurrentUserRole()=="Admin":
         data["b1"] = '<button data-action="Krankmeldungen">Krankmeldungen</button>'
      else:
         data["b1"] ='<button data-action="Krankmelden">Krankmelden</button>'
      return json.dumps(data,ensure_ascii=False,default=str)
