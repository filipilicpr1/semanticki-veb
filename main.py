from bs4 import BeautifulSoup
from selenium import webdriver
from Phone import Phone

BASE_URL = "https://mobilnisvet.com"

BASE_LINKS = [
    "/mobilni-proizvodjac/Apple/22/2",
    "/mobilni-proizvodjac/Google/71/2",
    "/mobilni-proizvodjac/Huawei/35/2",
    "/mobilni-proizvodjac/OnePlus/55/2",
    "/mobilni-proizvodjac/Poco/84/2",
    "/mobilni-proizvodjac/Samsung/6/2",
    "/mobilni-proizvodjac/Xiaomi/52/2"
]

def populate_links(top_level, links):
    for child in top_level.findChildren():
        text = child.get_text().strip()
        if child.name == "div" and (text == "2019." or text == "2018."):
            break

        if child.name != "a":
            continue

        link = next(iter(child.get_attribute_list(key="href")), None)
        if link is None:
            continue

        links.append(link)

options = webdriver.ChromeOptions()
options.add_argument("headless")

links = []

for base_link in BASE_LINKS:
    while True:
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url=BASE_URL + base_link)

            soup = BeautifulSoup(driver.page_source, features="html.parser")
            top_level = soup.find(
                'div', class_="my-3 flex justify-center border border-b border-green-200 bg-green-50 py-3 text-center text-xl font-black text-green-600"
                ).find_next_sibling()

            populate_links(top_level, links)

            driver.close()
            break
        except:
            driver.close()

listOfPhones = []

for link in links:
    while True:
        try:
            driver = webdriver.Chrome()
            driver.get(url=BASE_URL + link)
            
            soup = BeautifulSoup(driver.page_source, features="html.parser")

            spec = soup.find('div', id="specification")

            segments = spec.find_all('div', class_="segment")

            name = ''
            type = ''
            ram = ''
            os = ''
            chipset = ''
            camera = ''
            storage = ''
            brand = ''
            
            for segment in segments:
                
                content = segment.find('div', class_="content")

                options = content.find_all('div', class_="option")

                for option in options:
                    title = option.find('div', class_="title").get_text().strip()
                    if title == "Naziv":
                        name = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                        brand = name.split(' ')[0]

                    if title == "Tip":
                        type = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                        
                    if title == "RAM":
                        ram = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                        
                    if title == "Operativni":
                        os = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                        
                    if title == "Čipset":
                        chipset = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                        
                    if title == "Glavna":
                       camera = option.find('span', class_="pr-1 font-extrabold text-pink-600").get_text().strip()
                        
                    if title == "Interna":
                        storage = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                      
            phone = Phone(name,brand,camera,chipset,os,ram,type,storage)
            listOfPhones.append(phone)
            
            driver.close()
            break
        except:
            driver.close()
