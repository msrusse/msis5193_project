#! /usr/local/bin/python3

from bs4 import BeautifulSoup as BS
import json, requests
from progressbar import ProgressBar as pb
import wikipedia_scrape

rotten_tomatoes_url = 'https://www.rottentomatoes.com/m/'

def sanatizeHTMLStrings(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def getHTML(url, name):
    page = requests.get(url)
    html = BS(page.text, features='lxml')        
    return {
        'html': html,
        'status': page.status_code
    }

def convertMovieNameToURL(name):
    if '(' in name:
        name = name[:name.find('(')]
    search_term = sanatizeHTMLStrings(name, {
        ',': '',
        '-': ' ',
        '.': '',
        ':': '',
        ';': '',
        '\'': '',
        '&': 'and',
        ' ': '_'
    })
    if search_term[len(search_term)-1] == '_':
        search_term = search_term[:len(search_term)-1]
    if search_term == 'U_571':
        search_term = 'U571'
    return search_term

class Movie:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.critics_score = 'N/A'
        self.audience_score = 'N/A'
        self.retrieval_status = None
        self.html = ''

    def findRatings(self, html):
        ratings_spans = html.find_all(
            'span', attrs={'class': 'mop-ratings-wrap__percentage'})
        ratings_hrefs = html.find_all(
            'a', {'class': 'unstyled articleLink mop-ratings-wrap__icon-link'})
        if len(ratings_spans) == 2:
            critics_score = str(ratings_spans[0].text)
            audience_score = str(ratings_spans[1].text)
        elif len(ratings_spans) == 1:
            if str(ratings_hrefs[0]).find('#contentReviews') != -1:
                critics_score = str(ratings_spans[0].text)
            elif str(ratings_hrefs[0]).find('#audience_reviews') != -1:
                audience_score = str(ratings_spans[0].text)
        items_to_replace = {
            '\n': '',
            ' ': '',
            '%': ''
        }
        self.critics_score = sanatizeHTMLStrings(
            critics_score, items_to_replace)
        self.audience_score = sanatizeHTMLStrings(
            audience_score, items_to_replace)

movies_dict = wikipedia_scrape.getMovies()
bar = pb()
# TODO: Restructure code to work with returned dictionary
# for movie in movies_dict:
    # tomatos_movie_search = convertMovieNameToURL(movie)
    # new_movie = Movie(url=rotten_tomatoes_url + tomatos_movie_search, name=movie)
    # html_result = getHTML(new_movie.url, new_movie.name)
    # new_movie.retrieval_status = html_result['status']
    # new_movie.html = html_result['html']
    # if new_movie.retrieval_status == 200:
    #     new_movie.findRatings(new_movie.html)
    # movies_dict[tomatos_movie_search] = {
    #     'name' : movie,
    #     # 'html' : str(new_movie.html),
    #     # 'audince_score': new_movie.audience_score,
    #     # 'critics_score': new_movie.critics_score,
    #     'status' : new_movie.retrieval_status
    # }
with open('movies.json', 'w') as outfile:
    json.dump(movies_dict, outfile, sort_keys=True, indent=4)