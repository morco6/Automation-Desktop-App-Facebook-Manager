# -*- coding: utf-8 -*-
import psycopg2
import datetime
#NOTE:There must be a comma after ONLY ONE VALUE to make that a tuple

class DB:
    
    __database = "da4veoebvjlm9m"
    __user = "disqvoztoselhf"
    __password = "0c7f303f6b2b56c4702a57b671ea75c41c0218fc72686a9aee3b1f0f4bb682d4"
    __host = "ec2-54-217-206-65.eu-west-1.compute.amazonaws.com"
    __port = "5432"
    
    def __init__(self):
        self.__connection = None
        self.__cursor = None
    
    def connect(self):
        self.connection = psycopg2.connect(database = "da4veoebvjlm9m", user = "disqvoztoselhf", password = "0c7f303f6b2b56c4702a57b671ea75c41c0218fc72686a9aee3b1f0f4bb682d4", host = "ec2-54-217-206-65.eu-west-1.compute.amazonaws.com", port = "5432")
        try:
            self.cursor = self.connection.cursor()
            return self.cursor
        except (Exception, psycopg2.Error) as e:
            return e
        
    def close(self):
        self.cursor.close()
        self.connection.close()
        return("PostgreSQL connection is closed")
        
    def login(self, serial, password):
        query = "SELECT * FROM CLIENTS where sn=%s and password=%s and availble=true"
        try:
            self.cursor.execute(query, (serial, password))
            record = self.cursor.fetchall()
            return record
        except (Exception, psycopg2.Error) as e :
            return e
        
        
        
        