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
            data = self.getAvailablePersonal(arg1,arg2,arg3,Voredit=int(arg4))
         else:
            data = self.getEinsatzplan(0)
            data["extra"] = '<button data-action="edit">Edit</button>'+'<button data-action="create">Veranstaltung erstellen</button>'+'<button data-action="print">Plan ausdrucken</button>'

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
      
   def getAvailablePersonal(self,startTime,endTime,location,Voredit = 0):
      arbeiter = self.db.searchData(DB_Table.User,"`Rolle`='Arbeiter'")
      for v in arbeiter.values():
         v["Arbeitszeit"] = 0
      krankmeldungen = self.db.getData(DB_Table.KrankMeldung)
      veranstaltungen = self.getEinsatzplanCurrentWeek()
      timeNeed = abs(endTime.hour - startTime.hour)

      for k,v in veranstaltungen.items():
         if (v["Von"].month != startTime.month) or (v["Von"].year != startTime.year) or k == Voredit: 
            continue
         arbeiter[v["userID"]]["Arbeitszeit"] += abs(v["Bis"].hour-v["Von"].hour)
         if arbeiter[v["userID"]]["Arbeitszeit"] + timeNeed > 16:
            del(arbeiter[v["userID"]])
            continue 

      for k,v in veranstaltungen.items():
         if (v["Von"].day != startTime.day)or (v["Von"].month != startTime.month) or (v["Von"].year != startTime.year) or k == Voredit:
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
            if v["userID"] in arbeiter:
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
      result = {"Mo":{},"Di":{},"Mi":{},"Do":{},"Fr":{},"Sa":{},"So":{}}
      data  = self.getEinsatzplanCurrentWeek()
      arbeiter = self.db.getData(DB_Table.User)
      ### Krankmeldung in derm Plan als rote farbe anzeigen
      krankmeldung = self.getKrankmeldungCurrentWeek(custom)
      ###
      for k,v in data.items():
         if (custom != 0 and v["userID"] !=  custom) or v["userID"] == 0:
            continue
         flag = False
         c = 1
         while not flag:
            if c not in result[self.Weekday[v["Von"].weekday()]]:
               result[self.Weekday[v["Von"].weekday()]][c] = {}
            flag2 = True
            for ke,ve in result[self.Weekday[v["Von"].weekday()]][c].items():
               # 
               if (v["Von"].hour >= ke and v["Von"].hour <= ve["Bis"]) or (v["Bis"].hour <= ve["Bis"] and v["Bis"].hour >= ke) or (v["Von"].hour <= ke and v["Bis"].hour >= ve["Bis"]):
                  c+=1
                  flag2 = False
            if not flag2: continue
            result[self.Weekday[v["Von"].weekday()]][c][v["Von"].hour] = {"Bis":v["Bis"].hour,"Ort":v["Ort"],"Type":v["Type"],"Name":v["Name"],"Vnr":k,"Arbeiter":arbeiter[v["userID"]]["Nachname"],"Krank":0} 
            for ve in krankmeldung.values():
               if(v["userID"]==ve["userID"] and(v["Von"].day >= ve["Von"].day and v["Von"].day <= ve["Bis"].day) 
               and (v["Von"].month >= ve["Von"].month and v["Von"].month <= ve["Bis"].month)
               and(v["Von"].year >= ve["Von"].year and v["Von"].year <= ve["Bis"].year)):
                  result[self.Weekday[v["Von"].weekday()]][c][v["Von"].hour]["Krank"] = 1
            flag = True

      tmp = result # Ausgabe Sortieren
      for k,v in result.items():
         for ke,ve in v.items():
            tmp[k][ke] = dict(sorted(tmp[k][ke].items()))
         tmp[k] = dict(sorted(tmp[k].items()))
      result = tmp
      return result