#! /usr/bin/python

from bs4 import BeautifulSoup as BS
import numpy as np
import json, sys, requests, re

# Creates errors dictionary
errors = {}
# Sets the log file location
log = open("logs/imdb_oscar_actors_scrape.log", "a")
# Sets the standard output to console
primary_stdout = sys.stdout

def getOscarActorsWebpage():
    url = 'https://www.imdb.com/list/ls052063533/?page='
    request1 = requests.get(url + '1')
    request2 = requests.get(url + '2')
    return [request1, request2]

def checkStatusCode(response):
    if response:
        # If a valid response, return it
        if response and response.status_code == 200:
            return response
        # If the response is a server error, reattempt the response up to 25 times
        elif response and response.status_code == 503:
            # Makes individual request
            r=requests.get(response.url)
            checkStatusCode(r)
        # If the response has a nonvalid or server error response, add it to the errors file
        else:
            errors[response.url] = {
                'status' : response.status_code
            }
            return None
    # If response is none, log the response in the log file
    else:
        print('\n%s' % response)

def getOscarActorsFromResponse(response):
    response_html = BS(response.content, 'lxml')
    actors_divs = response_html.find_all('div', { 'class' : 'lister-item mode-detail' })
    actors_info = []
    for actor in actors_divs:
        movies_div = actor.find('div', { 'class' : 'list-description' })
        all_movies = movies_div.find('p').getText().replace('\n', ' ').replace('\u00e9', 'e')
        movie_indexes = [m.start() for m in re.finditer('\) ', all_movies)]
        year_indexes = [m.start() for m in re.finditer('\(', all_movies)]
        years = []
        movies = []
        for i in range(0,len(movie_indexes)):
            years.append(all_movies[year_indexes[i]+1:movie_indexes[i]])
            if i+1 == len(year_indexes):
                movies.append(all_movies[movie_indexes[i]+2:])
            else:
                movies.append(all_movies[movie_indexes[i]+2:year_indexes[i+1]])
        awards = {}
        for movie in movies:
            split = movie.split(' in ', 1)
            awards[split[1]] = split[0]
        actors_info.append({
            'name' : actor.find('h3').getText().replace('\n', '').replace('\u00e9', 'e').replace('  ', '').split('.')[1].rstrip(),
            'movies' : awards
        })
    return actors_info

def main():
    requests = getOscarActorsWebpage()
    actors = []
    print('\nGetting Oscar Winning Actors from IMDB...')
    for response in requests:
        if checkStatusCode(response):
            actors += getOscarActorsFromResponse(response)
    with open('data/oscar_actors.json', 'w') as outfile:
        json.dump(actors, outfile, sort_keys=True, indent=4)
    print('\nOscar Winning Actors Retrieved.')

if __name__ == '__main__':
    main()