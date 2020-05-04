import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver import ActionChains
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
    el = driver.find_elements_by_css_selector('id.wire0')
    #print(el)
    if el:
        time.sleep(1 + random.randint(1, 4))
        webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
        time.sleep(1 + random.randint(1, 4))
        webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
        time.sleep(1 + random.randint(1, 4))
        webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    time.sleep(1 + random.randint(1, 4))


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    total = []

    drd = soup.find("input", {"class": "b_searchbox"})
    jj = {}
    jj["original search"] = drd["value"]
    jj["type"] = "stats"
    drd = soup.find("span", {"class": "sb_count"})
    if drd:
        jj["stats"] = drd.text.encode('ascii', 'ignore').decode("utf-8")
    else:
        jj["stats"] = "not available"
    total.append(jj)


    content = soup.findAll("div", {"class": "b_subModule"})

    if content:

        js = {}
        js["type"]="box"
        try:
            js["box_title"] = content[0].h2.text.encode('ascii', 'ignore').decode("utf-8")
        except:
            time.sleep(2)
        divv = content[0].findAll("div")
        if divv:
            js["box_description"] = divv[0].text.encode('ascii', 'ignore').decode("utf-8")
        link = content[0].find("div",{"class":"infoCardIcons"})
        if link:
            ll=link.findAll("a")
            js["link_attached"] = ll[0]["href"]
        else:
            di = content[0].findAll("div",{"class":"b_bgdesc"})
            js["box_description"] = di[0].text.encode('ascii', 'ignore').decode("utf-8")
            link = content[0].find("div",{"class":"b_algo"})
            ll = link.findAll("a")
            js["link_attached"] = ll[0]["href"]
        js["page"] = 1
        total.append(js)

    ########################################

    content = soup.findAll("div", {"class": "df_c d_ans"})
    if content:
        js = {}
        js["original search"] = jj["original search"]
        js["page"] = 1
        js["type"] = "top-box"
        para = content[0].findAll("div", {"class": "b_algo"})
        if para:
            js["box_title"] = para[0].h2.a.text.encode('ascii', 'ignore').decode("utf-8")
            js["link_attached"] = para[0].h2.a["href"]
        para = content[0].findAll("div",{"class":["rwrl rwrl_pri rwrl_padref","rwrl rwrl_sec rwrl_padref rwrl_hastitle"]})
        if para:
            js["box_description"] = para[0].text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)

    #######################################

    content = soup.findAll("div",{"class":"b_expansion_text b_1linetrunc"})
    if content:
        count = 1
        for mink in content:
            js={}
            if (count % 2 == 1):
                count = count + 1
                continue
            js["original search"] = jj["original search"]
            js["page"] = 1
            js["rank"] = int(count/2)
            count = count + 1
            js["type"] = "people also ask"
            js["query"] = mink.text.encode('ascii', 'ignore').decode("utf-8")
            total.append(js)
    ##########################################
    count = 1
    content = soup.findAll("li", {"class":"b_algo"})
    for mink in content:
        js = {}
        js["type"]="result"
        js["page"] = 1
        js["original search"] = jj["original search"]
        js["rank"]=count
        count=count+1
        abcd = mink.find("h2")
        js["title"] = abcd.a.text.encode('ascii', 'ignore').decode("utf-8")
        js["link"] = abcd.a["href"]
        ab = mink.findAll("p")
        #print(abcd)
        if ab:
            js["description"]=ab[0].text.encode('ascii', 'ignore').decode("utf-8")
        else:
            js["description"]=""
        total.append(js)

    related = soup.find("div", {"class": "b_rs"})
    if related:
        topics = related.find_all("li")
        num = 1
        for topic in topics:
            ja = {}
            ja["page"] = 1
            ja["original search"] = jj["original search"]
            ja["related-search"] = topic.text.encode('ascii', 'ignore').decode("utf-8")
            ja["rank"] = num
            num = num + 1
            total.append(ja)


    newpage = soup.findAll("a",{"class":"b_widePag sb_bp"})
    if newpage:
        s1 = "https://www.bing.com"
        newl = (newpage[0]["href"])
        newurl = s1 + newl
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(newurl)
            print(newurl)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
        except TimeoutException as e:
            print("Page load Timeout Occured. Quiting !!!")
            driver.quit()

        #contents = soup2.findAll("div", {"class": "rc"})

        count = 1
        content = soup.findAll("li", {"class": "b_algo"})

        for mink in content:
            js = {}
            js["page"]=2
            js["type"] = "result"
            js["original search"] = jj["original search"]
            js["rank"] = count
            count = count + 1
            abcd = mink.find("h2")
            js["title"] = abcd.a.text.encode('ascii', 'ignore').decode("utf-8")
            js["link"] = abcd.a["href"]
            ab = mink.findAll("p")
            # print(abcd)
            if ab:
                js["description"] = ab[0].text.encode('ascii', 'ignore').decode("utf-8")
            else:
                js["description"] = ""
            total.append(js)

        related = soup.find("div", {"class": "b_rs"})
        if related:
            topics = related.find_all("li")
            num = 1
            for topic in topics:
                ja = {}
                ja["page"] = 2
                ja["original search"] = jj["original search"]
                ja["related-search"] = topic.text.encode('ascii', 'ignore').decode("utf-8")
                ja["rank"] = num
                num = num + 1
                total.append(ja)

    search = jj["original search"].replace(" ", "_")
    filename = "./result/" + search + "/zing.json"
    #print(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    json_file = open(filename, 'w')
    json.dump(total, json_file, indent=1)
    json_file.close()
    return total

with open('search.txt', 'r') as file_in:
    lines = []
    for line in file_in:
        line=line.replace(' ','+')
        line = line.replace("'", "%27")
        str1="https://www.bing.com/search?q="
        url = str1 + line
        print(url)
        print(json.dumps(scrap_website(url), indent=1))
        #time.sleep(2)
