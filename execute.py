#! /usr/bin/python

import box_office_mojo_individual_scrape, box_office_mojo_scrape, get_imdb_info, get_movie_ratings, imdb_oscar_actors_scrape, wikipedia_scrape, write_json_to_csv
import os

def mkdirs():
    data_path = 'data'
    movie_information = '%s/movie_information' % data_path
    valid_responses = '%s/valid_responses' % movie_information
    invalid_responses = '%s/invalid_responses' % movie_information
    movie_summaries = '%s/movie_summaries' % data_path
    movies_by_market = '%s/movies_by_market' % data_path
    if os.path.isdir(data_path):
        if os.path.isdir(movie_information):
            if not os.path.isdir(valid_responses):
                os.mkdir(valid_responses)
            if not os.path.isdir(invalid_responses):
                os.mkdir(invalid_responses)
        else:
            os.mkdir(movie_information)
            mkdirs()
        if not os.path.isdir(movie_summaries):
            os.mkdir(movie_summaries)
        if not os.path.isdir(movies_by_market):
            os.mkdir(movies_by_market)
    else:
        os.mkdir(data_path)
        mkdirs()
    if not os.path.isdir('logs'):
        os.mkdir('logs')

def main():
    mkdirs()

if __name__ == '__main__':
    main()