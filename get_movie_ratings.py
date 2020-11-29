#1 /usr/bin/python

import grequests
import json, glob, time, re
from bs4 import BeautifulSoup as bs
from progressbar import ProgressBar as pb

def get_all_movies():
    with open('data/box_office_movies.json') as infile:
        return json.load(infile)

def get_movie_titles(movies):
    movie_titles = {}
    for year in movies:
        movie_titles[year] = {}
        for movie in movies[year]:
            movie_titles[year]['%s_%s' % (year, movie)] = movies[year][movie]['movieName']
    return movie_titles

def get_rotten_tomatoes_name(movies):
    sanitized_movie_names = {}
    for year in movies:
        for movie in movies[year]:
            movie_name = movies[year][movie]
            if movie_name[:4] == 'The ':
                movie_name = movie_name[4:]
            movie_name = re.sub('[^0-9a-zA-Z\\s]+', '', movie_name)
            movie_name = movie_name.replace(' ', '_').lower()
            sanitized_movie_names[movie_name] = movie
    return sanitized_movie_names

def get_movies_from_rotten_tomatoes(movies):
    urls = []
    for movie in movies:
        urls.append('https://www.rottentomatoes.com/m/%s' % movie)
    split_urls = [urls[i:i + 75] for i in range(0, len(urls), 75)]
    responses = []
    bar = pb()
    for lst in bar(split_urls):
        grequest = (grequests.get(str(url)) for url in lst)
        responses += (grequests.map(grequest))
    return responses

def parse_rotten_tomatoes_pages(movie_responses):
    for movie in movie_responses:
        actors = []
        critics_ratings = {}
        directors = []
        production_company = ''
        content_rating = ''
        audience_rating = ''
        if movie is not None:
            if movie.status_code == 200:
                soup = bs(movie.content, features='lxml')
                info_script = soup.find('script', {'type', 'application/ld+json'})
                info_json = json.loads(info_script[0])
                for actor in info_json['actors']:
                    actor_name = actor['name']
                    actor_name_split = actor_name.split(' ')
                    actors.append({'firstName' : actor_name_split[0], 'lastName' : actor_name_split[1]})
                critics_ratings['count'] = info_json['aggregateRating']['ratingCount']
                critics_ratings['rating'] = info_json['aggregateRating']['ratingValue']
                critics_ratings['best'] = info_json['aggregateRating']['bestRating']
                critics_ratings['worst'] = info_json['aggregateRating']['worstRating']
                content_rating = info_json['contentRating']
                production_company = info_json['productionCompany']['name']
                for director in info_json['director']:
                    director_name = director['name']
                    director_name_split = director_name.split(' ')
                    directors.append({'firstName' : director_name_split[0], 'lastName' : director_name_split[1]})
                
    return ''

movies = get_all_movies()
movie_titles_by_year = get_movie_titles(movies)
movie_titles_by_year = get_rotten_tomatoes_name(movie_titles_by_year)
movie_responses = get_movies_from_rotten_tomatoes(movie_titles_by_year)
movie_information = parse_rotten_tomatoes_pages(movie_responses)