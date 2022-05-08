# Weather Data Scraper

## What this Program does
- Input a location you want to search to retrieve the weather data off of Weather.com.
- Selenium will automate the browser and input that keyword into the searchbox to get the first location that appears in the dropdown.
- BeautifulSoup will then parse information on the website from the location specific link to get the 10 day weather data results.
- Pandas will format the data into an Excel sheet and also print the weather data in the terminal.

## Demo
- Input a location: 

![image](https://user-images.githubusercontent.com/90528127/167280499-b9c89db9-1cd8-4f02-86f9-fc420794780a.png)
- Outputs the following weather data in the terminal: 

![image](https://user-images.githubusercontent.com/90528127/167280702-41f45c81-94a5-4257-ae88-99c3d67c5dc7.png)
- Pandas will also convert the data into an Excel file

![image](https://user-images.githubusercontent.com/90528127/167280727-80d042a1-b7d8-4c08-95f7-af38ba3c7ffb.png)

## How to run locally
- Clone this project
- Install the modules `pip install pandas` and `pip install beautifulsoup4`
- Install the Selenium WebDriver for Chrome based on your specific Chrome version
