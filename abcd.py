import json
from bs4 import BeautifulSoup
from selenium import webdriver
#from urllib.request import urlopen
import codecs
import re

# import the requests library to help use query a website


# import the BeautifulSoup library to help us parse the websites

def unmangle_utf8(match):
    escaped = match.group(0)                   # '\\u00e2\\u0082\\u00ac'
    hexstr = escaped.replace(r'\u00', '')      # 'e282ac'
    buffer = codecs.decode(hexstr, "hex")      # b'\xe2\x82\xac'

    try:
        return buffer.decode('utf8')           # '€'
    except UnicodeDecodeError:
        print("Could not decode buffer: %s" % buffer)

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
    content = soup.findAll("div", {"class":"rc"})
    #print(content[0].pretify())
    total = []
    #print(content[0])

    for mink in content:
        js = {}

        js["title"] = mink.h3.text.encode('ascii', 'ignore').decode("utf-8")
        abcd = mink.find("a")
        js["link"] = abcd["href"]


        des = mink.find("span", {"class": "st"})
        js["description"] = des.text.encode('ascii', 'ignore').decode("utf-8")
        #js["description"] = js["description"].decode("utf-8").encode("windows-1252").decode("utf-8")
        #js["description"] = des.text.decode('utf8')
        #js["description"] = re.sub(b'\\\u00([89a-f][0-9a-f])', lambda m: bytes.fromhex(m.group(1).decode()), des.text,flags=re.IGNORECASE)
        #js["description"] = re.sub(r"(?i)(?:\\u00[0-9a-f]{2})+", unmangle_utf8, des.text)
        total.append(js)
    # return our list of repositories as the output of our function


    json_file = open('out.json', 'w')
    json.dump(total , json_file)
    json_file.close()
    return total


print(json.dumps(scrap_website("https://www.google.co.in/search?sxsrf=ALeKk03JimFMbeftgaMShUSd2yF4tIncIQ%3A1583737742147&ei=jutlXufQCNfLrQHXx4_4BA&q=can+i+eat+banana+in+empty+stomach&oq=can+i+eat+&gs_l=psy-ab.3.8.35i39j0i67l2j0i20i263j0l6.5053.6504..14996...0.2..1.206.1523.0j8j1......0....1..gws-wiz.......0i71j0i22i30.-GrcTbIJAXc"), indent=1))
