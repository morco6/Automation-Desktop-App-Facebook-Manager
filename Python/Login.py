# -*- coding: utf-8 -*-
import psycopg2
import browsercookie
from DBCon import DB

class Login:
    """
    * Login class.
    * responsible for the login section.
    """
    
    url = 'https://www.facebook.com'
    facebook = 0
    
    def __init__(self, serial, pss, driver):
        self.serial = serial
        self.pss = pss
        self.expired_date = None
        self.driver = driver
        
    def get_cookie(self, cj, cts):
        """
        * cj: cookie jar. cts: cookie_to_send.
        * scan all cookies of firefox/chrome browser and look for 
        * facebook cookie.
        """
        for cookie in cj:
            if(cookie.domain == '.facebook.com'):
                tmp = {}
                tmp['name'] = cookie.name
                tmp['value'] = cookie.value
                cts.append(tmp)
        if(len(cts) == 0):
            raise "cookie not found"
        else:
            return cts
            
    def login_to_facebook(self, sleep):
        """
        * use the cookies of the user to login to facebook.
        """
        cookies_to_send = []
        try:
            cookies = self.get_cookie(browsercookie.chrome(),cookies_to_send)#cookie_jar and list
            print("chrome")
        except:    
            cookies = self.get_cookie(browsercookie.firefox(),cookies_to_send)
            print("firefox")
        if(len(cookies)>0):
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.get(self.url)
            facebook_success = { "status": True }
            return facebook_success
        else:
            facebook_failed =  { "status":False, "err1":"החיבור אל פייסבוק נכשל - יתכן שאינך מחובר", "err2":"*פתח את דפדפן chrome או firefox והתחבר אל פייסבוק"}
            return facebook_failed #server failed
    
    def loginToServer(self):
        """
        * User authentication by connecting to the heroku server.
        * DB - PostgreSQL.
        """
        try:
            db = DB()
            db.connect()
            record = db.login(self.serial, self.pss)
        except Exception as e:
            return e
        finally:
            db.close() 
        if(record): 
            if(record[0][6] < record[0][7]):
                self.expired_date = record[0][7]
                server_success = {"status":True}
                return server_success
            else:
                expired = { "status":False, "err1":"רשיון פג תוקף", "err2":"*חדש את רשיונך על מנת לבצע כניסה"}
                return expired 
        else:
            server_failed = { "status":False, "err1":"רשיון לא קיים במערכת", "err2":"*נסה להקליד שנית את מספר הרשיון והסיסמא"}
            return server_failed 

    def getProfileDetails(self, driver):
        try:
            profileTag = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div[1]/div/div/form/div[1]/div/div[1]/a/div")
        except Exception as e:
            return e
        profilePicture = profileTag.find_element_by_tag_name("img")
        expired_day = self.expired_date.day
        expired_month = self.expired_date.month
        expired_year = self.expired_date.year
        expired = ("%d/%d/%d" % (expired_day, expired_month, expired_year))
        profileDetails = {
            "profileName": profilePicture.get_attribute("aria-label"),
            "profilePicture": profilePicture.get_attribute("src"),
            "serial": self.serial,
            "expired": expired
        }
        return profileDetails