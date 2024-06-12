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
   def GET(self,cmd="",arg1="",arg2="",arg3="",arg4=""):
   #-------------------------------------------------------

      if not self.usermanager.userAuthenticated():
         raise cherrypy.HTTPError(401)
      data = {}
      if(self.usermanager.getCurrentUserRole() == "Admin"):
         if(cmd=="detail"):
            if(arg1=="0"):
               pass
            else:
               data = self.db.searchData(DB_Table.Einsatzplan,"`Vnr`='"+arg1+"'")[int(arg1)]
               data["Vnr"] = int(arg1)
         elif(cmd=="getPersonal" and len(arg1)>0 and len(arg2)>0):
            arg1 = datetime.strptime(arg1,"%Y-%m-%dT%H:%M")
            arg2 = datetime.strptime(arg2,"%Y-%m-%dT%H:%M")
            data = self.getAvailablePersonal(arg1,arg2,arg3)
         else:
            data = self.getEinsatzplan(0)
            data["extra"] = '<button data-action="edit">Edit</button><button data-action="create">Veranstaltung erstellen</button>'

      else:
         data =self.getEinsatzplan(int(self.usermanager.getUserID()))
      
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

      if(arg1 != ""):
         self.db.updateData(DB_Table.Einsatzplan,jsonData)
         pass
      else:
         self.db.updateData(DB_Table.Einsatzplan,jsonData,True)
         pass


      

   def DELETE(self,cmd="",arg1=""):
      if not self.usermanager.userAuthenticated() and self.usermanager.getCurrentUserRole() != "Admin":
         raise cherrypy.HTTPError(401)
      # delete termin
      
   def getAvailablePersonal(self,startTime,endTime,location):
      arbeiter = self.db.searchData(DB_Table.User,"`Rolle`='Arbeiter'")
      krankmeldungen = self.db.getData(DB_Table.KrankMeldung)
      veranstaltungen = self.getEinsatzplanCurrentWeek()

      for v in veranstaltungen.values():
         if (v["Von"].day != startTime.day)or (v["Von"].month != startTime.month) or (v["Von"].year != startTime.year): 
            continue
         if v["userID"] not in arbeiter:
            continue
         extraTime = 0
         if location != v["Ort"]:
            extraTime += 2
         if (endTime.hour < v["Von"].hour - extraTime):
            continue
         elif (startTime.hour > v["Bis"].hour + extraTime):
            continue
         del(arbeiter[v["userID"]])
      for v in krankmeldungen.values():
         if ((v["Von"].day <= startTime.day)and (v["Von"].month <= startTime.month) and (v["Von"].year <= startTime.year)and
             (v["Bis"].day <= startTime.day)and (v["Bis"].month <= startTime.month) and (v["Bis"].year <= startTime.year)
             ):
            del(arbeiter[v["userID"]])
      return arbeiter
   
   Weekday = {0:"Mo",1:"Di",2:"Mi",3:"Do",4:"Di",5:"Fr",6:"Sa",7:"So"}

   def getEinsatzplanCurrentWeek(self):
      t = datetime.today().weekday()
      weekstart = datetime.today() + timedelta(days=-(t+1))
      weekend = datetime.today() + timedelta(days=6-t)
      data  = self.db.searchData(DB_Table.Einsatzplan,"`Von`>='"+str(weekstart)+"' AND `Von` <='"+str(weekend)+"'")
      return data
   def getKrankmeldungCurrentWeek(self,custom:int = 0):
      t = datetime.today().weekday()
      weekstart = datetime.today() + timedelta(days=-(t+1))
      weekend = datetime.today() + timedelta(days=6-t)
      if custom >0:
         data  = self.db.searchData(DB_Table.KrankMeldung,"`Von`>='"+str(weekstart)+"' AND `Von` <='"+str(weekend)+"' AND `userID`='"+str(custom)+"'")
      else:
         data  = self.db.searchData(DB_Table.KrankMeldung,"`Von`>='"+str(weekstart)+"' AND `Von` <='"+str(weekend)+"'")
      return data
   
   def getEinsatzplan(self,custom:int=0):
      result = {"Mo":{},"Di":{},"Mi":{},"Do":{},"Fr":{}}
      data  = self.getEinsatzplanCurrentWeek()
      arbeiter = self.db.getData(DB_Table.User)
      ### Krankmeldung in derm Plan als rote farbe anzeigen
      krankmeldung = self.getKrankmeldungCurrentWeek(custom)
      ###
      for k,v in data.items():
         if custom != 0 and v["userID"] !=  custom:
            continue
         flag = False
         c = 1
         while not flag:
            if c not in result[self.Weekday[v["Von"].weekday()]]:
               result[self.Weekday[v["Von"].weekday()]][c] = {}
            if v["Von"].hour in result[self.Weekday[v["Von"].weekday()]][c]:
               c+=1
               continue
            else:
               result[self.Weekday[v["Von"].weekday()]][c][v["Von"].hour] = {"Bis":v["Bis"].hour,"Ort":v["Ort"],"Type":v["Type"],"Name":v["Name"],"Vnr":k,"Arbeiter":arbeiter[v["userID"]]["Nachname"]} 
               flag = True

      tmp = result # Ausgabe Sortieren
      for k,v in result.items():
         for ke,ve in v.items():
            tmp[k][ke] = dict(sorted(tmp[k][ke].items()))
         tmp[k] = dict(sorted(tmp[k].items()))
      result = tmp
      return result