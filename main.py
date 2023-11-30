from bs4 import BeautifulSoup
from selenium import webdriver
from Phone import Phone
from OWLManager import OWLManager

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

list_of_phones = []

for link in links:
    while True:
        try:
            driver = webdriver.Chrome()
            driver.get(url=BASE_URL + link)
            
            soup = BeautifulSoup(driver.page_source, features="html.parser")  

            price = soup.find('div', class_="my-auto flex w-[55px] min-w-[55px] max-w-[55px] flex-shrink-0 flex-grow-0 justify-end py-2 align-middle text-lg font-medium tablet:pr-0 laptop:h-5 laptop:py-0 laptop:text-sm").find('div',class_="tabular-nums tracking-tightest").get_text().strip().split('*')[0]

            spec = soup.find('div', id="specification")

            segments = spec.find_all('div', class_="segment")

            name = ''
            screen = ''
            ram = ''
            os = ''
            chipset = ''
            camera = ''
            storage = ''
            brand = ''
            screen_dimension = ''
            width = ''
            height = ''
            date = ''
            colors = ''
            
            for segment in segments:
                
                content = segment.find('div', class_="content")

                options = content.find_all('div', class_="option")

                for option in options:
                    title = option.find('div', class_="title").get_text().strip()
                    if title == "Naziv":
                        name = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                        brand = name.split(' ')[0]

                    if title == "Tip":
                        screen = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                        
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
                        
                    if title == "Dimenzije":
                        screen_dimension = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip().split(' ')[0]
                        
                    if title == "Status":
                        date = option.find('div', class_="value").find('span', class_="font-extrabold").get_text().strip()

                    if title == "Paleta":
                        colors = option.find('div', class_="value").get_text().strip()
                        
                    if title == "Rezolucija":
                        resolution = option.find('div', class_="value").find('span', class_="font-bold").get_text().strip()
                        width = resolution.split('x')[0]
                        height = resolution.split('x')[1].split('p')[0]
                      
            phone = Phone(name,brand,camera,chipset,os,ram,screen,storage,screen_dimension,width,height,date,price,colors)
            list_of_phones.append(phone)
            
            driver.close()
            break
        except:
            driver.close()

manager = OWLManager("GoodRelations.owl")

for phone in list_of_phones:
    manager.add_individual_phone(phone)

manager.save_ontology("GoodRelationsPopulated.owl")