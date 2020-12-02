#! /usr/bin/python3

import json, csv, glob, os

data_path = '%s/data' % os.path.dirname(__file__)

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
    with open('%s/csv_files/box_office_movies.csv' % data_path, 'w', newline='') as csvfile:
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

def getMoviesByMarketYearJSON():
    return glob.glob('%s/movies_by_market/*.json' % data_path)

def getMovieSummariesByYearJSON():
    return glob.glob('%s/movie_summaries/*.json' % data_path)

def getMovieInformationByYearJSON():
    return glob.glob('%s/movie_information/valid_responses/*.json' % data_path)

def convertAllYearsIntoList(all_movies_by_year):
    all_movies_by_year_list = []
    for year_file in all_movies_by_year:
        all_movies_by_year_list.append(json.load(open('%s' % year_file)))
    return all_movies_by_year_list

def writeMoviesByMarketToCSV(movies_by_market):
    with open('%s/csv_files/movies_by_year_market.csv' % data_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'marketID', 'marketName', 'country', 'countryGrossAmount', 'countryOpeningAmount', 'countryReleaseDate'])
        for year in movies_by_market:
            for movie in year:
                current_movie = year[movie]
                for market in current_movie['markets']:
                    current_market = current_movie['markets'][market]
                    for country in current_market:
                        writer.writerow([current_movie['id'], market, marketName(market), countryName(country['country']), country['countryGrossAmount'], country['countryOpeningAmount'], country['countryReleaseDate']])

def writeOscarActorsToCSV(oscar_actors):
    with open('%s/csv_files/oscar_actors.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['actorName', 'award', 'movieName'])
        for actor in oscar_actors:
            for movie in actor['movies']:
                writer.writerow([actor['name'], actor['movies'][movie], movie])

def writeAcademyAwardWinnersToCSV(academy_award_winning_movies):
    with open('%s/csv_files/academy_award_winning_movies.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['movieName', 'year', 'nominations', 'awards', 'bestPicture'])
        for movie in academy_award_winning_movies:
            movie_dict = academy_award_winning_movies[movie]
            writer.writerow([movie_dict['movieName'], movie_dict['year'], movie_dict['nominations'], movie_dict['awards'], movie_dict['bestPicture']])

def writePlotSummariesToCSV(movie_summaries):
    with open('%s/csv_files/movie_summeries.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'plotSummary', 'runtime'])
        for year in movie_summaries:
            for movie in year:
                writer.writerow([movie, year[movie]['plotSummary'], year[movie]['runtimeMinutes']])

def convertRottenTomatoesListToDicts(rotten_tomatoes_movies):
    actors = {}
    ratings = {}
    content_ratings = {}
    directors = {}
    genres = {}
    production_companies = {}
    reviews = {}
    for year in rotten_tomatoes_movies:
        for movie in year:
            movie_dict = year[movie]
            actors[movie] = movie_dict['actors']
            ratings[movie] = {
                'totalAudienceReviews' : movie_dict['audienceRatings']['count'],
                'audienceReviewScore' : movie_dict['audienceRatings']['rating'],
                'totalCriticsReviews' : movie_dict['criticsRatings']['count'],
                'criticsReviewScore' : movie_dict['criticsRatings']['rating']
            }
            content_ratings[movie] = movie_dict['contentRating']
            directors[movie] = movie_dict['directors']
            genres[movie] = movie_dict['genre'].split(', ')
            production_companies[movie] = movie_dict['productionCompany']
            reviews[movie] = movie_dict['reviews']
    writeRottenTomatoesActors(actors)
    writeRottenTomatoesRatings(ratings)
    writeRottenTomatoesContentRatings(content_ratings)
    writeRottenTomatoesDirectors(directors)
    writeRottenTomatoesGenres(genres)
    writeRottenTomatoesProductionCompanies(production_companies)
    writeRottenTomatoesReviews(reviews)

def writeRottenTomatoesActors(actors):
    with open('%s/csv_files/all_movie_actors.csv'  % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'actor'])
        for movie in actors:
            for actor in actors[movie]:
                writer.writerow([movie, actor])

def writeRottenTomatoesRatings(ratings):
    with open('%s/csv_files/all_movie_ratings.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'totalAudienceReviews', 'audienceReviewScore', 'totalCriticsReviews', 'criticsReviewScore'])
        for movie in ratings:
            writer.writerow([movie, ratings[movie]['totalAudienceReviews'], ratings[movie]['audienceReviewScore'], ratings[movie]['totalCriticsReviews'], ratings[movie]['criticsReviewScore']])

def writeRottenTomatoesContentRatings(content_ratings):
    with open('%s/csv_files/all_movie_content_ratings.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'contentRating'])
        for movie in content_ratings:
            writer.writerow([movie, content_ratings[movie]])

def writeRottenTomatoesDirectors(directors):
    with open('%s/csv_files/all_movie_directors.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'director'])
        for movie in directors:
            for director in directors[movie]:
                writer.writerow([movie, director])

def writeRottenTomatoesGenres(genres):
    with open('%s/csv_files/all_movie_genres.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'genre'])
        for movie in genres:
            for genre in genres[movie]:
                writer.writerow([movie, genre])

def writeRottenTomatoesProductionCompanies(production_companies):
    with open('%s/csv_files/all_movie_production_companies.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'productionCompany'])
        for movie in production_companies:
            writer.writerow([movie, production_companies[movie]])

def writeRottenTomatoesReviews(reviews):
    with open('%s/csv_files/all_movie_reviews.csv' % data_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'review'])
        for movie in reviews:
            for review in reviews[movie]:
                writer.writerow([movie, review])


def main():
    box_office_totals = json.load(open('%s/box_office_movies.json' % data_path))
    convertBoxOfficeTotalsToCSV(box_office_totals)
    all_movies_by_year_market = getMoviesByMarketYearJSON()
    all_movies_by_year_market_list = convertAllYearsIntoList(all_movies_by_year_market)
    writeMoviesByMarketToCSV(all_movies_by_year_market_list)
    oscar_actors = json.load(open('%s/oscar_actors.json' % data_path))
    writeOscarActorsToCSV(oscar_actors)
    wikipedia_movies = json.load(open('%s/movies_from_wikipedia.json' % data_path))
    writeAcademyAwardWinnersToCSV(wikipedia_movies)
    all_movie_summaries = getMovieSummariesByYearJSON()
    all_movie_summaries_list = convertAllYearsIntoList(all_movie_summaries)
    writePlotSummariesToCSV(all_movie_summaries_list)
    rotten_tomatoes_movies = getMovieInformationByYearJSON()
    rotten_tomatoes_movies_list = convertAllYearsIntoList(rotten_tomatoes_movies)
    convertRottenTomatoesListToDicts(rotten_tomatoes_movies_list)

if __name__ == '__main__':
    main()