import json
import cherrypy

from .usermanager import UserManager_cl

#----------------------------------------------------------
class Login_cl(object):
#----------------------------------------------------------
   exposed = True # gilt für alle Methoden


   #-------------------------------------------------------
   def __init__(self):
   #-------------------------------------------------------
      # spezielle Initialisierung können hier eingetragen werden
      self.usermanager = UserManager_cl()
      self.loggedIn = False

   #-------------------------------------------------------
   def GET(self):
   #-------------------------------------------------------
      if self.loggedIn == True:
         cherrypy.HTTPRedirect('/app')
      else:
         raise cherrypy.HTTPError(401)

   #-------------------------------------------------------
   def POST(self):
   #-------------------------------------------------------
      jsonData = json.loads(cherrypy.request.body.read())
      cookies = cherrypy.response.cookie

      if self.usermanager.authenticateUser(jsonData):
         self.loggedIn = True
         cookies['user'] = self.usermanager.getUserIdentifier(jsonData)
         cookies['user']['path'] = '/'
         cookies['user']['expires'] = 180000
         cookies['user']['version'] = 1
      else:
         raise cherrypy.HTTPError(401)