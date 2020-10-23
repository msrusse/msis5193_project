import pandas as pd
from lxml import html, etree
import requests, regex

oscar_actors_data = []
#Pull in the website html
for i in range(1,3):
    end = str(i)
    oscar_url = "https://www.imdb.com/list/ls052063533/?sort=list_order,asc&mode=detail&page="+end
    resp = requests.get(oscar_url)
    oscar_tree = html.fromstring(resp.content)
    #Find all movies that won awards
    actors = '//h3[@class="lister-item-header"]/a/text()'
    actors = oscar_tree.xpath(actors)
    oscar_actors_data.append(actors)
#Clean the data
oscar_actors_data0 = ''.join(oscar_actors_data[0])
oscar_actors_data1 = ''.join(oscar_actors_data[1])
oscar_actors_data = oscar_actors_data0 + oscar_actors_data1
oscar_actors_data = regex.findall("([A-zàâçéèêëîïôûùüÿñæœ'.-]+|[A-zàâçéèêëîïôûùüÿñæœ'.-]+ [A-zàâçéèêëîïôûùüÿñæœ'.-]+|[A-zàâçéèêëîïôûùüÿñæœ'.-]+ [A-zàâçéèêëîïôûùüÿñæœ'.-]+ [A-zàâçéèêëîïôûùüÿñæœ'.-]+)\\n", oscar_actors_data)
#Convert to a dataframe and export to csv
oscar_actors_data = pd.DataFrame({'oscarWinningActor' : oscar_actors_data})
oscar_actors_data.to_csv('oscar_actors.csv', index = False)
