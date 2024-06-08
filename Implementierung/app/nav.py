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
            ["home", "Startseite"],
            ["krankmeldung.create","Test Krankmeldung Erstellen"],
            ["krankmeldung.list","Test Krankmeldung List"]
        ]

        if(self.usermanager.userAuthenticated()):
            user = self.usermanager.getCurrentUserRole()
            if(user != "User"):
                nav.append(["summary.ausgabe", "Ausgaben"])



        #momentan manuell



        return json.dumps(nav,ensure_ascii=False)
