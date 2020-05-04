#web-scrapping-automation
for links and description related to search engine query

just run script with search.txt in same folder and you will get output in
./result/"search_query"/search_engine_name.json

folder name is query joind by "_"

##Dependancies::
bs4
selenium
python version 3.2+
Limitation:: run duck.py with atmost 15 queries at a time

##Input::
search.txt containg all query (one query in one line)
in same folder where all scripts are saved
only run duck.py google1.py bing.py yahoo.py for correct output

##Output Format::         (fild_name,description)

original search: input search query
type: type of data like result, stats,etc (stats shows no. of results found,etc)
        and 'people also ask' shows that bow with related questions asked  
stats: stats shows no. of results found,etc
page: show page number
rank: result rank in that page number
title: title of the result
description: description associated with result
link_attached: link associated with result
query: associated with 'people also ask' questions
related_search: shows suggestions (present in the end of page,if available) 

special types-->
box_title/topbox_title: title associated with left box/topbox
box_link/topbox_link: link associated with left box/topbox
box_description/topbox_description: description associated with left box/topbox



##Sample Output format::

1)google
{
  "original search": "ipv4",
  "type": "stats",
  "stats": "About 4,56,00,000 results (0.57 seconds)"
 },
 {
  "original search": "ipv4",
  "page": 1,
  "type": "box", // left side box 
  "box_title": "IPv4Internet protocol",
  "box_description": "Internet Protocol.....",
  "link_attached": "https://en.w....."
 },
 {
  "original search": "ipv4",
  "topbox-title": "IPv4 - W",
  "topbox-link": "https://en.wik..",
  "topbox-description": "Internet Protocol versi....",
  "rank": 1
 },
 {
  "type": "People also ask",
  "original search": "ip",
  "page": 1,
  "title": "Pa..",
  "link": "https...",
  "query": "What is IPv4 address?"
 },
 {
  "type": "result",
  "original search": "ipv4",
  "page": 1,
  "title": "IP address - Wikipedia",
  "link": "https://..",
  "description": "An IPv4 a...",
  "rank": 2
 },
 {
  "page": 1,
  "original search": "ipv4",
  "related-search": "what....",
  "rank": 1
 }
 
 
 2)bing
 
 {
  "original search": "ipv4",
  "type": "stats",
  "stats": "1,22,00,000 results"
 },
 {
  "type": "box",
  "box_title": "IPv4",
  "box_description": "Internet Protocol vers....",
  "link_attached": "https://en....",
  "page": 1
 },
 {
  "original search": "ipv4",
  "page": 1,
  "rank": 1,
  "type": "people also ask",
  "query": "What is better IPv4 or IPv6?"
 },
 {
  "type": "result",
  "page": 1,
  "original search": "ipv4",
  "rank": 1,
  "title": "IPv4 - Wikipedia",
  "link": "https://en.wikipe.......",
  "description": "Internet Protocol........"
 },
 {
  "page": 2,
  "original search": "ipv4",
  "related-search": "what is my ipv4",
  "rank": 8
 }
 
 
 
 3)
 duckduckgo
 
 {
  "original search": "ipv4",
  "type": "box",
  "box_title": "IPv4",
  "box_description": "Internet Protocol version 4 is the fourth version of the Internet Protocol. It is one of the core protocols of standards-based internetworking methods in the Internet and other packet-switched networks. IPv4 was the first version deployed for production in the ARPANET in 1983.WikipediaMore at Wikipedia",
  "link_attached": "https://en.wikipedia.org/wiki/IPv4"
 },
 {
  "original search": "ipv4",
  "type": "result",
  "rank": 1,
  "title": "IPv4 - Wikipedia",
  "link": "https://en.wikipedia.org/wiki/IPv4",
  "description": "Internet Protocol version 4 (IPv4) is the fourth version of the Internet Protocol (IP). It is one of the core protocols of standards-based internetworking methods in the Internet and other packet-switched..."
 },
 
 
 4)yahoo
 
 {
  "original search": "ipv4",
  "type": "stats",
  "stats": "About 4,56,00,000 results (0.57 seconds)"
 },
 {
  "original search": "ipv4",
  "page": 1,
  "type": "box", // left side box 
  "box_title": "IPv4Internet protocol",
  "box_description": "Internet Protocol.....",
  "link_attached": "https://en.w....."
 },
 {
  "original search": "ipv4",
  "topbox-title": "IPv4 - W",
  "topbox-link": "https://en.wik..",
  "topbox-description": "Internet Protocol versi....",
  "rank": 1
 },
 {
  "type": "People also ask",
  "original search": "ip",
  "page": 1,
  "title": "Pa..",
  "link": "https...",
  "query": "What is IPv4 address?"
 },
 {
  "type": "result",
  "original search": "ipv4",
  "page": 1,
  "title": "IP address - Wikipedia",
  "link": "https://..",
  "description": "An IPv4 a...",
  "rank": 2
 },
 {
  "page": 1,
  "original search": "ipv4",
  "related-search": "what....",
  "rank": 1
 }
