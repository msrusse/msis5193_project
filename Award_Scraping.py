import pandas as pd
from lxml import html, etree
import requests

#Pull in the website html
award_url = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"
resp = requests.get(award_url)
award_tree = html.fromstring(resp.content)

#Find all movies that won awards
movie = "//table[@class='wikitable']/tbody/tr/td/i/b/a/text() | //table[@class='wikitable']/tbody/tr/td/i/a/text()"
movie = award_tree.xpath(movie)
#Convert to a dataframe and export to csv
movie_awards_data = pd.DataFrame({'movie' : movie})
movie_awards_data.to_csv('movie_awards.csv', index = False)