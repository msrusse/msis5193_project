#! /usr/bin/python3

import json, csv, glob

def marketName(market_id):
    return {
        'domestic' : 'Domestic',
        'emea' : 'Europe, Middle East, and Africa',
        'latin_america' : 'Latin America',
        'latine_america' : 'Latin America',
        'asia_pacific' : 'Asia Pacific',
        'china' : 'China'
    }.get(market_id, market_id)

def countryName(country_name):
    return {
        'Domestic' : 'United States of America'
    }.get(country_name, country_name)

def convertBoxOfficeTotalsToCSV(movies):
    with open('data/csv_files/box_office_movies.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        # Writes column headers to the first row
        writer.writerow(['uniqueID', 'movieName', 'yearRank', 'year', 'worldwideTotal', 'domesticTotal', 'domesticPercent', 'foreignTotal', 'foreignPercent'])
        # Since this is a nested dict, I first loop through the years then through the rankings that year
        for year in movies:
            for movie_rank in movies[year]:
                # Takes the year of the movie and its box office rank to create a unique ID for that movie
                unique_id = '%s_%s' % (year, movie_rank)
                movie = movies[year][movie_rank]
                writer.writerow([unique_id, movie['movieName'], movie_rank, year, movie['worldwideTotal'], movie['domesticTotal'], movie['domesticPercent'], movie['foreignTotal'], movie['foreignPercent']])

def getMoviesByYearJSON():
    return glob.glob('data/movies_by_market/*.json')

def convertAllYearsIntoList(all_movies_by_year_market):
    all_movies_by_year_market_list = []
    for year_file in all_movies_by_year_market:
        all_movies_by_year_market_list.append(json.load(open('%s' % year_file)))
    return all_movies_by_year_market_list

def writeMoviesByMarketToCSV(movies_by_market):
    with open('data/csv_files/movies_by_year_market.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'marketID', 'marketName', 'country', 'countryGrossAmount', 'countryOpeningAmount', 'countryReleaseDate'])
        for year in movies_by_market:
            for movie in year:
                current_movie = year[movie]
                for market in current_movie['markets']:
                    current_market = current_movie['markets'][market]
                    for country in current_market:
                        writer.writerow([current_movie['id'], market, marketName(market), countryName(country['country']), country['countryGrossAmount'], country['countryOpeningAmount'], country['countryReleaseDate']])

def writeAcademyAwardWinnersToCSV(academy_award_winning_movies):
    with open('data/csv_files/academy_award_winning_movies.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['movieName', 'year', 'nominations', 'awards', 'bestPicture'])
        for movie in academy_award_winning_movies:
            movie_dict = academy_award_winning_movies[movie]
            writer.writerow([movie_dict['title'], movie_dict['year'], movie_dict['nominations'], movie_dict['awards'], movie_dict['bestPicture']])

def main():
    box_office_totals = json.load(open('data/box_office_movies.json'))
    convertBoxOfficeTotalsToCSV(box_office_totals)
    all_movies_by_year_market = getMoviesByYearJSON()
    all_movies_by_year_market_list = convertAllYearsIntoList(all_movies_by_year_market)
    writeMoviesByMarketToCSV(all_movies_by_year_market_list)
    wikipedia_movies = json.load(open('data/movies_from_wikipedia.json'))
    writeAcademyAwardWinnersToCSV(wikipedia_movies)

if __name__ == '__main__':
    main()