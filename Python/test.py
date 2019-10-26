# -*- coding: utf-8 -*-

from Login import Login
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pickle
import browsercookie
import psycopg2
import datetime
import os
from random import randint

'''login'''
options = Options()
options.set_preference("dom.webnotifications.enabled", False)
driver = webdriver.Firefox(firefox_options = options)
driver.get(login.url)

login.login_to_facebook(driver, sleep)
driver.get("https://www.facebook.com/groups/1271242713037977/")

############################################################################
'''post with img'''
xpath_to_postbox = "//*[@id='pagelet_group_composer']"
driver.find_element_by_xpath(xpath_to_postbox).click()
sleep(2)
xpath_to_tab_img_in_postbox = "//*[@id='rc.u_0_1x']/div[1]/div/div[1]/div/ul/li[2]/a"
driver.find_element_by_xpath(xpath_to_tab_img_in_postbox).click()
sleep(2)
xpath_to_upload_button = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div[1]/table/tbody/tr/td[1]/div/a/div[2]/input"
driver.find_element_by_xpath(xpath_to_upload_button).send_keys(os.path.abspath("/home/mor/Documents/Python_Projects/facebookCrawler/images/profile_pic.png"))
sleep(2)
#submit
bxpath = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/span/button"
driver.find_element_by_xpath(bxpath).click()
#more images
xpath_to_more_imgs = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div[1]/div/div[4]/div/div/div/div[1]/div/div/span/div/a/div/input"
driver.find_element_by_xpath(xpath_to_more_imgs).send_keys(os.path.abspath("/home/mor/Documents/Python_Projects/facebookCrawler/images/sa.jpg"))
driver.find_element_by_xpath(xpath_to_more_imgs).send_keys(os.path.abspath("/home/mor/Documents/Python_Projects/facebookCrawler/images/mail.png"))

#link to post
xpath = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[5]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div/span/span/a/abbr/span"
driver.find_element_by_xpath(xpath).click()

############################################################################

'''locate profile picture and name'''
s = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div[1]/div/div/form/div[1]/div/div[1]/a/div")
print(s)
d = s.find_element_by_tag_name("img")
print(d.get_attribute("src"))
profileTag = driver.find_element_by_xpath("//*[@id='u_jsonp_3_f']/div/div[1]/a/div/img")


############################################################################

'''scroll down dynamic'''
def scrollDown(pause_time):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        sleep(pause_time)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def loop_text_area(driver, f):
    text_area_list = f.find_elements(By.TAG_NAME, "textarea")
    if(len(text_area_list)>0):
        for text_box in text_area_list:
            text_box.click()
            sleep(randint(5,15))
            text_box.send_keys("Yes")

def try_to_fill_form(driver):
    print("form")
    forms = driver.find_elements(By.TAG_NAME, "form")
    for f in forms:
        loop_text_area(driver, f)
        try:
            click_on_radio_btn(driver, f)
        except:
            print('None')
        submit_form(driver, f)

def try_to_fill_dialog(driver):
    print("dialog")
    btns = driver.find_elements(By.TAG_NAME, "button")
    for b in btns:
        if (b.text == "סגור" or b.text == "close"):
            f = b.find_element_by_xpath('../..')
            loop_text_area(driver, f)
            try:
                click_on_radio_btn(driver, f)
            except:
                print('None')
            submit_form(driver, f)
        
def click_on_radio_btn(driver, f):
    radio_group = f.find_elements_by_xpath('//div[@role="radiogroup"]')
    for btn in radio_group:
        choise = btn.find_elements(By.TAG_NAME, "label")
        if(len(choise)==2):
            for c in choise:
                if(c.text == "Yes" or c.text == "כן"):
                    c.click()
        else:
            choise[0].click()
        sleep(randint(5,15))

def submit_form(driver, f):
    btns_in_form = f.find_elements(By.TAG_NAME, "button")#find submit form btn
    for btn in btns_in_form:
        if((btn.text == "שלח") or (btn.text == "Submit")):
            btn.click()#confirm form
            return True
    return False

def close_form(driver):
    btns = driver.find_elements(By.TAG_NAME, "button")
    for b in btns:
        if (b.text == "סגור" or b.text == "close"):
            b.click()
            return True
    raise "no close button to form"

            
            
############################################################################

'''login'''
options = Options()
options.set_preference("dom.webnotifications.enabled", False)
driver = webdriver.Firefox(firefox_options = options)
sleep(randint(5,15))
driver.get("https://www.facebook.com/groups")
login = Login("310470705mc","qwew",driver)
login.login_to_facebook(sleep)
'''groups'''
driver.get("https://www.facebook.com/groups")
'''automate group join'''
show_more_proposing_groups = "/html/body/div[1]/div[3]/div[1]/div/div[1]/div[3]/div/div[1]/div/div/div/div[1]/span/a"
sleep(randint(5,15))
'''scroll'''
driver.find_element_by_xpath(show_more_proposing_groups).click()
scrollDown(1)
'''scrap'''
xpath_to_table_of_groups = "/html/body/div[1]/div[3]/div[1]/div/div[1]/div[3]/div[2]/div/div/table"
table = driver.find_element_by_xpath(xpath_to_table_of_groups)
trs = table.find_elements(By.TAG_NAME, "tr")#all rows in table


for row in trs:#for each row
    print(row.text)
    tds = row.find_elements(By.TAG_NAME, "td")#all cells in row
    for cell in tds:
        print(cell.text)
        try:
            btn = cell.find_element(By.TAG_NAME, "button")
            print(btn.text)
            btn.click()#click to join group
            sleep(randint(5,15))
            try:
                try_to_fill_dialog(driver)
                sleep(randint(5,15))
                close_form(driver)
            except:
                None
            sleep(randint(5,15))
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()#exit the confirm popup
        except:
            continue


############################################################################
        
allc = trs[0].find_elements(By.TAG_NAME, "td")#all cells in row
cell = allc[0]
span_list = cell.find_elements(By.TAG_NAME, "span")
group_name = span_list[0].text
details = span_list[1].text.split("•")  
friends_amount = details[0]
posts_per_x = details[1]
print("group name: ", group_name)
print("friends: ", friends_amount)
print("posts: ", posts_per_x)

from Groups import Groups
import gevent
group = Groups(driver, gevent.sleep)
gene = await group.get_groups_to_join("https://www.facebook.com/groups_browse/see_all/?category_id=212609529249058")
group.join_to_group()
############################################################################
tds = trs[0].find_elements(By.TAG_NAME, "td")#all cells in row
btn = tds[0].find_element(By.TAG_NAME, "button")#find btn of cell
btn.click()
'''if there is popup form'''
forms = driver.find_elements(By.TAG_NAME, "form")

def find_all_text_Area_in_dialog(dialog):
    f=None
    text_area_list = []
    for f in dialog:
        try:
            form = f
            print("try to find list of text aera")
            text_area_list = f.find_elements(By.TAG_NAME, "textarea")
            if(len(text_area_list)>0):
                return text_area_list
            if(len(text_area_list) == 0):
                try:
                    text_area_list.append(f.find_element(By.TAG_NAME, "textarea"))
                    return text_area_list
                except:
                    continue
        except:
            continue
    return text_area_list
        
print(text_area_list)   
for text_area in text_area_list:
    print(text_area)
    sleep(1)
    text_area.click()
    sleep(1)
    text_area.send_keys("ok")

send_btn = form.find_element(By.TAG_NAME, "button")
send_btn.click() 
'''need to click ESC button'''


############################################################################
'''test generator'''
from time import sleep
import random

def func():
    lst =["mor1","mor2","mor3","mor4","mor5","mor6","mor7","mor8","mor9"]
    print(len(lst))
    for name in lst:
        x = (random.randint(4,5))*2
        y = (random.randint(8,10))*2
        for n in range(x,y):
            try:
                sleep(2)
                yield name
            except:
                yield "-2"
        yield (name + " finished")
for x in func():
    print(x)
    
    
############################################################################
'''get and save cookies as python object'''

cookies_to_send = []

def get_cookie(cj,cts):
    """
    * cj: cookie jar. cts: cookie_to_send
    * scan all cookies of firefox/chrome browser and look for 
    * facebook cookie.
    """
    for cookie in cj:
        if(cookie.domain == '.facebook.com'):
            print("cookie: ", cookie)
            tmp = {}
            tmp['name'] = cookie.name
            tmp['value'] = cookie.value
            cts.append(tmp)
            #cookie_to_send.append(cookie)
    if(len(cts) == 0):
        raise "cookie not found"
    else:
        return cts

try:
    c = get_cookie(browsercookie.chrome(),cookies_to_send)#cookie_jar and list
    print("chrome")
except:    
    c = get_cookie(browsercookie.firefox(),cookies_to_send)
    print("firefox")

pickle.dump(c , open("cookies.pkl","wb"))

cookies = pickle.load(open("cookies.pkl", "rb"))
print(cookies)
for cookie in cookies:
    driver.add_cookie(cookie)

#driver.add_cookie({'name': 'foo', 'value': 'bar'})
#{'fr': '1DUGYUasu3WrpNF6H..BdYSvs.rV.AAA.0.0.BdYSvs.AWW1St5R', 'sb': '7CthXZme937aMMChoQCyUsTa'}



#name of cols: ['id', 'sn', 'name', 'email', 'phone', 'availble', 'startd', 'endd']

def f():
    record = None
    try:
        connection = psycopg2.connect(database = "da4veoebvjlm9m", user = "disqvoztoselhf", password = "0c7f303f6b2b56c4702a57b671ea75c41c0218fc72686a9aee3b1f0f4bb682d4", host = "ec2-54-217-206-65.eu-west-1.compute.amazonaws.com", port = "5432")
        cursor = connection.cursor()
        query = "SELECT * FROM CLIENTS"
        #query = "ALTER TABLE CLIENTS ADD COLUMN password VARCHAR" #name of columns
        cursor.execute(query)
        #connection.commit()
        colnames = [desc[0] for desc in cursor.description] #name of columns
        record = cursor.fetchall()
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
        if(connection):
            print(record)
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")  
x = f()
print(x)





def update_date(serial, start_date=None, end_date=None):
    """
    update user date
    """
    s_date = datetime.datetime.fromisoformat(start_date)
    e_date = datetime.datetime.fromisoformat(end_date)
    if(s_date >= e_date):
        return false
    try:
        connection = psycopg2.connect(database = "da4veoebvjlm9m", user = "disqvoztoselhf", password = "0c7f303f6b2b56c4702a57b671ea75c41c0218fc72686a9aee3b1f0f4bb682d4", host = "ec2-54-217-206-65.eu-west-1.compute.amazonaws.com", port = "5432")
        cursor = connection.cursor()
                # Update single record now
        sql_update_query = """Update CLIENTS set startd=%s, endd=%s where sn = %s"""
        cursor.execute(sql_update_query, (start_date, end_date, serial))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")
        print("Table After updating record ")
        sql_select_query = """select * from clients"""
        cursor.execute(sql_select_query)
        record = cursor.fetchone()
        print(record)
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
a = update_date("310470705mc","2019-08-23","2030-08-23")

x = datetime.datetime.fromisoformat("2019-08-23")
print(x.day, x.month, x.year)
test_time = datetime.date(2019, 8, 23) > datetime.date(2020, 8, 23)
print(test_time)
...     INSERT INTO some_table (an_int, a_date, a_string)
...     VALUES (%s, %s, %s);
...     
...     (10, datetime.date(2005, 11, 18), "O'Reilly"))
a = fn()
import datetime

x = datetime.datetime.now()
print(x.day, x.month, x.year)

startd = "2019-08-23"
endd = "2020-08-23"



import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 65432)

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

tcp_echo_client('Hello World!')



'''
#api

    def groups_to_join(self, url):
        return self.group.get_groups_to_join(url) 
    
    def join_groups(self):
        try:
            return self.group.join_to_group()
        except Exception as e:
            return e    

####


    def get_groups_to_join(self, url):
        self.grp = JoinGroup(self.driver, self.sleep, url)
        self.driver.get(url)
        self.grp.initialize()
        #scrap all groups in page
        xpath_to_table_of_groups = "/html/body/div[1]/div[3]/div[1]/div/div[1]/div[3]/div[2]/div/div/table"
        table = self.driver.find_element_by_xpath(xpath_to_table_of_groups)
        trs = table.find_elements(By.TAG_NAME, "tr")#all rows in table
        for row in trs:#for each row
            trs = row.find_elements(By.TAG_NAME, "td")
            for cell in trs:
                self.tds.append(cell)
        to_return = self.tds.pop(0)
        return to_return.text

    def join_to_group(self):
        cell = self.tds.pop(1)
        print(cell.text)
        btn = cell.find_element(By.TAG_NAME, "button")
        btn.click()#click to join group
        try:
            self.grp.try_to_fill_dialog()
            self.grp.close_form()
        except:
            None
        self.sleep(randint(3,5))
        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()#exit the confirm popup
        return self.grp.get_group_details(cell)
'''
'''
async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.read(1024)).decode('utf8')
        response = str(eval(request)) + '\n'
        writer.write(response.encode('utf8'))
    writer.close()

loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle_client, 'localhost', 15555))
loop.run_forever()


async def echo_server(reader, writer):
    while True:
        data = await reader.read(1024)  # Max number of bytes to read
        if not data:
            break
        writer.write(data)
        await writer.drain()  # Flow control, see later
    writer.close()
    
async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()
asyncio.run(main('127.0.0.1', 65432))'''

async def loop_text_area(form, delay):
    """
    * Try to list text box's, click on each of them,
    * detect the language and send random keys with same language.
    * May raise Exception: x.find_..., x.click(), x.send_keys.
    """
    text_area_list = form.find_elements(By.TAG_NAME, "textarea")
    if(len(text_area_list)>0):
        for text_box in text_area_list:
            text_box_title = text_box.find_element_by_xpath('../..').text
            blob = TextBlob(text_box_title)
            text_box.click()
            if(blob.detect_language()=='iw'):#iw means hebrew
                text_box.send_keys(const.HEB[randint(0,len(const.HEB)-1)])
                print("mor")
            else:
                text_box.send_keys(const.ENG[randint(0,len(const.ENG)-1)])
                print("morrr")
            
f= ""            
btns = driver.find_elements(By.TAG_NAME, "button")
for btn in btns:
    if (btn.text == "סגור" or btn.text == "close" or btn.text == "Close"):
        go_to_parent = '..'
        for x in range(0,10):
            form = btn.find_element_by_xpath(go_to_parent)
            try:
                form = form.find_element_by_xpath('//div[@aria-label="השבה לשאלות"]')
                f= form
            except:
                go_to_parent += '/..'
                continue  
print(f.text)
a = loop_text_area(f,5)
print(a)


#form
forms = driver.find_elements(By.TAG_NAME, "form")
for form in forms:
    text_area_list = form.find_elements(By.TAG_NAME, "textarea")
    if(len(text_area_list)>0):
        f = form
 f.click()      





##################################################################
'''crawl jobs'''
################################################################## 

def scrollDown(pause_time):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for x in range(0,10):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        sleep(pause_time)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

options = Options()
options.set_preference("dom.webnotifications.enabled", False)
driver = webdriver.Firefox(firefox_options = options)
sleep(randint(2,5))
driver.get("https://www.facebook.com/")
login = Login("310470705mc","qwew",driver)
login.login_to_facebook(sleep)

post_content = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div/span')


import xerox
s = "dfdsf"
xerox.copy(s)

print(post_content.text)
post_content[0].send_keys("abcd")


scrollDown(8)

import re
job_posts = []
pref = ["javascript", "js", "python", "full", "stack"]

posts = driver.find_elements_by_xpath('//div[@data-testid="post_message"]')

for x in posts:    
    try:
        show_more = x.find_element_by_class_name("text_exposed_link")
        show_more.click()
    except:
        pass
    tmp = x.text
    tmp = tmp.lower()
    match = re.search(r'[\w\.-]+@[\w\.-]+', tmp)
    if match != None:
        for x in pref:
            if x in tmp:
                tmp = tmp.split()
                job_posts.append(tmp)
                break



