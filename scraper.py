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
        js["box_description"] = divv[0].span.span.text.encode('ascii', 'ignore').decode("utf-8")
        link = content[0].find("div",{"id":"iconset_19"})

        ll=link.findAll("a")
        js["link_attached"] = ll[0]["href"]
        total.append(js)


    content = soup.findAll("li", {"class":"b_algo"})
    for mink in content:
        js = {}
        abcd = mink.find("h2")
        js["title"] = abcd.a.text.encode('ascii', 'ignore').decode("utf-8")
        js["link"] = abcd.a["href"]
        abcd = mink.findAll("p")
        js["description"]=abcd[0].text.encode('ascii', 'ignore').decode("utf-8")
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


    json_file = open('out.json', 'w')
    json.dump(total , json_file)
    json_file.close()
    return total


print(json.dumps(scrap_website("https://www.bing.com/search?q=ipv+violence+types&qs=BT&pq=ipv+violence+&sk=BT1&sc=5-13&cvid=4C3E80B63B0F4551951730A5D95E95EF&FORM=QBRE&sp=2&ghc=1"), indent=1))
