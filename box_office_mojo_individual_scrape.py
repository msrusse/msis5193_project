#! python

from bs4 import BeautifulSoup as BS
import grequests
import json, datetime, csv
from progressbar import ProgressBar as pb

base_url = 'https://www.boxofficemojo.com'

def getMovieUrls(movies):
    urls = {}
    for year in movies:
        urls[year] = []
        for rank in movies[year]:
            urls[year].append(base_url + movies[year][rank]['individual_url'])
    return urls

def getIndividualMovies(urls):
    responses = []
    bar = pb()
    for year in bar(urls):
        grequest = (grequests.get(url) for url in urls[year])
        responses.append(grequests.map(grequest))
    return responses

def determineValidResponse(individual_movies):
    bar = pb()
    valid_responses = []
    for response in bar(individual_movies):
        if response is not None and response.status_code == 200:
            valid_responses.append(response)
    return valid_responses

def main():
    movies = json.load(open('box_office_movies.json'))
    urls = getMovieUrls(movies)
    individual_movies = getIndividualMovies(urls)
    valid_movie_responses = determineValidResponse(individual_movies)

if __name__ == '__main__':
    main()