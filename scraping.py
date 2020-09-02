#! /usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS

rotten_tomatoes_url = 'https://www.rottentomatoes.com/m/'

def sanatize_html_strings(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def getHTML(url, name):
        print('Retrieving %s HTML...\n' % name)
        page = urlopen(url)
        html = BS(page.read(), features='lxml')
        print('HTML received.\n')
        return html

def wikipedia_scrape():
    url = 'https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films'
    return getHTML(url, 'Wikipedia')

def determine_movies(html):
    content = html.find('table', {'class' : 'wikitable sortable'})
    movies_refs = content.find_all('i')
    movies_list = []
    for movie in movies_refs:
        try:
            title = movie.find('a').contents[0]
            movies_list.append(title)
        except:
            pass
    return movies_list

class Movie:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.critics_score = 0
        self.audience_score = 0

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
        self.critics_score = sanatize_html_strings(critics_score, items_to_replace)
        self.audience_score = sanatize_html_strings(audience_score, items_to_replace)
        print('Ratings Determined.\n')

wiki_html = wikipedia_scrape()
movies = determine_movies(wiki_html)
test_movie = Movie(url=rotten_tomatoes_url + 'learning_to_skateboard_in_a_warzone', name='Star Trek Beyond')
bs_html = getHTML(test_movie.url, test_movie.name)
test_movie.findRatings(bs_html)
print('%s, %s' % (test_movie.critics_score, test_movie.audience_score))