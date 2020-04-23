import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.common.exceptions import TimeoutException


def scrap_website(url):
    driver = webdriver.Chrome()
    driver.get(url)
    el = driver.find_element_by_css_selector(".mWyH1d.UgLoB.kno-atc")
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    #time.sleep(1)
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    #print(soup.prettify())
    total = []
    drd=soup.find("input",{"class":"gLFyf gsfi"})
    jj={}
    jj["original search"]=drd["value"]
    jj["type"]="stats"
    drd=soup.find("div",{"id":"result-stats"})
    jj["stats"]=drd.text.encode('ascii', 'ignore').decode("utf-8")
    total.append(jj)

    content = soup.findAll("div",{"class":"SPZz6b"})
    if content:
        js = {}
        js["original search"]=jj["original search"]
        js["page"] = 1
        js["type"] = "box"
        js["box_title"] = content[0].text.encode('ascii', 'ignore').decode("utf-8")
        desc = soup.find("div",{"class":"kno-rdesc"})
        js["box_description"] = desc.div.span.text.encode('ascii', 'ignore').decode("utf-8")
        link = soup.find("a",{"class":"q ruhjFe NJLBac fl"})
        js["link_attached"] = link["href"]
        total.append(js)


    content = soup.find_all("div", {"class":"rc"})
    #print(content)
    count=1
    p=0
    for mink in content:
        js = {}
        js["type"] = "result"
        js["original search"] = jj["original search"]
        js["page"]=1
        js["title"] = mink.h3.text.encode('ascii', 'ignore').decode("utf-8")
        abcd = mink.find("a")
        js["link"] = abcd["href"]


        des = mink.find_all("span", {"class": "st"})
        js["description"] = des[0].text.encode('ascii', 'ignore').decode("utf-8")
        if js["description"]:
            js["rank"] = count
            count = count + 1
            total.append(js)
            continue
        if not js["description"] and count<2:
            des = soup.find("span", {"class": "ILfuVd"})
            print(des)
            if des:
                ja={}
                ja["original search"] = jj["original search"]
                ja["topbox-title"] = js["title"]
                ja["topbox-link"]=js["link"]
                ja["topbox-description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
                ja["rank"]=1
                count = count + 1
                total.append(ja)
                continue
        if not js["description"] and count > 1:
            js["type"]="People also ask"
            des = soup.findAll("div",{"class":"match-mod-horizontal-padding hide-focus-ring cbphWd"})
            del js["description"]
            js["query"] = des[p].text.encode('ascii', 'ignore').decode("utf-8")
            p=p+1
            total.append(js)

    related = soup.find("div",{"class":"card-section"})
    topics=related.find_all("a")
    num=1
    for topic in topics:
        ja={}
        ja["original search"] = jj["original search"]
        ja["related-search"]=topic.text.encode('ascii', 'ignore').decode("utf-8")
        ja["rank"]=num
        num=num+1
        total.append(ja)
    newpage = soup.findAll("div",{"id":"foot"})

    pag = newpage[0].findAll("td")
    s1 = "https://www.google.co.in"
    newl = (pag[2].a["href"])
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
    count=1
    for mink in contents:
        js = {}
        js["original search"] = jj["original search"]
        js["page"] = 2
        js["type"] = "result"
        #js["rank"] = count
        js["title"] = mink.h3.text.encode('ascii', 'ignore').decode("utf-8")
        abcd = mink.find("a")
        js["link"] = abcd["href"]

        des = mink.find("span", {"class": "st"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        if js["description"]:
            js["rank"] = count
            count = count + 1
        total.append(js)
    related = soup.find("div", {"class": "card-section"})
    topics = related.find_all("a")
    num = 1
    for topic in topics:
        ja = {}
        ja["original search"] = jj["original search"]
        ja["related-search"] = topic.text.encode('ascii', 'ignore').decode("utf-8")
        ja["rank"] = num
        num = num + 1
        total.append(ja)

        #count=count+1
    # return our list of repositories as the output of our function

    with open('out.json') as f:
        data = json.load(f)
        f.close()
    data.extend(total)
    json_file = open('out.json', 'w')
    json.dump(data, json_file, indent=1)
    json_file.close()
    return total



with open('search.txt', 'r') as file_in:
    lines = []
    for line in file_in:
        line=line.replace(' ','+')
        str1="https://www.google.com/search?q="
        url = str1 + line
        print(url)
        #lines.append(line)
        print(json.dumps(scrap_website(url), indent=1))
        #time.sleep(2)