import json
import cherrypy

from .usermanager import UserManager_cl

class Navbar_cl(object):
#----------------------------------------------------------
   exposed = True # gilt für alle Methoden


   #-------------------------------------------------------
   def __init__(self,userman:UserManager_cl):
   #-------------------------------------------------------
      # spezielle Initialisierung können hier eingetragen werden
      self.usermanager = userman
      self.loggedIn = False

   #-------------------------------------------------------
   def GET(self):
   #-------------------------------------------------------
        nav = [
            ["krankmeldung.list","Test Krankmeldung List"],
            ["einsatzplan.list","EPlan"],
            ["einsatzplan.detail","EDetail"]
        ]

        if(self.usermanager.userAuthenticated()):
            user = self.usermanager.getCurrentUserRole()
            if(user != "User"):
                pass


        #momentan manuell



        return json.dumps(nav,ensure_ascii=False)
