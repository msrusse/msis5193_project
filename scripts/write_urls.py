#! /usr/bin/python3

import json, csv, glob

def convertBoxOfficeTotalsToCSV(movies):
    urls = []
    for year in movies:
        for movie_rank in movies[year]:
            urls.append([movies[year][movie_rank]['movieName'], 'https://www.boxofficemojo.com/releasegroup/%s' % movies[year][movie_rank]['individualURL']])
    return urls

def getMoviesByYearJSON():
    return glob.glob('data/movies_by_market/*.json')

def convertAllYearsIntoList(all_movies_by_year_market):
    all_movies_by_year_market_list = []
    for year_file in all_movies_by_year_market:
        all_movies_by_year_market_list.append(json.load(open('%s' % year_file)))
    return all_movies_by_year_market_list

def writeMoviesByMarketToCSV(movies_by_market):
    urls = []
    for year in movies_by_market:
        for movie in year:
            urls.append([year[movie]['movieName'], year[movie]['castURL']])
    return urls

def writeAcademyAwardWinnersToCSV(academy_award_winning_movies):
    urls = []
    for movie in academy_award_winning_movies:
        movie_dict = academy_award_winning_movies[movie]
        urls.append([movie_dict['movieName'], movie_dict['rottenTomatoes']])
        urls.append([movie_dict['movieName'], movie_dict['wikiLink']])
    return urls

def main():
    box_office_totals = json.load(open('data/box_office_movies.json'))
    urls = convertBoxOfficeTotalsToCSV(box_office_totals)
    all_movies_by_year_market = getMoviesByYearJSON()
    all_movies_by_year_market_list = convertAllYearsIntoList(all_movies_by_year_market)
    urls += writeMoviesByMarketToCSV(all_movies_by_year_market_list)
    wikipedia_movies = json.load(open('data/movies_from_wikipedia.json'))
    urls += writeAcademyAwardWinnersToCSV(wikipedia_movies)
    print('All urls used for this project can be found here: ttps://rr.noordstar.me/737b2e0f')
    with open('urls_used.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['movieName', 'URL'])
        for url in urls:
            writer.writerow([url[0], url[1]])

if __name__ == '__main__':
    main()