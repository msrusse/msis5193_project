import pandas as pd
from lxml import html, etree
import requests

#Pull in the website html
award_url = "https://en.wikipedia.org/wiki/Academy_Award_for_best_picture"
resp = requests.get(award_url)
award_tree = html.fromstring(resp.content)

#Find all movies that won best picture
movie = "//tr[@style='background:#FAEB86']/td[1]/i/b/a/text()"
movie = award_tree.xpath(movie)
#make a second list to indicate that the movie won
best_picture = []
for i in range(0,len(movie)):
    best_picture.append(True)
#Convert to a dataframe and export to csv
best_picture_data = pd.DataFrame({'movie' : movie,
                           'bestPicture' : best_picture})
best_picture_data.to_csv('best_picture.csv', index = False)