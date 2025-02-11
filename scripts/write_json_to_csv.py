#! /usr/bin/python3

import json, csv, glob, os

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
csv_path = os.path.join(data_path, 'csv_files')

def marketName(market_id):
    return {
        'domestic' : 'Domestic',
        'emea' : 'Europe, Middle East, and Africa',
        'latinAmerica' : 'Latin America',
        'asiaPacific' : 'Asia Pacific',
        'china' : 'China'
    }.get(market_id, market_id)

def countryName(country_name):
    return {
        'Domestic' : 'United States of America'
    }.get(country_name, country_name)

def convertBoxOfficeTotalsToCSV(movies):
    with open(os.path.join(csv_path, 'box_office_movies.csv'), 'w', newline='') as csvfile:
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
    return glob.glob(os.path.join(data_path, 'movies_by_market', '*.json'))

def getMovieSummariesByYearJSON():
    return glob.glob(os.path.join(data_path, 'movie_summaries', '*.json'))

def getMovieInformationByYearJSON():
    return glob.glob(os.path.join(data_path, 'movie_information', 'valid_responses', '*.json'))

def convertAllYearsIntoList(all_movies_by_year):
    all_movies_by_year_list = []
    for year_file in all_movies_by_year:
        all_movies_by_year_list.append(json.load(open('%s' % year_file)))
    return all_movies_by_year_list

def writeMoviesByMarketToCSV(movies_by_market):
    with open(os.path.join(csv_path, 'movies_by_year_market.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'marketID', 'marketName', 'country', 'countryGrossAmount', 'countryOpeningAmount', 'countryReleaseDate'])
        for year in movies_by_market:
            for movie in year:
                current_movie = year[movie]
                for market in current_movie['markets']:
                    current_market = current_movie['markets'][market]
                    for country in current_market:
                        writer.writerow([current_movie['id'], market, marketName(market), countryName(country['country']), country['countryGrossAmount'], country['countryOpeningAmount'], country['countryReleaseDate']])

def writeMoviesByMarketMonthsToCSV(movies_by_market):
    with open(os.path.join(csv_path, 'movies_by_year_month_market.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'monthNumber'])
        for year in movies_by_market:
            for movie in year:
                current_movie = year[movie]
                writer.writerow([current_movie['id'], current_movie['markets']['domestic'][0]['countryReleaseDate'].split('/', 1)[0]])

def writeOscarActorsToCSV(oscar_actors):
    with open(os.path.join(csv_path, 'oscar_actors.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['actorName', 'award', 'movieName'])
        for actor in oscar_actors:
            for movie in actor['movies']:
                writer.writerow([actor['name'], actor['movies'][movie], movie])

def writeAcademyAwardWinnersToCSV(academy_award_winning_movies):
    with open(os.path.join(csv_path, 'academy_award_winning_movies.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['movieName', 'year', 'nominations', 'awards', 'bestPicture'])
        for movie in academy_award_winning_movies:
            movie_dict = academy_award_winning_movies[movie]
            writer.writerow([movie_dict['movieName'], movie_dict['year'], movie_dict['nominations'], movie_dict['awards'], movie_dict['bestPicture']])

def writePlotSummariesToCSV(movie_summaries):
    with open(os.path.join(csv_path, 'movie_summeries.csv'), 'w', encoding='utf-8', newline='') as csvfile:
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
    writeGenreBools(genres)

def writeRottenTomatoesActors(actors):
    with open(os.path.join(csv_path, 'all_movie_actors.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'actor'])
        for movie in actors:
            for actor in actors[movie]:
                writer.writerow([movie, actor])

def writeRottenTomatoesRatings(ratings):
    with open(os.path.join(csv_path, 'all_movie_ratings.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'totalAudienceReviews', 'audienceReviewScore', 'totalCriticsReviews', 'criticsReviewScore'])
        for movie in ratings:
            writer.writerow([movie, ratings[movie]['totalAudienceReviews'], ratings[movie]['audienceReviewScore'], ratings[movie]['totalCriticsReviews'], ratings[movie]['criticsReviewScore']])

def writeRottenTomatoesContentRatings(content_ratings):
    with open(os.path.join(csv_path, 'all_movie_content_ratings.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'contentRating'])
        for movie in content_ratings:
            writer.writerow([movie, content_ratings[movie]])

def writeRottenTomatoesDirectors(directors):
    with open(os.path.join(csv_path,'all_movie_directors.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'director'])
        for movie in directors:
            for director in directors[movie]:
                writer.writerow([movie, director])

def writeRottenTomatoesGenres(genres):
    with open(os.path.join(csv_path,'all_movie_genres.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'genre'])
        for movie in genres:
            for genre in genres[movie]:
                writer.writerow([movie, genre])

def writeRottenTomatoesProductionCompanies(production_companies):
    with open(os.path.join(csv_path,'all_movie_production_companies.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'productionCompany'])
        for movie in production_companies:
            writer.writerow([movie, production_companies[movie]])

def writeRottenTomatoesReviews(reviews):
    with open(os.path.join(csv_path,'all_movie_reviews.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'review'])
        for movie in reviews:
            for review in reviews[movie]:
                writer.writerow([movie[:4], review])

def writeGenreBools(genres):
    with open(os.path.join(csv_path, 'movies_with_genre_bool.csv'), 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['uniqueID', 'fantasy', 'adventure', 'sci fi', 'action', 'comedy', 'kids and family', 'drama', 'horror', 'animation', 'crime', 'mystery and trhiller', 'musical', 'romance', 'music', 'war', 'other', 'biography', 'western', 'history', 'documentary', 'sports and fitness', 'anime', 'foreign'])
        for movie in genres:
            fantasy = 0 
            adventure = 0 
            scifi = 0 
            action = 0
            comedy = 0 
            kids_fam = 0 
            drama = 0 
            horror = 0 
            animation = 0 
            crime = 0 
            mystery_thrill = 0 
            musical = 0 
            romance = 0 
            music = 0 
            war = 0 
            other = 0 
            biography = 0 
            western = 0 
            history = 0 
            documentary = 0 
            sports_fitness = 0 
            anime = 0 
            foreign = 0
            for genre in genres[movie]:
                if genre == 'adventure':
                    adventure = 1
                elif genre == 'fantasy':
                    fantasy = 1
                elif genre == 'sci fi':
                    scifi = 1
                elif genre == 'action':
                    action = 1
                elif genre == 'comedy':
                    comedy = 1
                elif genre == 'kids and family':
                    kids_fam = 1
                elif genre == 'drama':
                    drama = 1
                elif genre == 'horror':
                    horror = 1
                elif genre == 'animation':
                    animation = 1
                elif genre == 'crime':
                    crime = 1
                elif genre == 'mystery and thriller':
                    mystery_thrill = 1
                elif genre == 'musical':
                    musical = 1
                elif genre == 'romance':
                    romance = 1
                elif genre == 'music':
                    music = 1
                elif genre == 'war':
                    war = 1
                elif genre == 'other':
                    other = 1
                elif genre == 'biography':
                    biography = 1
                elif genre == 'western':
                    western = 1
                elif genre == 'history':
                    history = 1
                elif genre == 'documentary':
                    documentary = 1
                elif genre == 'sports and fitness':
                    sports_fitness = 1
                elif genre == 'anime':
                    anime = 1
                elif genre == 'foreign':
                    foreign = 1 
            writer.writerow([movie, fantasy, adventure, scifi, action, comedy, kids_fam, drama, horror, animation, crime, mystery_thrill, musical, romance, music, war, other, biography, western, history, documentary, sports_fitness, anime, foreign])

def main():
    # box_office_totals = json.load(open(os.path.join(data_path, 'box_office_movies.json')))
    # convertBoxOfficeTotalsToCSV(box_office_totals)
    # all_movies_by_year_market = getMoviesByMarketYearJSON()
    # all_movies_by_year_market_list = convertAllYearsIntoList(all_movies_by_year_market)
    # writeMoviesByMarketToCSV(all_movies_by_year_market_list)
    # writeMoviesByMarketMonthsToCSV(all_movies_by_year_market_list)
    # oscar_actors = json.load(open(os.path.join(data_path, 'oscar_actors.json')))
    # writeOscarActorsToCSV(oscar_actors)
    # wikipedia_movies = json.load(open(os.path.join(data_path, 'movies_from_wikipedia.json')))
    # writeAcademyAwardWinnersToCSV(wikipedia_movies)
    # all_movie_summaries = getMovieSummariesByYearJSON()
    # all_movie_summaries_list = convertAllYearsIntoList(all_movie_summaries)
    # writePlotSummariesToCSV(all_movie_summaries_list)
    rotten_tomatoes_movies = getMovieInformationByYearJSON()
    rotten_tomatoes_movies_list = convertAllYearsIntoList(rotten_tomatoes_movies)
    convertRottenTomatoesListToDicts(rotten_tomatoes_movies_list)

if __name__ == '__main__':
    main()