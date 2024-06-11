import json
import cherrypy

from .usermanager import UserManager_cl
from .database import Database_cl,DB_Table
from datetime import datetime,timedelta

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
            data = self.getEinsatzplan(1)
      else:
         data = self.db.searchData(DB_Table.Einsatzplan,"`userID`="+self.usermanager.getUserID())         
      
      return json.dumps(data,ensure_ascii=False,default=str)

   def PUT(self,cmd="",arg1=""):
      if not self.usermanager.userAuthenticated() and self.usermanager.getCurrentUserRole() != "Admin":
         raise cherrypy.HTTPError(401)
      # create termin
      try:
         jsonData =json.loads(cherrypy.request.body.read())
         jsonData = json.loads(jsonData)
      except:
         corruptData = True
         jsonData={}

      if(arg1 == "zahl"):
         self.db.updateData(DB_Table.Einsatzplan,jsonData)
         pass
      else:
         self.db.updateData(DB_Table.Einsatzplan,jsonData,True)
         pass


      

   def DELETE(self,cmd="",arg1=""):
      if not self.usermanager.userAuthenticated() and self.usermanager.getCurrentUserRole() != "Admin":
         raise cherrypy.HTTPError(401)
      # delete termin
      
   def getAvailablePersonal(self):
      return
   
   Weekday = {0:"Mo",1:"Di",2:"Mi",3:"Do",4:"Di",5:"Fr",6:"Sa",7:"So"}

   def getEinsatzplan(self,custom):
      result = {"Mo":{},"Di":{},"Mi":{},"Do":{},"Fr":{}}
      t = datetime.today().weekday()
      weekstart = datetime.today() + timedelta(days=-t)
      weekend = datetime.today() + timedelta(days=6-t)
      datetime.hour
      data  = self.db.searchData(DB_Table.Einsatzplan,"`Von`>='"+str(weekstart)+"' AND `Von` <='"+str(weekend)+"'")
      
      for v in data.values():
         flag = False
         c = 1
         while not flag:
            if c not in result[self.Weekday[v["Von"].weekday()]]:
               result[self.Weekday[v["Von"].weekday()]][c] = {}
            if v["Von"].hour in result[self.Weekday[v["Von"].weekday()]][c]:
               c+=1
               continue
            else:
               result[self.Weekday[v["Von"].weekday()]][c][v["Von"].hour] = {"Bis":v["Bis"].hour,"Ort":v["Ort"]}
               flag = True

      tmp = result # Ausgabe Sortieren
      for k,v in result.items():
         for ke,ve in v.items():
            tmp[k][ke] = dict(sorted(tmp[k][ke].items()))
         tmp[k] = dict(sorted(tmp[k].items()))
      result = tmp
      return result