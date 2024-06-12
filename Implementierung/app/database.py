# coding: utf-8

import os
import codecs
import json
import datetime
import enum
from xml.etree.ElementTree import tostring
import mysql.connector
from ast import literal_eval


from .Tables.basetable import *


class DB_Table():
   Markt = "Markt",
   KrankMeldung = "krankmeldung"
   Einsatzplan = "Veranstaltungen"
   User = "User"


dbconfig = {
   "host":"localhost",
   "user":"SysUser",
   "password":"0EfwxC[Y3v51Sh20",
   "database":"swe",
   "autocommit":True
}

#----------------------------------------------------------
class Database_cl(object):
#----------------------------------------------------------
   #connectionPool = mysql.connector.pooling.MySQLConnectionPool(20,"test",True,**dbconfig)
   
   # pylint: disable=E1101
   #-----------------------   --------------------------------
   def __init__(self):
   #-------------------------------------------------------
      self.database =  mysql.connector.connect(host="h2988575.stratoserver.net",user="DnD5e",password="fjgazve3cSJSecCnoaMwOUfau",database="DnD5e")
      self.database.autocommit = True
      
      self.tables = {}
      self.tables[DB_Table.KrankMeldung] = KrankMeldung_cl()
      self.tables[DB_Table.Einsatzplan] = Einsatzplan_cl()
      self.tables[DB_Table.User] = User_cl()
      baseTable_cl.database = self.database


      
   def createConnection(self):
      self.database.close()
      self.database = mysql.connector.connect(**dbconfig)
      return

   def getData(self,table,querySelector="*",id = None,skip = False):
      #try:
         data = self.tables[table].getData(querySelector,skip)
         return data
      #except:
       #  return 0#cherrypy.HTTPError(500,"Data not found")



   def resolveForiegnKey(self,result,collumn,table):
      for k,v in result:
         if k == collumn:
            query = "`"+collumn+"`="
            if type(v) is int:
               query+=str(v)
            else:
               query+="'"+v+"'"     
            result.update(self.searchData(table,query))
         if type(v) is dict:
            v = self.resolveForiegnKey(v,collumn,table)  
         
      return result


   def searchData(self,table,search):
      try:
         return self.tables[table].searchData(search)
      except Exception as e:
         print(e)
         return {}
    


   def searchDataNew(self,table,colums,values):
      try:
         return self.tables[table].searchDataNew(colums,values)
      except Exception as e:
         print(e)
         return {}
   
   
   def searchWhereIdIn(self,table,column,dblist):
      a = list("(")
      for x in dblist:
         a.append(str(x[column]))
         a.append( ",")
      a[len(a)-1] = ")"
      return self.db_o.searchData(table,"`ID` in "+"".join(a))


   def updateData(self,table,data,insert=False):
      try:
         if insert:
            self.tables[table].insertData(data)
         else:
            self.tables[table].updateData(data,insert) 
         return 
      except Exception as e:
         print(e)
         
   def deleteEntry(self,table,search):
      try:
         return self.tables[table].deleteData(search)
      except Exception as e:
         print(e)
      
   def getStructur(self,table):
      mycursor = self.database.cursor()
      mycursor.execute("SHOW COLUMNS FROM "+table)
      columns = mycursor.fetchall()
      self.database.commit()
      retVal = {}
      for s in columns:
         retVal[s]=''
      return retVal

