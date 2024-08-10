import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui as py
kerala_bus_details=[]

def busdetails(i,p):
   
    time.sleep(10)
    #c=driver.find_element(By.CSS_SELECTOR,'div[class="button"]')
    #action.move_to_element(c).click()
    wait=WebDriverWait(driver,100)
    try:
        asrpt= driver.find_element(By.CSS_SELECTOR, "#result-section>div:nth-child(1) .button")
        driver.execute_script("arguments[0].scrollIntoView();", asrpt)
        action.move_to_element(asrpt).click().perform()
    except:
        print('no data')    
    
    try:
        element=driver.find_element(By.CSS_SELECTOR,"#result-section>div:nth-child(2) .button")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        action.move_to_element(element).click().perform()
    except:
        print("nodatafound")    
    element = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="clearfix bus-item"]')))
    body = driver.find_element(By.TAG_NAME, 'body')
   
    while True:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if driver.execute_script("return window.innerHeight + window.scrollY") >= new_height:
            break
    buses = driver.find_elements(By.XPATH,'//div[@class="clearfix bus-item-details"]')
    
    for bus in buses:
        name = bus.find_element(By.CSS_SELECTOR, ".column-two.p-right-10.w-30.fl").text
        #type = bus.find_element(By.CSS_SELECTOR,".bus-type").text
        #departure_time = bus.find_element(By.CSS_SELECTOR, ".dp-time").text
        #arrival_time = bus.find_element(By.CSS_SELECTOR, ".bp-time").text
        duration = bus.find_element(By.CSS_SELECTOR, ".dur.l-color.lh-24").text
        price = bus.find_element(By.CSS_SELECTOR, ".seat-fare .fare span.f-19.f-bold").text
        seats_available=bus.find_element(By.CSS_SELECTOR,".seat-left.m-top-30").text
        try:
            rating = bus.find_element(By.CSS_SELECTOR, ".lh-18.rating.rat-green").text
        except:
            rating = "No rating"

        kerala_bus_details.append({
            "route-collected": i,
            "name": name,
           # "type":type,
           # "departure_time": departure_time,
           # "arrival_time": arrival_time,
            "duration": duration,
            "price": price,
            "seats_available":seats_available,
            "rating": rating
        })
        
    max_attempts = 10
    attempts = 0
    while attempts < max_attempts:
        py.hotkey('alt', 'left')
        time.sleep(1)
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, "route")))
            break
        except:
            attempts += 1
    
    scroll=driver.find_element(By.CSS_SELECTOR,f'.DC_117_paginationTable>.DC_117_pageTabs:nth-child({p})')        
    action.move_to_element(scroll).click().perform()      
       


driver=webdriver.Chrome()
driver.get("https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile")
action=ActionChains(driver)


p=1
