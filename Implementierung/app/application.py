# coding: utf-8

import cherrypy

from .database import Database_cl
from .usermanager import UserManager_cl


#----------------------------------------------------------
class Application_cl(object):
#----------------------------------------------------------

   exposed = True # gilt für alle Methoden

   #-------------------------------------------------------
   def __init__(self):
   #-------------------------------------------------------
      # spezielle Initialisierung können hier eingetragen werden
      self.usermanager = UserManager_cl()

   #-------------------------------------------------------
   def GET(self, id=None):
   #-------------------------------------------------------

      if self.usermanager.userAuthenticated():
         raise cherrypy.HTTPError(401)

      retVal_s = ''
      return retVal_s

# EOF