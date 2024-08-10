from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyautogui as py
import mysql.connector
import csv
import os

# Define your list to hold bus details
rajasthan_bus_details = []

def busdetails(route_name, page_number):
    """Collect bus details from the current route page."""
    time.sleep(10)  # Wait for the page to load

    try:
        # Click on the route details button
        asrpt = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#result-section>div:nth-child(1) .button"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", asrpt)
        action.move_to_element(asrpt).click().perform()
    except Exception as e:
        print(f'Error clicking on route details button: {e}')

    try:
        # Click on the additional details button
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#result-section>div:nth-child(2) .button"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)
        action.move_to_element(element).click().perform()
    except Exception as e:
        print(f'Error clicking additional details button: {e}')

    try:
        # Wait for bus items to be present and scroll
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="clearfix bus-item"]'))
        )

        body = driver.find_element(By.TAG_NAME, 'body')
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Extract bus details
        buses = driver.find_elements(By.CSS_SELECTOR, ".bus-item")  # Ensure this selector is correct
        for bus in buses:
            try:
                bus_name = bus.find_element(By.CSS_SELECTOR, ".column-two.p-right-10.w-30.fl").text
                arrival_time = bus.find_element(By.CSS_SELECTOR, ".bp-time.f-19.d-color.disp-Inline").text
                duration = bus.find_element(By.CSS_SELECTOR, ".dur.l-color.lh-24").text
            
                # Extract seat availability with a fallback
                try:
                    seat_availability = bus.find_element(By.CSS_SELECTOR, ".seat-left.m-top-30").text
                except:
                    seat_availability = "Not available"
                
                # Extract fare with a fallback
                try:
                    fare = bus.find_element(By.CSS_SELECTOR, ".seat-fare .fare span.f-19.f-bold").text
                except:
                    fare = "Not listed"
                
                # Extract rating
                try:
                    rating_element = bus.find_element(By.CSS_SELECTOR, ".lh-18.rating.rat-green")  # Adjust the selector if necessary
                    rating = rating_element.text
                except:
                    rating = "No rating"
                
                # Extract departure and arrival locations if needed
                try:
                    departure_location = bus.find_element(By.CSS_SELECTOR, ".dp-loc.l-color.w-wrap.f-12.m-top-42").text
                except:
                    departure_location = "Not listed"
                
                try:
                    arrival_location = bus.find_element(By.CSS_SELECTOR, ".bp-loc.l-color.w-wrap.f-12.m-top-8").text
                except:
                    arrival_location = "Not listed"
                
                # Print bus information without departure time
                print(f"Name: {bus_name}")
                print(f"Arrival Time: {arrival_time}")
                print(f"Duration: {duration}")
                print(f"Fare: {fare}")
                print(f"Seat Availability: {seat_availability}")
                print(f"Rating: {rating}")
                print(f"Departure Location: {departure_location}")
                print(f"Arrival Location: {arrival_location}")
                print("------")

                # Append the details to the list
                rajasthan_bus_details.append({
                    "route-collected": route_name,
                    "name": bus_name,
                    "arrival_time": arrival_time,
                    "duration": duration,
                    "fare": fare,
                    "seats_available": seat_availability,
                    "rating": rating,
                    "departure_location": departure_location,
                    "arrival_location": arrival_location
                })

            except Exception as e:
                print(f"Error extracting information from bus item: {e}")

    except Exception as e:
        print(f"Error in busdetails function: {e}")

    try:
        # Navigate back and go to the next page
        max_attempts = 10
        attempts = 0
        while attempts < max_attempts:
            py.hotkey('alt', 'left')
            time.sleep(1)
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "route"))
                )
                break
            except Exception as e:
                print(f"Error navigating back: {e}")
                attempts += 1

        # Go to the specified page
        scroll = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'.DC_117_paginationTable>.DC_117_pageTabs:nth-child({page_number})'))
        )
        action.move_to_element(scroll).click().perform()

    except Exception as e:
        print(f"Error in pagination or navigation: {e}")

chrome_options = Options()
# Uncomment to run in headless mode
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
action = ActionChains(driver)

try:
    driver.get("https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile")  # Adjust URL if needed

    for j in range(1, 4):  # Adjust range if needed
        try:
            scroll = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'.DC_117_paginationTable>.DC_117_pageTabs:nth-child({j})'))
            )
            action.move_to_element(scroll).click().perform()

            route_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "route"))
            )
            route_collected = [route.text for route in route_elements]

            for route_name in route_collected:
                try:
                    route_link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, route_name))
                    )
                    action.move_to_element(route_link).click().perform()
                    busdetails(route_name, j)
                except Exception as e:
                    print(f"Error interacting with route link '{route_name}': {e}")

        except Exception as e:
            print(f"Error navigating pages or routes: {e}")

finally:
    driver.quit()

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="Iloveall@12345",  # Replace with your MySQL password
    database="bus_routes"  # Replace with your database name
)
cursor = conn.cursor()

# Create table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS rajasthan_bus_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(255),
    bus_name VARCHAR(255),
    arrival_time VARCHAR(255),
    duration VARCHAR(255),
    fare VARCHAR(255),
    seats_available VARCHAR(255),
    rating VARCHAR(255),
    departure_location VARCHAR(255),
    arrival_location VARCHAR(255)
);
'''
cursor.execute(create_table_query)

# Function to insert data
def insert_data(data):
    insert_query = '''
    INSERT INTO rajasthan_bus_routes (
        route_name, bus_name, arrival_time, duration, fare,
        seats_available, rating, departure_location, arrival_location
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        data.get('route-collected'),
        data.get('name'),
        data.get('arrival_time'),
        data.get('duration'),
        data.get('fare'),
        data.get('seats_available'),
        data.get('rating'),
        data.get('departure_location'),
        data.get('arrival_location')
    ))
    conn.commit()

# Insert the scraped data into MySQL
for bus in rajasthan_bus_details:
    try:
        insert_data(bus)
    except Exception as e:
        print(f"Error inserting data into MySQL: {e}")

# Close the database connection
cursor.close()
conn.close()

print("Data successfully inserted into MySQL database.")
