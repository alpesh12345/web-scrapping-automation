import json
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.common.exceptions import TimeoutException


def scrap_website(url):
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    #print(soup.prettify())
    total = []


    content = soup.findAll("div",{"class":"kno-ecr-pt PZPZlf gsmt i8lZMc hNKfZe"})
    if content:
        js = {}
        js["box_title"] = content[0].text.encode('ascii', 'ignore').decode("utf-8")
        desc = soup.find("div",{"class":"kno-rdesc"})
        js["box_description"] = desc.div.span.text.encode('ascii', 'ignore').decode("utf-8")
        link = soup.find("a",{"class":"q ruhjFe NJLBac fl"})
        js["link_attached"] = link["href"]
        total.append(js)


    content = soup.findAll("div", {"class":"rc"})

    for mink in content:
        js = {}

        js["title"] = mink.h3.text.encode('ascii', 'ignore').decode("utf-8")
        abcd = mink.find("a")
        js["link"] = abcd["href"]


        des = mink.find("span", {"class": "st"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)
    newpage = soup.findAll("td")
    s1 = "https://www.google.co.in"
    newl = (newpage[2].a["href"])
    newurl = s1 + newl
    driver = webdriver.Chrome()
    try:
        driver.get(newurl)
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
    except TimeoutException as e:
        print("Page load Timeout Occured. Quiting !!!")
        driver.quit()

    contents = soup2.findAll("div", {"class": "rc"})

    for mink in contents:
        js = {}

        js["title"] = mink.h3.text.encode('ascii', 'ignore').decode("utf-8")
        abcd = mink.find("a")
        js["link"] = abcd["href"]

        des = mink.find("span", {"class": "st"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)

    # return our list of repositories as the output of our function

    json_file = open('out.json', 'w')
    json.dump(total , json_file)
    json_file.close()
    return total


print(json.dumps(scrap_website("https://www.google.co.in/search?sxsrf=ALeKk01F0bMR9IBCwInM9ypyRgYXuz905g%3A1584110723297&ei=g5xrXpblEcbH4-EPqtCz6A0&q=intimate+partner&oq=intimate+partner&gs_l=psy-ab.3..35i39j0i67j0j0i67j0l3j0i67j0l2.29762.31015..31593...0.0..0.183.1300.0j8......0....1..gws-wiz.......0i7i30.gC2JBieh39g&ved=0ahUKEwjWssmn2JfoAhXG4zgGHSroDN0Q4dUDCAs&uact=5"), indent=1))
