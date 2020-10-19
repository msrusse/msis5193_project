import pandas as pd
from lxml import html
from lxml import etree
import requests

#Pull in the website html
award_url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"
resp = requests.get(award_url)
award_tree = html.fromstring(resp.content)

#Find all movies that won best picture
Movie = "//tr[@style='background:#FAEB86']/td[1]/i/b/a/text()"
Movie = award_tree.xpath(Movie)
#make a second list to indicate that the movie won
Best_Picture = []
for i in range(0,len(Movie)):
    Best_Picture.append(True)
#Convert to a dataframe and export to csv
Best_Picture_data = pd.DataFrame({'Movie' : Movie,
                           'Best Picture' : Best_Picture})
Best_Picture_data.to_csv(r'C:\Users\Rrsha\source\repos\msis5193_project\Best_Picture.csv', index = False)
Best_Picture_data