# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from random import randint
import constant as const
import asyncio
from textblob import TextBlob

class JoinGroup:
    """
    * Take care of join groups scenarios.
    * - get the catagory url
    * - scrap the groups table, and loop on it.
    * - for each cell(group), press on join button.
    * - It may appear a popup form to fill.
    * - If there is a form to fill, then then fill,click the right areas.
    * - If form filling is complete, then submit.
    * - If could not deal with the form scenario, then exit form.
    *   Don't worry, the form will be sent anyway :)
    """
    def __init__(self, driver, sleep, url):
        self.driver = driver
        self.sleep = sleep
        self.url = url
    
    async def catch_dialog(self):
        """
        * Try to catch form if popup happen. 
        """
        await asyncio.sleep(self.randDelay())
        btns = self.driver.find_elements(By.TAG_NAME, "button")
        for btn in btns:
            if (btn.text == "סגור" or btn.text == "close" or btn.text == "Close"):
                go_to_parent = '..'
                for x in range(0,10):
                    form = btn.find_element_by_xpath(go_to_parent)
                    try:
                        form = form.find_element_by_xpath('//div[@aria-label="השבה לשאלות"]')
                        return form
                    except:
                        go_to_parent += '/..'
                        continue                            
        return False
    
    async def catch_form(self):
        """
        * Try to catch form if popup happen. 
        """
        await asyncio.sleep(self.randDelay())
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        for form in forms:
            text_area_list = form.find_elements(By.TAG_NAME, "textarea")
            if(len(text_area_list)>0):
                return form
        return None

    async def loop_text_area(self, form):
        """
        * Try to list text box's, click on each of them,
        * detect the language and send random keys with same language.
        * May raise Exception: x.find_..., x.click(), x.send_keys.
        """
        await asyncio.sleep(self.randDelay())
        try:
            text_area_list = form.find_elements(By.TAG_NAME, "textarea")
        except:
            return False
        if(len(text_area_list)>0):
            for text_box in text_area_list:
                try:
                    text_box_title = text_box.find_element_by_xpath('../..').text
                    blob = TextBlob(text_box_title)
                    text_box.click()
                    if(blob.detect_language()=='iw'):#iw means hebrew
                        text_box.send_keys(const.HEB[randint(0,len(const.HEB)-1)])
                    else:
                        text_box.send_keys(const.ENG[randint(0,len(const.ENG)-1)])
                except:
                    text_box.send_keys(const.ENG[randint(0,len(const.ENG)-1)])
                await asyncio.sleep(self.randDelay())
            return True
        return False
            
    async def click_on_radio_btn(self, form):
        """
        * Select one option at each radio group if exist.
        * If there is only two choices, then probably it's "yes" and "no".
        * Else, then random a choice from the choices list. 
        """
        await asyncio.sleep(self.randDelay())
        try:
            radio_btn_list = form.find_elements_by_xpath('//div[@role="radiogroup"]')
        except:
            return False
        for btn in radio_btn_list:
            choices = btn.find_elements(By.TAG_NAME, "label")
            if(len(choices)==2):
                for c in choices:
                    if(c.text == "Yes" or c.text == "כן"):
                        c.click()
            else:
                choices[randint(0,len(choices)-1)].click()
            
            await asyncio.sleep(self.randDelay())
        return True
    
    async def submit_form(self, form):
        """
        * Complete the form stage by click on Submit button.
        """
        await asyncio.sleep(self.randDelay())
        btns_in_form = form.find_elements(By.TAG_NAME, "button")#find submit form btn
        for btn in btns_in_form:
            if((btn.text == "שלח") or (btn.text == "Submit")):
                btn.click()#confirm form
                return True
        return False
    
    async def close_form(self):
        """
        * After form complete facebook may display popup dialog.
        * This method will close it.
        """
        await asyncio.sleep(self.randDelay())
        btns = self.driver.find_elements(By.TAG_NAME, "button")
        for btn in btns:
            if (btn.text == "סגור" or btn.text == "close" or btn.text == "Close"):
                btn.click()
                try:
                    await asyncio.sleep(self.randDelay())
                    closeList = self.driver.find_elements(By.TAG_NAME, "a")
                    for closeBtn in closeList:
                        if(closeBtn.text == "סגור" or closeBtn.text == "close" or closeBtn.text == "Close"):
                            closeBtn.click()
                except:
                    await asyncio.sleep(self.randDelay())
                return True
        return False
    
    def get_group_details(self, cell):
        """
        * Returns: name, friends amount and post per x (x = (day or week))
        * of current group.
        """
        span_list = cell.find_elements(By.TAG_NAME, "span")
        details = span_list[1].text.split("•")
        data = {"name":span_list[0].text, 
                "friends":self.convertToNum(details[0]), 
                "posts":details[1]}
        return data
    
    def convertToNum(self, txt):
        if 'k' in txt:
            return float(txt.replace('k', ''))*1000
        return float(txt.replace('M', ''))*1000000 if 'M' in txt else int(txt)
    
    async def scrollDown(self):
        """
        * Dynamic page scroll down 
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            await asyncio.sleep(self.randDelay())
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
    def randDelay(self):
        return randint(const.MIN_SIMPLE_ACTION, const.MAX_SIMPLE_ACTION)