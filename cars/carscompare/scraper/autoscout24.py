from urllib.request import urlopen
from bs4 import BeautifulSoup

def is_int(input):
	try:
		int(input)
	except ValueError:
		return False
	return True


brand = "ford"
model = "fiesta"
upholstery = "CL"
year = "2013"
gear = "M"
fuel = "D"

quote_page = 'https://www.autoscout24.com/lst/' + brand + '/' + model + '?sort=price&desc=0&gear=' + gear + '&fuel=' + fuel + '&ustate=N%2CU&priceto=4500&fregfrom=' + year + '&uph=' + upholstery + '&atype=C'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

brands = soup.findAll(name = 'h2', attrs = {"class" : "cldt-summary-makemodel sc-font-bold sc-ellipsis"})
prices = soup.findAll(name = 'span', attrs = {"class" : "cldt-price sc-font-xl sc-font-bold"})


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
