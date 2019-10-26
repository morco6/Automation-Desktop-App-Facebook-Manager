# -*- coding: utf-8 -*-
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import xerox


class NewPost:
    """
    * Represent the process of posting new post in selected group.
    """
    
    def __init__(self, driver, url, sleep, img, data):
        self.driver = driver    #browser driver
        self.url = url          #link address of selected group page
        self.sleep = sleep      #sleep function
        self.attempts = 3       #max attempts
        self.tries = 0          #counter
        self.success = 0        #flag
        self.img = img          #file list of paths to images and videos
        self.data = data.encode().decode('utf-8')

    def runNoIMG(self):
        self.driver.get(self.url)
        if(self.keepTrying(self.findPostBox, "text box..")):
            for x in range(0,10):
                xerox.copy(self.data)
            self.sleep(2)
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform() #Step 2.
            return (self.keepTrying(self.findPostButton, "submit button.."))
            
    def runOneIMG(self):
        self.driver.get(self.url)
        if(self.keepTrying(self.findPostBox, "text box..")):
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            if(self.keepTrying(self.switchToImgTab, "image tab..")):
                if(self.addImg()):
                    return (self.keepTrying(self.findPostButtonIMG, "submit button.."))
                
    def runFewIMG(self):
        self.driver.get(self.url)
        if(self.keepTrying(self.findPostBox, "text box..")):
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            if(self.keepTrying(self.switchToImgTab, "image tab..")):
                if(self.addImg()):
                    if(self.secondIMGs()):
                        return (self.keepTrying(self.findPostButtonIMG, "submit button.."))
        
    def keepTrying(self, func, actionName):
        """
        * A decorator that keep looking for each element
        * at each selected page (depends the received function).
        * Received functions: findPostBox, findPostButton.
        """
        while(self.tries < self.attempts):
            try:
                print("Trying to find the " + actionName)
                res = func()
                self.success = 1
            except:
                self.tries += 1
                print("%d/%d Attempt Failed! - trying again" % (self.tries, self.attempts))
                continue
            if(self.success):
                print("Success!")
                res.click()
                return 1
        return 0
    
    def findPostBox(self):
        #Step 1.
        self.sleep(2)
        xpath = "//*[@id='pagelet_group_composer']"
        WebDriverWait(self.driver, 15).until(visibility_of_element_located((By.XPATH, xpath)))
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return(self.driver.find_element_by_xpath(xpath))#for friend xhpc
 
    def findPostButton(self):
        self.sleep(2)
        #ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(u'\ue007').key_up(Keys.CONTROL).perform()
        xpath = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div/div[2]/button"
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return(self.driver.find_element_by_xpath(xpath))#for friend //*[@id='js_3']/div[2]/div[3]/div/div[2]/div/button        
        
    def findPostButtonIMG(self):
        self.sleep(2)
        xpath = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/span/button"
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return(self.driver.find_element_by_xpath(xpath))
        
    def switchToImgTab(self):
        xpath = "//*[@id='rc.u_0_1x']/div[1]/div/div[1]/div/ul/li[2]/a"
        return(self.driver.find_element_by_xpath(xpath))
        
    def addImg(self):
        xpath_to_upload_button = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div[1]/table/tbody/tr/td[1]/div/a/div[2]/input"
        c=10
        while(c>0):
            try:
                self.driver.find_element_by_xpath(xpath_to_upload_button).send_keys(os.path.abspath(self.img[0]))
                return 1
            except:
                c-=1
                continue
        return 0
    
    def secondIMGs(self):
        i=1
        xpath = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div/div/div/div[1]/div/div/span/div/a/div/input"
        while(i<(len(self.img))):
            for x in range(0,3):
                try:
                    self.driver.find_element_by_xpath(xpath).send_keys(os.path.abspath(self.img[i]))
                    break
                except:
                    continue
            i+=1
        return 1
    
    def set_driver(self, driver):
        self.driver = driver
        
    def set_url(self, url):
        self.url = url
        
    def set_fileList(self, fList):
        self.img = fList