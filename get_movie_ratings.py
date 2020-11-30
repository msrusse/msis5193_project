#1 /usr/bin/python

import grequests
import json, time, re
from bs4 import BeautifulSoup as bs
from multiprocessing import Process
from tqdm import tqdm
from colorama import init

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
        sanitized_movie_names[year] = {}
        for movie in movies[year]:
            movie_name = movies[year][movie]
            if movie_name[:4] == 'The ':
                movie_name = movie_name[4:]
            elif movie_name[:2] == 'A ':
                movie_name = movie_name[2:]
            elif movie_name[:3] == 'An ':
                movie_name = movie_name[3:]
            movie_name = re.sub('[^0-9a-zA-Z\\s]+', '', movie_name)
            movie_name = movie_name.replace(' ', '_').lower()
            sanitized_movie_names[year][movie_name] = movie
    return sanitized_movie_names

def get_movies_from_rotten_tomatoes(movies, movie_titles_by_year):
    responses = {}
    for year in tqdm(movies, desc='All Years'):
        responses[year] = {}
        urls = []
        for movie in movies[year]:
            urls.append('https://www.rottentomatoes.com/m/%s' % movie)
        split_urls = [urls[i:i + 50] for i in range(0, len(urls), 50)]
        year_responses = []
        for lst in tqdm(split_urls, desc='%s' % year):
            grequest = (grequests.get(str(url)) for url in lst)
            year_responses += (grequests.map(grequest))
            if len(split_urls) > 2:
                for i in tqdm(range(100)):
                    time.sleep(.6)
        responses[year] = year_responses
        parse_rotten_tomatoes_pages(responses[year], movie_titles_by_year[year], year)

def parse_rotten_tomatoes_pages(movie_responses, movie_titles_by_year, year):
    movies = {}
    for movie in movie_responses:
        actors = []
        critics_ratings = {}
        directors = []
        reviews = []
        production_company = ''
        content_rating = ''
        audience_rating = ''
        total_audience_reviews = ''
        genre = ''
        if movie is not None:
            if movie.status_code == 200:
                soup = bs(movie.content, features='lxml')
                info_script = soup.find('script', type='application/ld+json').string
                info_json = json.loads(info_script)
                if 'actors' in info_json.keys():
                    for actor in info_json['actors']:
                        actors.append(actor['name'])
                if 'review' in info_json.keys():
                    for review in info_json['review']:
                        reviews.append(review['reviewBody'])
                if 'aggregateRating' in info_json.keys():
                    critics_ratings['count'] = info_json['aggregateRating']['ratingCount']
                    critics_ratings['rating'] = info_json['aggregateRating']['ratingValue']
                    critics_ratings['best'] = info_json['aggregateRating']['bestRating']
                    critics_ratings['worst'] = info_json['aggregateRating']['worstRating']
                if 'contentRating' in info_json.keys():
                    content_rating = info_json['contentRating']
                if 'productionCompany' in info_json.keys():
                    production_company = info_json['productionCompany']['name']
                for director in info_json['director']:
                    directors.append(director['name'])
                try:
                    audience_rating = int(soup.find('span', {'class' : 'mop-ratings-wrap__percentage'}).getText().replace('%', '').replace('\n', '').replace(' ', ''))
                except:
                    pass
                try:
                    total_audience_reviews = soup.find('strong', {'class' : 'mop-ratings-wrap__text--small'}).getText().replace(',', '').split(': ')[1]
                except:
                    pass
                genre_div = soup.find('div', {'class' : 'genre'})
                if genre_div is not None:
                    genre = genre_div.getText().replace('\n', '').replace('  ', '')
                movies[movie.url.rsplit('/', 1)[1]] = {
                    'actors' : actors,
                    'criticsRatings' : critics_ratings,
                    'directors' : directors,
                    'reviews' : reviews,
                    'productionCompany' : production_company,
                    'contentRating' : content_rating,
                    'audienceRatings' : {
                        'rating' : audience_rating,
                        'count' : total_audience_reviews
                    },
                    'genre' : genre
                }
    get_id_for_movies(movies, movie_titles_by_year, year)

def get_id_for_movies(movie_information, movie_titles_by_year, year):
    movie_by_year_id = {}
    for movie in movie_information:
        movie_by_year_id[movie_titles_by_year[movie]] = movie_information[movie]
    with open('data/movie_information/valid_responses/%s_movie_information.json' % year, 'w') as outfile:
        json.dump(movie_by_year_id, outfile, sort_keys=True, indent=4)
    incorrect_movies = list(set(movie_titles_by_year.values()) - set(movie_by_year_id.keys()))
    with open('data/movie_information/invalid_responses/%s_movie_information.json' % year, 'w') as outfile:
        json.dump(incorrect_movies, outfile, sort_keys=True, indent=4)

init()
movies = get_all_movies()
movie_titles_by_year = get_movie_titles(movies)
movie_titles_by_year = get_rotten_tomatoes_name(movie_titles_by_year)
get_movies_from_rotten_tomatoes(movie_titles_by_year, movie_titles_by_year)