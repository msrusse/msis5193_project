import pandas as pd
from lxml import html
from lxml import etree
import requests
import regex


Oscar_Actors_data = []
#Pull in the website html
for i in range(1,3):
    end = str(i)
    oscar_url = "https://www.imdb.com/list/ls052063533/?sort=list_order,asc&mode=detail&page="+end
    resp = requests.get(oscar_url)
    oscar_tree = html.fromstring(resp.content)
    #Find all movies that won awards
    Actors = '//h3[@class="lister-item-header"]/a/text()'
    Actors = oscar_tree.xpath(Actors)
    Oscar_Actors_data.append(Actors)

Oscar_Actors_data = 