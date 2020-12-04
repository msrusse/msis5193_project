#! /usr/bin/python3

from multiprocessing.context import Process
from scripts import box_office_mojo_individual_scrape, box_office_mojo_scrape, get_imdb_info, get_movie_ratings, imdb_oscar_actors_scrape, wikipedia_scrape, write_json_to_csv
import os, json

def mkdirs():
    data_path = 'data'
    csv_path = '%s/csv_files' % data_path
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
        if not os.path.isdir(csv_path):
            os.mkdir(csv_path)
    else:
        os.mkdir(data_path)
        mkdirs()
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    if not os.path.isfile(os.path.join(movie_information, 'irregular_movie_links.json')):
        json.dump(json.load(open('sample_data/irregular_movie_links.json')), os.path.join(movie_information, 'irregular_movie_links.json'), sort_keys=True, indent=4)

def executeBoxOfficeMojo():
    box_office_mojo_scrape.main()
    box_office_mojo_individual_scrape.main()

def executeSinglePages():
    wikipedia_scrape.main()
    imdb_oscar_actors_scrape.main()

def executeIMDB():
    get_imdb_info.main()

def executeRottenTomatoes():
    get_movie_ratings.main()

def main():
    mkdirs()

if __name__ == '__main__':
    main()
    # p1 = Process(target=executeBoxOfficeMojo)
    # p1.start()
    # p2 = Process(target=executeSinglePages)
    # p2.start()
    # p1.join()
    # p2.join()
    # p3 = Process(target=executeIMDB)
    # p3.start()
    # p4 = Process(target=executeRottenTomatoes)
    # p4.start()
    # p3.join()
    # p4.join()
    # executeRottenTomatoes()
    write_json_to_csv.main()