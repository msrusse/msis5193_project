#1 /usr/bin/python3

import grequests
import json, time, re, os
from tqdm import tqdm
from colorama import init
from bs4 import BeautifulSoup as bs
import numpy as np
from pathlib import Path

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')

def get_all_movies():
    return json.load(open(os.path.join(data_path,'box_office_movies.json')))

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
    irregular_keys = {}
    with open(os.path.join(data_path, 'movie_information','irregular_movie_links.json')) as infile:
        irregular_keys = json.load(infile)
    for year in tqdm(movies, desc='Movie Ratings'):
        responses[year] = {}
        urls = []
        for movie in list(movies[year]):
            url_end = movie
            if movies[year][movie] in irregular_keys[year].keys():
                url_end = irregular_keys[year][movies[year][movie]]
                movie_titles_by_year[year][url_end] = movie_titles_by_year[year][movie]
            urls.append('https://www.rottentomatoes.com/m/%s' % url_end)
        split_urls = [urls[i:i + 75] for i in range(0, len(urls), 75)]
        year_responses = []
        for lst in split_urls:
            grequest = (grequests.get(str(url)) for url in lst)
            year_responses += (grequests.map(grequest))
            if len(split_urls) > 2:
                for i in range(100):
                    time.sleep(.45)
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
                    critics_ratings['count'] = int(info_json['aggregateRating']['ratingCount'])
                    critics_ratings['rating'] = int(info_json['aggregateRating']['ratingValue'])
                if 'contentRating' in info_json.keys():
                    content_rating = info_json['contentRating']
                if 'productionCompany' in info_json.keys():
                    production_company = info_json['productionCompany']['name']
                for director in info_json['director']:
                    directors.append(director['name'])
                audience_revies_div = soup.find('div', {'class' : 'audience-score'})
                try:
                    audience_rating = int(audience_revies_div.find('span', {'class' : 'mop-ratings-wrap__percentage'}).getText().replace('%', '').replace('\n', '').replace(' ', ''))
                except:
                    pass
                try:
                    total_audience_reviews = int(audience_revies_div.find('strong', {'class' : 'mop-ratings-wrap__text--small'}).getText())
                    total_audience_reviews = int(total_audience_reviews.replace(',', '').split(': ')[1])
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
    current_year_file = '%s_movie_information.json' % year
    valid_path = os.path.join(data_path, 'movie_information','valid_responses','%s' % current_year_file)
    if Path(valid_path).exists():
        current_results = json.load(open(valid_path))
        for movie in current_results:
            if movie not in movie_by_year_id.keys():
                movie_by_year_id[movie] = current_results[movie]
    with open('%s' % valid_path, 'w') as outfile:
        json.dump(movie_by_year_id, outfile, sort_keys=True, indent=4)
    incorrect_movies = list(set(movie_titles_by_year.values()) - set(movie_by_year_id.keys()))
    with open(os.path.join(data_path,'movie_information','invalid_responses','%s' % current_year_file), 'w') as outfile:
        json.dump(incorrect_movies, outfile, sort_keys=True, indent=4)

def main():
    init()
    movies = get_all_movies()
    movie_titles_by_year = get_movie_titles(movies)
    print('\nRetreiving Movies from Rotten Tomatoes...')
    movie_titles_by_year = get_rotten_tomatoes_name(movie_titles_by_year)
    get_movies_from_rotten_tomatoes(movie_titles_by_year, movie_titles_by_year)
    print('\nRotten Tomatoes Movies Retrieved.')

if __name__ == '__main__':
    main()