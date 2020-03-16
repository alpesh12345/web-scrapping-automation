import json
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
# The function to query a website
def scrap_website(url):
    driver.get(url)
    el = driver.find_element_by_id("rld-1")
    webdriver.ActionChains(driver).move_to_element(el).click(el).perform()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    total = []
    content = soup.findAll("div", {"class": "module__body js-about-item"})
    if content:
        js = {}
        divv = content[0].findAll("div")
        js["box_title"] = divv[0].text.encode('ascii', 'ignore').decode("utf-8")
        js["box_description"] = divv[1].text.encode('ascii', 'ignore').decode("utf-8")
        link = divv[1].find("a", {"class": "module__more-at js-about-item-more-at-inline tx--bold"})
        js["link_attached"] = link["href"]
        total.append(js)


    content = soup.findAll("div", {"class":"result__body links_main links_deep"})
    for mink in content:
        js = {}

        abcd = mink.h2.find("a", {"class":"result__a"})
        js["title"] = abcd.text.encode('ascii', 'ignore').decode("utf-8")
        js["link"] = abcd["href"]
        des = mink.find("div", {"class": "result__snippet js-result-snippet"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        total.append(js)
    json_file = open('out.json', 'w')
    json.dump(total , json_file)
    json_file.close()
    return total


print(json.dumps(scrap_website("https://duckduckgo.com/?q=intimate+partner+violence&ia=web"), indent=1))
