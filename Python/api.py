# -*- coding: utf-8 -*-
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import gevent #for better sleep function (NodeJS - special case)
from Login import Login
from Groups import Groups
import sys
import zerorpc

class pyApi(object):
    """
    * The api class for communication between nodeJS and Python.
    * Each method exposed to nodeJS such that nodeJS can call
    * to specific method of this class.
    * Methods with the property "@zerorpc.stream", are streaming
    * data from generator function.  
    """

    def __init__(self):
        """
        * Initialize the reqire objects.
        * Selenium use the firefox driver.
        """
        self.options = Options()
        self.options.set_preference("dom.webnotifications.enabled", False) #Clear Notifications and Alerts
        self.driver = webdriver.Firefox(firefox_options = self.options)
        #self.driver.set_window_position(10000,0)
        self.group = Groups(self.driver, gevent.sleep)
        self.login = None

    ################- Login -################
    def serverLoginRequest(self, details):
        details = json.loads(details)
        self.login = Login(details["serial"], details["password"], self.driver)
        self.driver.get(self.login.url)
        return self.login.loginToServer()
    
    def facebookLoginRequest(self):
        return self.login.login_to_facebook(gevent.sleep)

    def getProfileDetails(self):
        return self.login.getProfileDetails(self.driver)
    ##########################################

    ##############- Collecting groups -############## 
    def init_collect(self):
        try:
            if(self.driver.current_url != self.group.adrs):
                self.driver.get(self.group.adrs) 
            return self.group.click_show_more()
        except Exception as e:
            return e  

    @zerorpc.stream
    def collect(self):
        try:
            return self.group.collect()
        except Exception as e:
            return e     

    def exportJSON(self):
        return self.group.export_json_group_list() #export json file with the group list
    ##############################################

    ################- Join Groups -############### 
    
    def init_groups_to_join(self, url):
        return self.group.get_groups_to_join(url) 

    def join_group(self):
        if(self.group.pop_g()):#there is more groups?
            self.group.click_join()
            return True
        return False
            
    def isForm(self):
        if(not self.group.catch_form()):
            if(not self.group.catch_dialog()):
                return self.group.get_group_details()
        return True
    
    def fillForm(self):
        try:
            isFill = self.group.catch_and_fill_text_area()
            if(isFill):
                self.group.click_submit_form()
        except Exception as e:
            return e
        try:
            isClose = self.group.exit_form_and_popup()
            if(isClose):
                return self.group.get_group_details()
        except Exception as e:
            return e
        return False
    
    ##########################################

    ################- Posting -###############
    def post(self, url, fileList, data):
        return self.group.run(url, fileList, data)

    def linkToPost(self):
        return self.group.getLinkToPost()

    def echo(self, details):
        return details

#######################################################
#####################- Open Host -#####################
#######################################################
def parse_port():
    port = 4244
    try:
        port = int(sys.argv[1])
    except:
        pass
    return '{}'.format(port)

def main():
    """
    * Main function - open server with zerorpc module.
    * Method: tcp.
    * Server: localhost.
    * Port: 4242.
    """
    addr = 'tcp://127.0.0.1:' + parse_port()
    s = zerorpc.Server(pyApi())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
    