import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
import time
import random


# The function to query a website
def scrap_website(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(1 + random.randint(1, 4))
    el = driver.find_element_by_id("rld-1")
    time.sleep(1 + random.randint(1, 4))
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    total = []
    drd = soup.find("input", {"class": "search__input--adv js-search-input"})
    search=drd["value"]
    content = soup.findAll("div", {"class": "module__body js-about-item"})
    if content:
        js = {}
        divv = content[0].findAll("div")
        js["original search"] = search
        js["type"]="box"
        js["box_title"] = divv[0].text.encode('ascii', 'ignore').decode("utf-8")
        js["box_description"] = divv[1].text.encode('ascii', 'ignore').decode("utf-8")
        link = divv[1].find("a", {"class": "module__more-at js-about-item-more-at-inline tx--bold"})
        js["link_attached"] = link["href"]
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
    with open('out.json') as f:
        data = json.load(f)
        f.close()
    data.extend(total)
    json_file = open('duckduck.json', 'w')
    json.dump(data , json_file, indent=1)
    json_file.close()
    return total


with open('search.txt', 'r') as file_in:
    lines = []
    for line in file_in:
        line=line.replace(' ','+')
        str1="https://duckduckgo.com/?q="
        url = str1 + line
        print(url)
        #lines.append(line)
        print(json.dumps(scrap_website(url), indent=1))
        #time.sleep(2)
