import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.common.exceptions import TimeoutException


def scrap_website(url):
    driver = webdriver.Chrome()
    driver.get(url)
    #el = driver.find_element_by_css_selector(".ico.bingdd-arrow-down")
    #webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    #time.sleep(2)
    #webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    #time.sleep(2)
    #webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    #time.sleep(2)
    #webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    #time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    #print(soup.prettify())
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
        #desc = soup.find("div",{"class":"kno-rdesc"})
        js["box_description"] = para[1].text.encode('ascii', 'ignore').decode("utf-8")
        if len(para)>2:
            js["more description"] = para[2].text.encode('ascii', 'ignore').decode("utf-8")
        #link = soup.find("a",{"class":"q ruhjFe NJLBac fl"})
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
        js["box_title"] = para[1].a.text.encode('ascii', 'ignore').decode("utf-8")
        #desc = soup.find("div",{"class":"kno-rdesc"})
        js["box_description"] = para[0].text.encode('ascii', 'ignore').decode("utf-8")
        js["link_attached"] = para[1].a["href"]
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
        js["description"] = des[0].text.encode('ascii', 'ignore').decode("utf-8")
        #if js["description"]:
        js["rank"] = count
        count = count + 1
        total.append(js)
        #continue
        #if not js["description"] and count<2:
         #   des = soup.find("span", {"class": "ILfuVd"})
          #  print(des)
           # if des:
            #    ja={}
             #   ja["original search"] = jj["original search"]
              #  ja["topbox-title"] = js["title"]
               # ja["topbox-link"]=js["link"]
                #ja["topbox-description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
                #ja["rank"]=1
                #count = count + 1
                #total.append(ja)
                #continue
        #if not js["description"] and count > 1:
        #    js["type"]="People also ask"
        #    des = soup.findAll("div",{"class":"match-mod-horizontal-padding hide-focus-ring cbphWd"})
        #    del js["description"]
        #    js["query"] = des[p].text.encode('ascii', 'ignore').decode("utf-8")
        #    p=p+1
        #    total.append(js)
###################################################################################
    related = soup.find("table",{"class":"compTable m-0 ac-1st td-n fz-ms"})
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
    s1 = "https://search.yahoo.com/search?q="
    newurl = (pag[0]["href"])
    #print(newurl)
    #newurl = s1 + newl
    driver = webdriver.Chrome()
    try:
        driver.get(newurl)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

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
        js["description"] = des[0].text.encode('ascii', 'ignore').decode("utf-8")
        # if js["description"]:
        js["rank"] = count
        count = count + 1
        total.append(js)

    related = soup.find("table", {"class": "compTable m-0 ac-1st td-n fz-ms"})
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
        str1="https://search.yahoo.com/search?q="
        url = str1 + line
        print(url)
        #lines.append(line)
        print(json.dumps(scrap_website(url), indent=1))
        #time.sleep(2)