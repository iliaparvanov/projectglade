from selenium import webdriver
from bs4 import BeautifulSoup
import time

__author__ = "Engine Bai"
url = "https://www.cars.bg/?go=cars&search=1&advanced=&fromhomeu=1&currencyId=1&yearTo=&autotype=1&stateId=1&section=home&categoryId=0&doorId=0&brandId=0&modelId=0&fuelId=1&gearId=1&yearFrom=&priceFrom=&priceTo=&man_priceFrom=&man_priceTo=&regionId=0&offersFor4=1&offersFor1=1&filterOrderBy=1"

driver = webdriver.Chrome(executable_path="C:/Users/gdemi/Desktop/scraper/chromedriver.exe")
driver.get(url)
content_element = driver.find_element_by_tag_name("body")
content_html = content_element.get_attribute("innerHTML")

soup = BeautifulSoup(content_html, "html.parser")
brands = soup.find_all(name = "span", attrs = {"class" : "ver15black"})
price = soup.find_all(name = "span", attrs = {"class" : "ver20black"})
print(brands[0].b.text)
print(price[0].strong.text)

driver.close()