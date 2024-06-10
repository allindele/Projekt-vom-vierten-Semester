import json
from time import time
import  mysql.connector
import mysql.connector.pooling

dbconfig = {
   "host":"localhost",
   "user":"SysUser",
   "password":"0EfwxC[Y3v51Sh20",
   "database":"swe",
   "autocommit":True
}


class baseTable_cl():

    def __init__(self,tabel = ""):
        self.table = tabel
        self.columns = self.getColumnsData()


    def getRawData(self,items,columns):
        result = []
       
        for x in items:
            i=0
            tmp = {}
            for s in columns:
                tmp[s[0]] = x[i]
                i+=1
            result.append(tmp)
        return result
    

    def combineData(self,items,columns,skip=0):

        return 0

    def getColumnsData(self):
        connection = mysql.connector.connect(**dbconfig)
        mycursor = connection.cursor()
        mycursor.execute("SHOW COLUMNS FROM "+self.table)
        columns = mycursor.fetchall()
        connection.commit()
        mycursor.close()
        connection.close()
        return columns

    def resolveForiegnKey(self,result):
        
        return result


    def getData(self,skip = False):  #missing json resolver
        
        connection = mysql.connector.connect(**dbconfig)
        #connection = baseTable_cl.connectionPool.get_connection()
        mycursor = connection.cursor()
        #mycursor = baseTable_cl.database.cursor()

        mycursor.execute("SELECT * FROM "+self.table)
        items = mycursor.fetchall()
        connection.commit()
        mycursor.close()
        connection.close()
        try:
            if id == None:
                result = self.combineData(items,self.columns)
            else:
                result = self.combineData(items,self.columns,1)
        except:
            print("Failed to Combine date with Columns")
               
        return result
    


    def searchData(self,search):
        result = []

        connection = mysql.connector.connect(**dbconfig)
        mycursor = connection.cursor()

        mycursor.execute("SELECT * FROM "+self.table+" WHERE "+search)
        items = mycursor.fetchall()
        connection.commit()
        result = self.combineData(items,self.columns)
        #self.resolveForiegnKey(result)
        mycursor.close()
        connection.close()
        return result
    
    def deleteData(self,search):
        connection = mysql.connector.connect(**dbconfig)
        mycursor = connection.cursor()

        mycursor.execute("DELETE FROM "+self.table+" WHERE "+search)
        connection.commit()
        mycursor.close()
        connection.close()


    def searchDataNew(self,columns,values):
        if len(columns) != len(values):
            raise ValueError("Columns lenght missmatch values lenght")
        result = []
        search = " Where "
        for k in range(0,len(columns)):
            if k >0:
                search += " AND "
            search += "`" + columns[k]+"`="
            if type(values[k])==int:
                search+=str(values[k])
            else:
                search+="'"+values[k]+"'"
            
        connection = mysql.connector.connect(**dbconfig)
        mycursor = connection.cursor()

        mycursor.execute("SELECT * FROM "+self.table+search)
        items = mycursor.fetchall()
        connection.commit()

        mycursor.close()
        connection.close()

        result = self.combineData(items,self.columns)
        #self.resolveForiegnKey(result)
        return result

   
    def updateData(self,data,insert = 0): #rework needed
        if insert:
            updateType = "INSERT "
        else:
            updateType = "UPDATE "

        connection = mysql.connector.connect(**dbconfig)
        mycursor = connection.cursor()

        sqlQuery = updateType + self.table
        if(updateType == "INSERT "):
            sqlQuery += " VALUES( "
        else:
            sqlQuery += " SET "

        for c in data.keys():
            sqlQuery += c + "='"+str(data[c])+"', "
        sqlQuery=sqlQuery[:len(sqlQuery)-2] 
        if(updateType == "INSERT "):
            sqlQuery+= ')'
        else:
            sqlQuery += self.getUpdateString(data)
            #sqlQuery += " Where ID=" + str(data["ID"])
        print(sqlQuery)
        mycursor.execute(sqlQuery)
        connection.commit()

        mycursor.close()
        connection.close()
        return 
    
    def insertData(self,data):
        connection = mysql.connector.connect(**dbconfig)
        mycursor = connection.cursor()

        query = "INSERT INTO `"+self.table+"` ("
        key = ""
        value = ""
        for k,v in data.items():
            key += "`"+k+"`,"
            if type(v) == int:
                value += str(v)+","
            else:
                value += "'"+v+"',"
        key = key[:len(key)-1]
        value = value[:len(value)-1]
        query += key + ") VALUES (" + value + ");"
        print(query) 
        mycursor.execute(query)
        connection.commit()
        mycursor.close()
        connection.close()
        return


    def getUpdateString(data):
        return "Where `ID`=0"

class Fachbereich_cl(baseTable_cl):
    def __init__(self):
        super().__init__("Item_db")

    def combineData(self,items,columns,skip=0):
        result = {}
       
        for x in items:
            result[x[0]] = {
                "Wert":x[1],
                "Anz2LE":x[2],
                "Quality":x[3],
                "Discription":x[4],
                "Standart":x[6]
            }
        return result
    
    def getUpdateString(self,data):
        return "Where `Name`='"+data["Name"]+"'"
        
class Veranstaltung_cl(baseTable_cl):
    def __init__(self):
        super().__init__("Veranstaltung")

    def combineData(self,items,columns,skip=0):
        result = {}
       
        for x in items:
            result[x[0]] = {
                columns[1][0]:x[1],
                columns[2][0]:x[2],
                columns[3][0]:x[3],
                columns[4][0]:x[4],
                columns[5][0]:x[5]
            }
        return result
    
    def getUpdateString(self,data):
        return "Where `VNr`='"+data["VNr"]+"'"

class KrankMeldung_cl(baseTable_cl):
    def __init__(self):
        super().__init__("krankmeldung")

    def combineData(self,items,columns,skip=0):
        result = {}
       
        for x in items:
            result[x[0]] = {
                columns[1][0]:x[1],
                columns[2][0]:x[2],
                columns[3][0]:x[3]
            }
        return result
    
    def getUpdateString(self,data):
        return "Where `Knr`='"+data["Knr"]+"'"

class Einsatzplan_cl(baseTable_cl):
    def __init__(self):
        super().__init__("veranstaltung")

    def combineData(self,items,columns,skip=0):
        result = {}
       
        for x in items:
            result[x[0]] = {
                columns[1][0]:x[1],
                columns[2][0]:x[2],
                columns[3][0]:x[3],
                columns[4][0]:x[4],
                columns[5][0]:x[5]
            }
        return result
    
    def getUpdateString(self,data):
        return "Where `Vnr`='"+data["Vnr"]+"'"
        
