from selenium import webdriver
from bs4 import BeautifulSoup
import time

def is_int(input):
	try:
		int(input)
	except ValueError:
		return False
	return True


def scraper(brandid, modelid, gearid, year, fuelid):
	url = "https://www.cars.bg/?go=cars&search=1&advanced=&fromhomeu=1&currencyId=1&yearTo=&autotype=1&stateId=1&section=home&categoryId=0&doorId=0&brandId=" + brandid + "&modelId=" + modelid + "&fuelId=" + fuelid + "&gearId=" + gearid + "&yearFrom=" + year + "&yearTo=" + year + "&priceFrom=&priceTo=&man_priceFrom=&man_priceTo=&regionId=0&offersFor4=1&offersFor1=1&filterOrderBy=1"

	__author__ = "Engine Bai"
	driver = webdriver.Chrome(executable_path=r"C:/Users/gdemi/Desktop/projectglade/cars/carscompare/scraper/chromedriver.exe")
	driver.get(url)
	content_element = driver.find_element_by_tag_name("body")
	content_html = content_element.get_attribute("innerHTML")

	soup = BeautifulSoup(content_html, "html.parser")
	prices = soup.find_all(name = "span", attrs = {"class" : "ver20black"})

	if soup and prices:

		for i in range(len(prices)):
			prices[i] = prices[i].strong


		a = 0
		pricesList = []
		for j in range(len(prices)):
			for i in range(len(prices[j].text)):
				if is_int(prices[j].text[i]):
					a *= 10
					a += int(prices[j].text[i])
			pricesList.append(a)
			a = 0


		prices = 0
		for i in pricesList:
			prices += i

		prices //= len(pricesList)

	driver.close()

	return prices

	