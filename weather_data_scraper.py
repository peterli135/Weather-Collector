import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

search_input = input('What location do you want search: ')

# uses selenium in order to automate web browser to get url links for request location.
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

# requests instance for current weather
current_weather_html = requests.get(current_weather_url)
soup_current = BeautifulSoup(current_weather_html.text, 'html.parser')

# gets tenday weather url requests and instance for tenday weather
def find_tenday(href): 
    return href and re.compile("/en-CA/weather/tenday").search(href)

tenday_weather_url = 'https://weather.com' + soup_current.find(href=find_tenday).get('href')
tenday_weather_html = requests.get(tenday_weather_url)
soup_tenday = BeautifulSoup(tenday_weather_html.text, 'html.parser')

weather_info = soup_tenday.find_all(class_='DaypartDetails--DetailSummaryContent--3uxcj Disclosure--SummaryDefault--3xAWB')

#creates empty lists and uses for loop to go through each date for the weather
days = []
weather_list = []
for items in weather_info:
    weather_dict = {}
    day = items.find('h3').text
    weather_dict['Temperature'] = items.find(class_='DetailsSummary--temperature--1Syw3').text
    weather_dict['Conditions'] = items.find(class_='DetailsSummary--extendedData--365A_').text
    weather_dict['Precipitation'] = items.find('span', attrs={'data-testid': 'PercentageValue'}).text
    weather_dict['Wind'] = items.find(class_='Wind--windWrapper--3aqXJ undefined').text
    days.append(day)
    weather_list.append(weather_dict)

# prints out the location that was requested
location = soup_tenday.find('span', attrs={'class': 'LocationPageTitle--PresentationName--1QYny'}).text
print("You requested weather data for the location:", location)

df = pd.DataFrame(weather_list, index = days).rename_axis("Days")
with pd.ExcelWriter('weather_10day_data.xlsx') as writer:  
    df.to_excel(writer, sheet_name='x1')

print(df)
