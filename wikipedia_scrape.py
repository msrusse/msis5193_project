#! /usr/local/bin/python3

from bs4 import BeautifulSoup as BS
import grequests
import json, requests
from progressbar import ProgressBar as pb

wikipedia_url = 'https://en.wikipedia.org'

class FeedbackCounter:
    """Object to provide a feedback callback keeping track of total calls."""
    def __init__(self):
        self.counter = 0

    def feedback(self, r, **kwargs):
        self.counter += 1
        print("{0} fetched, {1} total.".format(r.url, self.counter))
        return r

def getHTML(url):
    page = requests.get(url)
    html = BS(page.text, features='lxml')        
    return {
        'html': html,
        'status': page.status_code
    }

def determineMovies(html):
    content = html.find('table', {'class': 'wikitable sortable'})
    movies_refs = content.find_all('i')
    movies = {}
    for movie in movies_refs:
        try:
            if movie.find('a') is not None:
                title = movie.find('a').contents[0]
                wiki_link = wikipedia_url + movie.find('a')['href']
                movies[wiki_link] = {
                    'title' : title, 
                    'wiki_link' : wiki_link
                    }
        except Exception as e:
            print(e)
    return movies

def getMoviesOnWikipedia(movies):
    fbc = FeedbackCounter()
    response = (grequests.get(movie, callback=fbc.feedback) for movie in movies)
    mapped_response = grequests.map(response)
    return mapped_response

def parseWikipediaPages(response):
    response_bs = BS(response.text, features='lxml')
    hrefs = response_bs.find_all('a', href=True)
    rotten_tomatoes_links = 'N/A'
    for url in hrefs:
        if 'rottentomatoes.com' in url.get('href') and 'web.archive.org' not in url.get('href'):
            rotten_tomatoes_links = url.get('href')
    return rotten_tomatoes_links

def getMovies():
    all_award_winners = getHTML(wikipedia_url + '/wiki/List_of_Academy_Award-winning_films')
    if all_award_winners['status'] == 200:
        movies = determineMovies(all_award_winners['html'])
        mapped_response = getMoviesOnWikipedia(movies)
        bar = pb()
        for response in bar(mapped_response):
            if response is not None and response.status_code == 200:
                movies[response.url]['rotten_tomatoes'] = parseWikipediaPages(response)
        return movies

# with open('movies.json', 'w') as outfile:
#     json.dump(movies, outfile, sort_keys=True, indent=4)