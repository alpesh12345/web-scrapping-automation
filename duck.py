import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
import time
import random
import os


# The function to query a website
def scrap_website(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(1 + random.randint(1, 4))
    try:
        el = driver.find_element_by_id("rld-1")
        #print(el)
        time.sleep(1 + random.randint(1, 4))
        if el:
            webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    except:
        time.sleep(1 + random.randint(1, 4))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    total = []
    drd = soup.find("input", {"class": "search__input--adv js-search-input"})
    search=drd["value"]
    content = soup.findAll("div", {"class": "module__body js-about-item"})
    #asd=0
    try:
        divv = content[0].a["href"]
    except:
        divv=""
    print(content)
    if content:
        if not divv:
            js = {}
            divv = content[0].findAll("div")
            js["original search"] = search
            js["type"]="box"
            js["box_title"] = divv[0].text.encode('ascii', 'ignore').decode("utf-8")
            js["box_description"] = divv[1].text.encode('ascii', 'ignore').decode("utf-8")
            link = divv[1].find("a", {"class": "module__more-at js-about-item-more-at-inline tx--bold"})
            js["link_attached"] = link["href"]
            total.append(js)
        else:
            js = {}
            js["original search"] = search
            js["type"] = "box"
            js["link_attached"] = content[0].a["href"]
            divv = content[0].findAll("div")
            js["box_title"] = divv[0].text.encode('ascii', 'ignore').decode("utf-8")
            js["box_description"] = divv[2].text.encode('ascii', 'ignore').decode("utf-8")
            total.append(js)


    count=1
    content = soup.findAll("div", {"class":"result__body links_main links_deep"})
    for mink in content:
        js = {}
        js["original search"] = search
        js["type"] = "result"
        js["rank"]=count
        count=count+1
        abcd = mink.h2.find("a", {"class":"result__a"})
        js["title"] = abcd.text.encode('ascii', 'ignore').decode("utf-8")
        js["link"] = abcd["href"]
        des = mink.find("div", {"class": "result__snippet js-result-snippet"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)

    search=search.replace(" ","_")
    filename = "./result/"+search+"/duckduck.json"
    print(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    json_file = open(filename, 'w')
    json.dump(total , json_file, indent=1)
    json_file.close()
    return total


with open('search.txt', 'r') as file_in:
    lines = []
    count =1
    for line in file_in:
        count = count + 1
        if count % 14 == 0:
            time.sleep(15 + random.randint(1, 4))
            print("sleeping")
        line=line.replace(' ','+')
        line = line.replace("'", "%27")
        str1="https://duckduckgo.com/?q="
        url = str1 + line
        print(url)
        print(json.dumps(scrap_website(url), indent=1))
        time.sleep(4 + random.randint(1, 4))