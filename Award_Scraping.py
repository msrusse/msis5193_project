import pandas as pd
from lxml import html
from lxml import etree
import requests

#Pull in the website html
award_url = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"
resp = requests.get(award_url)
award_tree = html.fromstring(resp.content)

#Find all movies that won awards
Movie = "//table[@class='wikitable']/tbody/tr/td/i/b/a/text() | //table[@class='wikitable']/tbody/tr/td/i/a/text()"
Movie = award_tree.xpath(Movie)
Movie
#Convert to a dataframe and export to csv
Movie_Awards_data = pd.DataFrame({'Movie' : Movie})
Movie_Awards_data.to_csv(r'C:\Users\Rrsha\source\repos\msis5193_project\Movie_awards.csv', index = False)