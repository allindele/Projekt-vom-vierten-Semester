# coding:utf-8

import sys
import os.path
import cherrypy

from app import application, template, login,krankmeldung,plan,mainsite
from app import database

from app.usermanager import UserManager_cl


#----------------------------------------------------------
def main():
#----------------------------------------------------------
   
   # aktuelles Verzeichnis ermitteln, damit es in der Konfigurationsdatei als
   # Bezugspunkt verwendet werden kann
   db = database.Database_cl()
   try:                                    # aktuelles Verzeichnis als absoluter Pfad
      currentDir_s = os.path.dirname(os.path.abspath(__file__))
   except:
      currentDir_s = os.path.dirname(os.path.abspath(sys.executable))
   cherrypy.Application.currentDir_s = currentDir_s

   configFileName_s = os.path.join(currentDir_s, 'server.conf') # im aktuellen Verzeichnis
   if os.path.exists(configFileName_s) == False:
      # Datei gibt es nicht
      configFileName_s = None


   userman = UserManager_cl()
   # autoreload-Monitor hier abschalten
   cherrypy.engine.autoreload.unsubscribe()

   # 1. Eintrag: Standardverhalten, Berücksichtigung der Konfigurationsangaben im configFile
   cherrypy.tree.mount(
      None, '/', configFileName_s
   )

   # 2. Eintrag: Method-Dispatcher für die "Applikation" "app" vereinbaren
   cherrypy.tree.mount(
      application.Application_cl(),
      '/app',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   # 3. Eintrag: Method-Dispatcher für die "Applikation" "templates" vereinbaren
   cherrypy.tree.mount(
      template.Template_cl(),
      '/templates',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   # 4. Eintrag: Method-Dispatcher für die "Applikation" "login" vereinbaren
   cherrypy.tree.mount(
      login.Login_cl(),
      '/login',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      krankmeldung.Krankmeldung_cl(userman,db),
      '/krankmeldung',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )
   cherrypy.tree.mount(
      plan.plan_Cl(userman,db),
      '/plan',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )
   cherrypy.tree.mount(
      mainsite.mainsite_cl(userman,db),
      '/mainsite',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )


   #cherrypy.server.socket_host = '0.0.0.0'
   cherrypy.engine.start()
   cherrypy.engine.block()

#----------------------------------------------------------
if __name__ == '__main__':
#----------------------------------------------------------
   main()