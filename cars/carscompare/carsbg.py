from selenium import webdriver
from bs4 import BeautifulSoup
import time
from . import views
from .scraper import maps 

def is_int(input):
	try:
		int(input)
	except ValueError:
		return False
	return True

def urlCreate(brandid, modelid, gearid, year, fuelid):
	
	url = "https://www.cars.bg/?go=cars&search=1&advanced=&fromhomeu=1&currencyId=1&autotype=1&stateId=1&section=home&categoryId=0&doorId=0&brandId=" + brandid + "&modelId=0&models%5B%5D=" + modelid + "&fuelId=" + fuelid + "&gearId=" + gearid + "&yearFrom=" + year + "&yearTo=" + year + "&priceFrom=&priceTo=&man_priceFrom=&man_priceTo=&regionId=0&offersFor4=1&offersFor1=1&filterOrderBy=1"
	return url


def urlsCreate():
	start = time.time()
	urls = list()
	index = 0
	for brand, brandid in maps.brandId.items():
		for model, modelid in maps.globalsFromMaps[brand].items():
			for gear, gearid in maps.gearId.items():
				for fuel, fuelId in maps.fuelId.items():
					for yearid in maps.yearid:


						if yearid < 2006 and fuelId == 7:
							pass
						else:
							url = urlCreate(str(brandid), str(modelid), str(gearid), str(yearid), str(fuelId))
							info = [str(brand), str(model), str(gear), str(yearid), str(fuel)]
							urls.append([url, info])
	return urls

def scraper(url, info):
	#print(info)
	__author__ = "Engine Bai"
	driver = webdriver.Chrome(executable_path=r"C:/Users/gdemi/Desktop/projectglade/cars/carscompare/scraper/chromedriver.exe")
	driver.get(url)
	content_element = driver.find_element_by_tag_name("body")
	content_html = content_element.get_attribute("innerHTML")

	soup = BeautifulSoup(content_html, "html.parser")
	prices = soup.find_all(name = "span", attrs = {"class" : "ver20black"})
	fuel = soup.find_all(name = "td", attrs = {"style" : "border-left:0px;padding-left:0px;"})
	

	if prices != []:

		

		a = 0
		fuelList = []
		pricesList = []
		for j in range(len(prices)):
			for i in range(len(prices[j].text)):
				if is_int(prices[j].text[i]):
					a *= 10
					a += int(prices[j].text[i])

			if info[4] == "Gasoline":
				if "газ/бензин" in fuel[j].text or "метан/бензин" in fuel[j].text:
					pass
				else:

					pricesList.append(a)
					fuelList.append(fuel[j].text)
			else:
				pricesList.append(a)
				fuelList.append(fuel[j].text)
			
			a = 0


				

		prices = 0
		for i in pricesList:
			prices += i


		if prices > 0:
			prices //= len(pricesList)
		else:
			prices = []

	driver.close()
	print(info)
	return prices, info
		
# print(scraper("https://www.cars.bg/?go=cars&search=1&advanced=0&fromhomeu=1&publishedTime=0&filterOrderBy=1&showPrice=0&autotype=1&stateId=1&section=cars&categoryId=0&doorId=0&brandId=5&modelId=0&models%5B%5D=55&fuelId=2&gearId=1&yearFrom=2006&yearTo=2006&priceFrom=&priceTo=&currencyId=1&man_priceFrom=0&man_priceTo=0&man_currencyId=1&regionId=0&offersFor4=1&offersFor1=1", ['Alpina', 'D3', 'Manual', '2006', 'Diesel']))
