import json
from bs4 import BeautifulSoup
from selenium import webdriver
import random
import time

# The function to query a website
def scrap_website(url):

    driver = webdriver.Chrome()
    el = driver.find_elements_by_id("wire1")

    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    time.sleep(1 + random.randint(1, 4))
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    time.sleep(1 + random.randint(1, 4))
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    time.sleep(1 + random.randint(1, 4))
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    time.sleep(1 + random.randint(1, 4))
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    total = []

    drd = soup.find("input", {"class": "b_searchbox"})
    jj = {}
    jj["original search"] = drd["value"]
    jj["type"] = "stats"
    drd = soup.find("span", {"class": "sb_count"})
    jj["stats"] = drd.text.encode('ascii', 'ignore').decode("utf-8")
    total.append(jj)


    content = soup.findAll("div", {"class": "b_subModule"})

    if content:

        js = {}
        js["type"]="box"
        js["box_title"] = content[0].h2.text.encode('ascii', 'ignore').decode("utf-8")
        divv = content[0].findAll("div")
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
        js["box_title"] = para[0].h2.a.text.encode('ascii', 'ignore').decode("utf-8")
        js["link_attached"] = para[0].h2.a["href"]
        para = content[0].findAll("div",{"class":"rwrl rwrl_pri rwrl_padref"})
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
            js["rank"] = count/2
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
    s1 = "https://www.bing.com"
    newl = (newpage[0]["href"])
    newurl = s1 + newl
    driver = webdriver.Chrome()
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
        str1="https://www.bing.com/search?q="
        url = str1 + line
        print(url)
        #lines.append(line)
        print(json.dumps(scrap_website(url), indent=1))
        #time.sleep(2)
