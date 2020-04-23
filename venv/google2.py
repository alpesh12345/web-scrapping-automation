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


    content = soup.findAll("div",{"class":"SPZz6b"})
    if content:
        js = {}
        js["box_title"] = content[0].text.encode('ascii', 'ignore').decode("utf-8")
        desc = soup.find("div",{"class":"kno-rdesc"})
        js["box_description"] = desc.div.span.text.encode('ascii', 'ignore').decode("utf-8")
        link = soup.find("a",{"class":"q ruhjFe NJLBac fl"})
        js["link_attached"] = link["href"]
        total.append(js)


    content = soup.find_all("div", {"class":"rc"})
    count=1;
    for mink in content:
        js = {}
        js["rank"]=count
        js["title"] = mink.h3.text.encode('ascii', 'ignore').decode("utf-8")
        abcd = mink.find("a")
        js["link"] = abcd["href"]


        des = mink.find("span", {"class": "st"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)
        count=count+1
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
    for mink in contents:
        js = {}
        js["rank"] = count
        js["title"] = mink.h3.text.encode('ascii', 'ignore').decode("utf-8")
        abcd = mink.find("a")
        js["link"] = abcd["href"]

        des = mink.find("span", {"class": "st"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)
        count=count+1
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