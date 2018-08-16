from urllib.request import urlopen
from bs4 import BeautifulSoup

quote_page = 'https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=7ubv0g&f1=1'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
	
brands = soup.findAll(name = 'a', attrs = {"class" : "mmm"})
prices = soup.findAll(name = 'span', attrs = {"class" : "price"})

print(brands[0].text)
print(prices[0].text)