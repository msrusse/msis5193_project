#! /usr/bin/python

import grequests
import json, glob, time, re
from bs4 import BeautifulSoup as bs
from progressbar import ProgressBar as pb

movies_by_market_path = 'data/movies_by_market'
movies_summary_path = 'data/movie_summaries'

def parse_json_files(file):
    with open(file) as infile:
        year_movies = json.load(infile)
        movie_urls = {}
        for movie in year_movies:
            movie_urls[year_movies[movie]['castURL']] = {
                'id' : year_movies[movie]['id'] 
            }
        return movie_urls

def determine_imdb_urls():
    imdb_urls = {}
    files = glob.glob('%s/*.json' % movies_by_market_path)
    for file in files:
        year = file.split('\\')[1][0:4]
        imdb_urls[year] = parse_json_files(file)
    return imdb_urls

def get_imdb_pages(movies):
    urls = list(movies.keys())
    split_urls = [urls[i:i + 25] for i in range(0, len(urls), 25)]
    responses = []
    for lst in split_urls:
        grequest = (grequests.get(str(url)) for url in lst)
        responses += (grequests.map(grequest))
        if len(split_urls) > 2:
            time.sleep(60)
    return responses

def parse_imdb_pages(movies, year_movies):
    for movie in movies:
        plot_summary = ''
        if movie is not None:
            if movie.status_code == 200:
                html_bs = bs(movie.text, features='lxml')
                title_description = html_bs.find('div', {'id' : 'title_summary'})
                if title_description is not None:
                    title_description = title_description.getText()
                    plot_summary = title_description.replace('\n', '').replace(' Read more: Plot summary', '').replace(' | Synopsis', '').replace('\u00e9', 'e').replace('\\', '')
                runtime = html_bs.find('span', {'id' : 'running_time'})
                if runtime is not None:
                    runtime = runtime.getText()
                    runtime = re.sub('[^0-9]+', '', runtime)
            else:
                plot_summary =  'N/A, status code: %s' % movie.status_code
                runtime = 'N/A, status code: %s' % movie.status_code
            if movie.url in year_movies.keys():
                year_movies[movie.url]['plotSummary'] = plot_summary
                year_movies[movie.url]['runtimeMinutes'] = runtime
            else:
                year_movies[movie.url] = {
                    'plotSummary' : plot_summary,
                    'runtimeMinutes' : runtime
                }
    return year_movies

def restructure_dict_to_file(movies, year):
    year_movies = {}
    for movie in movies:
        if 'plotSummary' in movies[movie].keys():
            year_movies[movies[movie]['id']] = {
                'plotSummary' : movies[movie]['plotSummary'],
                'runtimeMinutes' : movies[movie]['runtimeMinutes']
            }
    with open(movies_summary_path + '/%s_movie_summaries.json' % year, 'w') as outfile:
        json.dump(year_movies, outfile, sort_keys=True, indent=4)

all_movies = determine_imdb_urls()
bar = pb()
for year in bar(all_movies):
    movies = get_imdb_pages(all_movies[year])
    year_movies = parse_imdb_pages(movies, all_movies[year])
    restructure_dict_to_file(year_movies, year)