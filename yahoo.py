import json
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
import time
import os

from selenium.common.exceptions import TimeoutException


def scrap_website(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    #print("success")
    time.sleep(2 + random.randint(1, 4))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #
    #print(soup.prettify())
    driver.quit()
    total = []
    drd=soup.find("input",{"class":"sbq"})
    jj={}
    jj["original search"]=drd["value"]
    jj["type"]="stats"
    drd=soup.findAll("div",{"class":"compPagination"})
    #print(drd)
    jj["stats"]=drd[0].span.text.encode('ascii', 'ignore').decode("utf-8")
    total.append(jj)

    content = soup.findAll("div",{"class":"dd catKG KgGeneric"})
    if content:
        js = {}
        js["original search"]=jj["original search"]
        js["page"] = 1
        js["type"] = "box"
        para=content[0].findAll("p")
        js["box_title"] = para[0].text.encode('ascii', 'ignore').decode("utf-8")

        js["box_description"] = para[1].text.encode('ascii', 'ignore').decode("utf-8")
        if len(para)>2:
            js["more description"] = para[2].text.encode('ascii', 'ignore').decode("utf-8")

            js["link_attached"] = para[2].a["href"]
        else:
            js["link_attached"] = para[1].a["href"]
        total.append(js)

    content = soup.findAll("div",{"class":"compContainerUL yui3-skin-sam"})
    if content:
        js = {}
        js["original search"]=jj["original search"]
        js["page"] = 1
        js["type"] = "top-box"
        para=content[0].findAll("div")
        if para[1].a:
            js["box_title"] = para[1].a.text.encode('ascii', 'ignore').decode("utf-8")

            js["box_description"] = para[0].text.encode('ascii', 'ignore').decode("utf-8")
            js["link_attached"] = para[1].a["href"]
            total.append(js)
        else:
            js["box_title"] = para[0].text.encode('ascii', 'ignore').decode("utf-8")
            js["box_description"] = para[1].text.encode('ascii', 'ignore').decode("utf-8")
            sds=para[2].find("a")
            if sds:
                js["link_attached"] = sds["href"]
            total.append(js)

    count=1
    content = soup.findAll("span",{"class":"cur-p c-black fz-m"})
    for mink in content:
        js = {}
        js["original search"]=jj["original search"]
        js["page"] = 1
        js["rank"] = count
        count = count + 1
        js["type"] = "People also ask"
        js["query"] = mink.text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)


    content = soup.find_all("div", {"class":["dd algo algo-sr lst richAlgo","dd algo algo-sr fst Sr","dd algo algo-sr richAlgo","dd algo algo-sr lst Sr","dd algo algo-sr Sr"]})
    count=1
    p=0
    for mink in content:
        js = {}
        js["type"] = "result"
        js["original search"] = jj["original search"]
        js["page"]=1
        js["title"] = mink.div.h3.text.encode('ascii', 'ignore').decode("utf-8")
        abcd = mink.find("a")
        js["link"] = abcd["href"]


        des = mink.find_all("p", {"class": "fz-ms lh-1_43x"})
        if des:
            js["description"] = des[0].text.encode('ascii', 'ignore').decode("utf-8")
        else:
            js["description"] = ""
        js["rank"] = count
        count = count + 1
        total.append(js)

###################################################################################
    related = soup.find("table",{"class":"compTable m-0 ac-1st td-n fz-ms"})
    if related:
        topics=related.find_all("a")
        num=1
        for topic in topics:
            ja={}
            ja["page"] = 1
            ja["original search"] = jj["original search"]
            ja["related-search"]=topic.text.encode('ascii', 'ignore').decode("utf-8")
            ja["rank"]=num
            num=num+1
            total.append(ja)
##################################################################################
    newpage = soup.findAll("div",{"class":"compPagination"})

    pag = newpage[0].findAll("a")
    if pag:
        s1 = "https://search.yahoo.com/search?q="
        newurl = (pag[0]["href"])
        #print(newurl)
        #newurl = s1 + newl
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get(newurl)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(2 + random.randint(1, 4))
            driver.quit()
        except TimeoutException as e:
            print("Page load Timeout Occured. Quiting !!!")
            driver.quit()

        content = soup.find_all("div", {
            "class": ["dd algo algo-sr lst richAlgo", "dd algo algo-sr fst Sr", "dd algo algo-sr richAlgo",
                      "dd algo algo-sr lst Sr", "dd algo algo-sr Sr"]})
        count = 1
        p = 0
        for mink in content:
            js = {}
            js["type"] = "result"
            js["original search"] = jj["original search"]
            js["page"] = 2
            js["title"] = mink.div.h3.text.encode('ascii', 'ignore').decode("utf-8")
            abcd = mink.find("a")
            js["link"] = abcd["href"]

            des = mink.find_all("p", {"class": "fz-ms lh-1_43x"})
            if des:
                js["description"] = des[0].text.encode('ascii', 'ignore').decode("utf-8")
            else:
                js["description"] = ""
            js["rank"] = count
            count = count + 1
            total.append(js)

        related = soup.find("table", {"class": "compTable m-0 ac-1st td-n fz-ms"})
        if related:
            topics = related.find_all("a")
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
    filename = "./result/" + search + "/yahoo.json"
    print(filename)
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
        str1="https://search.yahoo.com/search?q="
        url = str1 + line
        print(url)
        print(json.dumps(scrap_website(url), indent=1))
        #time.sleep(2)