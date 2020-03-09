import json
from bs4 import BeautifulSoup
from selenium import webdriver
#from urllib.request import urlopen
import requests

# import the requests library to help use query a website


# import the BeautifulSoup library to help us parse the websites

driver = webdriver.Chrome()
# The function to query a website
def scrap_website(url):
    # query the web page
    # find the repositories container div
    driver.get(url)
    #html_page = requests.get(url)
    #uclient = urlopen(url)
    #html_page = uclient.read()
    #uclient.close()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    #print(soup.prettify())
    content = soup.findAll("div", {"class":"result__body links_main links_deep"})
    #print(content[0].pretify())
    total = []
    #print(content[0])

    for mink in content:
        js = {}

        abcd = mink.h2.find("a", {"class":"result__a"})
        js["title"] = abcd.text.encode('ascii', 'ignore').decode("utf-8")
        js["link"] = abcd["href"]
        des = mink.find("div", {"class": "result__snippet js-result-snippet"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)
    # return our list of repositories as the output of our function

    json_file = open('out.json', 'w')
    json.dump(total , json_file)
    json_file.close()
    return total


print(json.dumps(scrap_website("https://duckduckgo.com/?q=intimate+partner+violence&ia=web"), indent=1))
