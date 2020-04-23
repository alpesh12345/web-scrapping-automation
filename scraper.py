import json
from bs4 import BeautifulSoup
from selenium import webdriver

# The function to query a website
def scrap_website(url):

    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    total = []

    content = soup.findAll("div", {"class": "b_subModule"})

    if content:

        js = {}

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
        total.append(js)


    content = soup.findAll("li", {"class":"b_algo"})
    for mink in content:
        js = {}
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
    newpage = soup.findAll("a",{"class":"b_widePag sb_bp"})
    s1 = "https://www.bing.com"
    newl = (newpage[0]["href"])
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
        abcd = mink.find("h2")
        js["title"] = abcd.a.text.encode('ascii', 'ignore').decode("utf-8")
        js["link"] = abcd.a["href"]
        abcd = mink.findAll("p")
        js["description"]=abcd[0].text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)

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
