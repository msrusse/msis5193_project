#! /usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS

def sanatize_html_strings(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

class Movie:
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def getHTML(self):
        print('Retrieving %s HTML...\n' % self.name)
        page = urlopen(test_movie.url)
        html = BS(page.read(), features='lxml')
        print('HTML received.\n')
        return html

    def findRatings(self, html):
        print('Determining ratings for %s...\n' % self.name)
        ratings_spans = html.find_all('span', attrs={'class': 'mop-ratings-wrap__percentage'})
        ratings_hrefs = html.find_all('a', {'class':'unstyled articleLink mop-ratings-wrap__icon-link'})
        critics_score = 'N/A'
        audience_score = 'N/A'
        if len(ratings_spans) == 2:
            critics_score = str(ratings_spans[0].text)
            audience_score = str(ratings_spans[1].text)
        elif len(ratings_spans) == 1:
           if str(ratings_hrefs[0]).find('#contentReviews') != -1:
               critics_score = str(ratings_spans[0].text)
           elif str(ratings_hrefs[0]).find('#audience_reviews') != -1:
               audience_score = str(ratings_spans[0].text)
        items_to_replace = {
            '\n' : '',
            ' ' : '',
            '%' : ''
        }
        critics_score = sanatize_html_strings(critics_score, items_to_replace)
        audience_score = sanatize_html_strings(audience_score, items_to_replace)
        print('Ratings Determined.\n')
        return {
            'critics': critics_score, 
            'audience': audience_score
        }

test_movie = Movie(url='https://www.rottentomatoes.com/m/learning_to_skateboard_in_a_warzone', name='Star Trek Beyond')
bs_html = test_movie.getHTML()
scores = test_movie.findRatings(bs_html)
print(scores)