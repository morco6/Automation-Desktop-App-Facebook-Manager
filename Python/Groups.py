# -*- coding: utf-8 -*-
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from NewPost import NewPost
from Join import JoinGroup
import json
import asyncio
from random import randint
import codecs
import constant as const

class Groups:
    """
    * The class deals with the groups tasks.
    * Collect and receive groups information automatic by bot scrapper
    * or by list (json file) from the user.
    * In addition, responsible for posting on each group.
    """
    
    adrs = "https://www.facebook.com/groups"
    groups = {}             #the collected groups
    
    def __init__(self, driver, sleep, jsn_file=None):
        self.driver = driver
        self.sleep = sleep
        self.currentPost = None
        self.tds = []
        self.form = None
        self.cell = None
        if(jsn_file):
            self.load_json(jsn_file)
    
    
    def click_show_more(self):
        """click on 'show more' button """
        try:
            try:
                load_more = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[1]/div[1]/div[1]/div/div[1]/div/div/div[3]/div[2]/a/div")
            except:
                load_more = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[1]/div[1]/div[1]/div/div[1]/div/div/div[4]/div[2]/a/div")
            load_more.click()
            return False #that means there is more to click
        except:
            return True #that means there is no more to click
        
        
    def collect(self):
        """
        * Step 2: collect each group data (name, url and picture).
        * looking for the <div> tag that contains the group
        * list of the facebook account.
        * Data: dict{name:[url, picture]} (self.groups)
        * Streaming the number of the collected groups back to nodeJS.
        """
        counter = 0
        not_complete = "could not complete the collecting process" #message for exception
        try:
            div = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[1]/div[1]/div[1]/div/div[1]/div/div/div[4]/div[2]")
        except:
            div = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[1]/div[1]/div[1]/div/div[1]/div/div/div[3]/div[2]")
        lst = div.find_elements_by_tag_name("a")
        for g in lst:
            name = g.text
            url = g.get_attribute("href")
            url = url.replace("/?ref=group_browse", '')
            try:
                picture = g.find_element_by_tag_name("img")
                picture = picture.get_attribute("src")
                self.groups[name] = [url, picture]
                counter += 1
                yield counter   
            except:
                yield not_complete 
    
    
    def run(self, url, fileList, data):
        """
        * Post on facebook group.
        """
        if(self.currentPost == None):#only one object
            self.currentPost = NewPost(self.driver, url, self.sleep, fileList, data)
        else:
            self.currentPost.set_driver(self.driver)
            self.currentPost.set_url(url)
            self.currentPost.set_fileList(fileList)
            self.currentPost.sleep = self.sleep
        try:
            if(fileList == []):
                return self.currentPost.runNoIMG()
            elif(len(fileList) == 1):
                return self.currentPost.runOneIMG()
            else:
                return self.currentPost.runFewIMG()
        except Exception as e:
            return e
            
        
    def getLinkToPost(self):
        c=10
        while(c>0):
            try:
                xpath = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[5]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div/span/span/a"
                WebDriverWait(self.driver, 15).until(visibility_of_element_located((By.XPATH, xpath)))
                WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                post = self.driver.find_element_by_xpath(xpath)
                post.click()
                link = self.driver.current_url
                return link
            except: 
                c-=1
                continue
               
                
    def export_json_group_list(self):
        """
        * After the groups collect is done the method will execute a json
        * file with the details of each group.
        """
        to_json_list = []
        for name,values in self.groups.items():
            sample={
                        "pic":"<img class='rounded-circle' src='" +values[1]+ "' width=50px height=50px></img>",
                        "name":name,
                        "status": u" ",
                        "url": values[0]}
            to_json_list.append(sample)
        json_string = json.dumps(to_json_list, ensure_ascii=False) #hebrew support
        file = codecs.open("./Content/groupList.json", "w", "utf-8")
        file.write(json_string)
        file.close()


    def get_groups_to_join(self, url):
        """
        * Prepare the 'join to groups' process.
        """
        self.grp = JoinGroup(self.driver, self.sleep, url)
        self.form = None
        self.driver.get(url)
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.grp.scrollDown())
        except Exception as e:
            return(e)            
        #scrap all groups in page
        xpath_to_table_of_groups = "/html/body/div[1]/div[3]/div[1]/div/div[1]/div[3]/div[2]/div/div/table"
        table = self.driver.find_element_by_xpath(xpath_to_table_of_groups)
        trs = table.find_elements(By.TAG_NAME, "tr")#all rows in table
        for row in trs:#for each row
            trs = row.find_elements(By.TAG_NAME, "td")
            for cell in trs:
                self.tds.append(cell)
        return {"count": len(self.tds)}


    def pop_g(self):
        try:
            self.cell = self.tds.pop(0)#take first group from the list
            return True
        except:
            return False

    
    def click_join(self):
        btn = self.cell.find_element(By.TAG_NAME, "button")
        btn.click()#click to join group     
 
       
    def catch_dialog(self):
        if(self.form != None):
            return True
        try:
            loop = asyncio.get_event_loop()
            self.form = loop.run_until_complete(self.grp.catch_dialog())
            if(self.form != None):
                return True
        except:
            return "error at catch_dialog "
        return False
 
    
    def catch_form(self):
        loop = asyncio.get_event_loop()
        self.form = loop.run_until_complete(self.grp.catch_form())
        if(self.form != None):
            return True
        return False

        
    def catch_and_fill_text_area(self):
        loop = asyncio.get_event_loop()
        try:
            isFill = loop.run_until_complete(self.grp.loop_text_area(self.form))
        except Exception as e:
            return e 
        if(isFill):
            return True
        return False
 
       
    def catch_and_click_radio_buttons(self):
        loop = asyncio.get_event_loop()
        try:
            isClicked = loop.run_until_complete(self.grp.click_on_radio_btn(self.form))
        except Exception as e:
            return e 
        if(isClicked):
            return True
        return False
 
       
    def click_submit_form(self):
        loop = asyncio.get_event_loop()
        try:
            isSubmit = loop.run_until_complete(self.grp.submit_form(self.form))
        except Exception as e:
            return e
        if(isSubmit):
            return True
        return False

            
    def exit_form_and_popup(self):
        loop = asyncio.get_event_loop()
        try:
            isClose = loop.run_until_complete(self.grp.close_form())
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        except Exception as e:
            return e
        if(isClose):
            return True
        return False
 
         
    def get_group_details(self):
        return self.grp.get_group_details(self.cell)

    
    def set_delay(self):
        return randint(const.MIN_SIMPLE_ACTION, const.MAX_SIMPLE_ACTION)
        