import mysql.connector as sql
import os
import time
import getpass

class Database:
    databaseName = 'torPenetrator'
    tableName = 'searchResult'
    conn = None
    cursor = None
    
    def __init__(self) -> None:
        self.connect()

    def __del__(self) -> None:
        self.disconnect()

    def connect(self) -> None:
        try:
            os.system("service mariadb restart")
            print("\nEnter mariaDB credentials to store the results:")
            hostName = input('Enter host: ')
            userName = input('Enter username: ')
            userPass = getpass.getpass("Enter password: ")

            try:
                self.conn = sql.connect(host = hostName, user = userName, password = userPass)

            except:
                print('Invalid Credentials!!!')
                print('Access Denied')
                exit()
            
            del userPass

            if self.conn.is_connected():
                print("\nMariaDB: Connected")

            self.cursor = self.conn.cursor()

            sqlQuery = f'CREATE DATABASE IF NOT EXISTS {self.databaseName};'
            self.cursor.execute(sqlQuery)

            sqlQuery = 'USE torPenetrator;'
            self.cursor.execute(sqlQuery)

            sqlQuery = f'CREATE TABLE IF NOT EXISTS {self.tableName} (Sno INT AUTO_INCREMENT PRIMARY KEY, SiteTitle VARCHAR(200) NOT NULL, SiteUrl VARCHAR(200) NOT NULL UNIQUE, SearchEngine VARCHAR(50) NOT NULL, Query VARCHAR(100) NOT NULL, ExtractTime TIMESTAMP NOT NULL);'
            self.cursor.execute(sqlQuery)
        
        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured while connecting\nError: ', e)
            exit()

    def disconnect(self) -> None:
        flag = 0
        attempt = 0
        print()

        try:
            while flag != 1 and attempt < 3:
                self.conn.close()
                
                if self.conn.is_connected():
                    print("MariaDB: Still Connected")
                    attempt += 1
                else:
                    print("MariaDB: Disconnected")
                    flag = 1
            
        except:
            print("Exception occured while Disconnecting")
    
    def insertData(self, dataDict:dict) -> None:
        try:
            sqlQuery = f'INSERT INTO {self.tableName} (SiteTitle, SiteUrl, SearchEngine, Query, ExtractTime) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP());'

            val1 = []
            val2 = []
            val3 = []
            val4 = []
            ind = 0

            for i in dataDict.keys():
                
                for j in dataDict[i]:
                    
                    if ind == 0:
                        val1.append(j)
                    
                    if ind == 1:
                        val2.append(j)
                        
                    if ind == 2:
                        val3.append(j)

                    if ind == 3:
                        val4.append(j)
                    
                ind += 1
                
            insCount = 0
            dup = 0

            for i in range(len(val1)):

                try:
                    value = [val1[i], val2[i], val3[i], val4[i]]
                    self.cursor.execute(sqlQuery, value)
                    insCount += 1
                    self.conn.commit()

                except sql.IntegrityError:
                    dup += 1
                    data = self.getAllRecords()
                    totalRows = len(data)
                    aiQuery = f"ALTER TABLE {self.tableName} AUTO_INCREMENT = {totalRows}"
                    self.cursor.execute(aiQuery)
                    self.conn.commit()
                    continue

            print(f"\n{dup} duplicate url(s) skipped")
            print(f"\n{insCount} row(s) inserted successfully")

        
        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured while inserting\nError: ', e)
            exit()

    def getAllRecords(self) -> list:
        try:
            sqlQuery = f'SELECT * FROM {self.tableName}'
            self.cursor.execute(sqlQuery)

            data = self.cursor.fetchall()

        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured while fetching records\nError: ', e)
            exit()
            
        return data
    
    def getColumn(self, columnNumber:int) -> list:
        try:
            dataList =[]
            sqlQuery = f'SELECT * FROM {self.tableName}'
            self.cursor.execute(sqlQuery)

            data = self.cursor.fetchall()

            for row in data:
                colind = 0
                for col in row:
                    colind += 1
                    if colind == columnNumber:
                        dataList.append(col)
        
        except KeyboardInterrupt:
            print("\nKeyboard interruption occurred")
            print("Exiting program...")
            time.sleep(1)
            exit()

        except Exception as e:
            print('Exception occured while fetching records\nError: ', e)
            exit()

        return dataList
