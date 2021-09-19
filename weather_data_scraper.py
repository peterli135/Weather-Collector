"""
Project: Get Weather Data from Zipcode (Weather.com)

What the program will do:
1. Get the search keyword, in this case, it will be the zipcode, from the input zipcode.
2. Retrieve the search result page for the zipcode that was given.
3. Print what the weather is / can also open a new tab to take you to Weather.com for that zipcode.

What the code will look like:
1. Read the zipcode that was given from the input.
2. Fetch the search result page with the requests module.
3. Find the link to each search result.
4. Call webbrowser.open() to open the link.
"""

#! python 3
# find_weather.py - Find the weather through the zipcode.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

search_input = input('What location do you want search: ')

#uses selenium in order to automate web browser to get url links.
driver = webdriver.Chrome()
driver.get('https://weather.com/')
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'LocationSearch_input')))
weather_search = driver.find_element_by_id('LocationSearch_input')
weather_search.send_keys(search_input)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'LocationSearch_listbox-0')))
weather_click = driver.find_element_by_id('LocationSearch_listbox-0')
weather_click.click()
current_weather_url = driver.current_url
driver.quit()

#requests instance for current weather
current_weather_html = requests.get(current_weather_url)
soup_current = BeautifulSoup(current_weather_html.text, 'html.parser')

#gets tenday weather url requests and instance for tenday weather
tenday_weather_url = 'https://weather.com' + soup_current.find('a', attrs={'data-from-string': 'localsuiteNav_3_10 Day'}).get('href')
tenday_weather_html = requests.get(tenday_weather_url)
soup_tenday = BeautifulSoup(tenday_weather_html.text, 'html.parser')

weather_info = soup_tenday.find_all(class_='DaypartDetails--DetailSummaryContent--3uxcj Disclosure--SummaryDefault--3xAWB')

days = []
weather_list = []
for items in weather_info:
    weather_dict = {}
    day = items.find('h2').text
    weather_dict['Temperature'] = items.find(class_='DetailsSummary--temperature--1Syw3').text
    weather_dict['Conditions'] = items.find(class_='DetailsSummary--extendedData--365A_').text
    weather_dict['Precipitation'] = items.find('span', attrs={'data-testid': 'PercentageValue'}).text
    weather_dict['Wind'] = items.find(class_='Wind--windWrapper--3aqXJ undefined').text
    days.append(day)
    weather_list.append(weather_dict)

location = soup_tenday.find('span', attrs={'class': 'LocationPageTitle--PresentationName--1QYny'}).text
print("You requested weather data for the location:", location)

df = pd.DataFrame(weather_list, index = days)
print(df)

"""
#get the location of the zipcode
location = soup_tenday.find('span', attrs={'class': 'LocationPageTitle--PresentationName--1QYny'}).text

#get current temperature
current_temp = soup_current.find('span', attrs={'class': 'CurrentConditions--tempValue--3a50n'}).text

#get current conditions
current_conditions = soup_current.find('div', attrs={'class': 'CurrentConditions--phraseValue--2Z18W'}).text

#get the high temperature
high_temp = soup_tenday.find('span', attrs={'class': 'DetailsSummary--highTempValue--3Oteu'}).text

#get the low temp value
low_temp = soup_tenday.find('span', attrs={'class': 'DetailsSummary--lowTempValue--3H-7I'}).text

#get the precipitation content
precip = soup_tenday.find('span', attrs={'data-testid': 'PercentageValue'}).text

#get the wind content
wind = soup_tenday.find('span', attrs={'class': 'Wind--windWrapper--3aqXJ undefined'}).text

#get the time from when the data was requested
time = soup_tenday.find('div', attrs={'class': 'DailyForecast--timestamp--22ExT'}).text

print("You requested weather data for the location:", location)
print("The time is currently:", time)
print("The current temperature is:", current_temp, "& Current conditions:", current_conditions)
print("The tempature high for today will be:", high_temp, "& The temperature low for today will be: ", low_temp)
print("The precipitation for today is:", precip)
print("The wind today is:", wind)

temps = []
for items in soup_tenday.find_all(class_='DaypartDetails--DetailSummaryContent--3uxcj Disclosure--SummaryDefault--3xAWB'):
    day = items.find('h2').text
    temp = items.find(class_="DetailsSummary--temperature--1Syw3").text
    temps.append(temp)
    print(day, ":", temp)
"""
