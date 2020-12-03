#! /usr/bin/python3

import os
from bs4 import BeautifulSoup as BS
import numpy as np
import grequests
import json, sys, time, requests
from tqdm import tqdm
from colorama import init
from datetime import datetime

data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
# Base url used for individual box office mojo movies, will have the movie ID appended to it
base_url = 'https://www.boxofficemojo.com/releasegroup/'
# Creates dictionary for holding any errors in responses that are unhandled
errors = {}
# Sets the standard output to console
primary_stdout = sys.stdout
# Sets the log file location
log = open(os.path.join(log_path,'errors', 'box_office_mojo_individual.log'), "a")

# TODO: Write function to sanitize country names with weird characters

#Returns an ID for the specific markets for key:value pairing
def marketKey(market):
    return {
        'Domestic' : 'domestic',
        'Europe, Middle East, and Africa' : 'emea',
        'Latin America' : 'latinAmerica',
        'Asia Pacific' : 'asiaPacific',
        'China' : 'china'
    }.get(market, market)

# Easy dictionary look-up for characters to replace in order to sanitize earnings for float conversion
def charsToReplace(char):
    return {
        '$' : '',
        ' ' : '',
        ',' : ''
    }.get(char, char)

# Removes none-standard characters not converted along with extra formatting from HTML repsonses
def sanitizeCols(cols):
    sanitized = []
    for col in cols:
        text = col.getText().replace(u'\u2013', u'-').replace('\n', '').replace(',', '').replace(' ', '')
        if text != '-':
            text = float(text[1:])
        sanitized.append(text)
    return sanitized

# Converts the text date into a datetime object, then back into a string for use wtih JSON
def getDateTime(date):
    if date != '':
        date = datetime.strptime(date, '%b %d, %Y').strftime('%m/%d/%Y')
    return date

# Takes the dictionary read in from box_office_mojo_scrape and converts it into a dictionary for use with this script, and data reconciliation later
def convertDict(movies_dict):
    new_dict = {}
    for year in movies_dict:
        new_dict[year] = {}
        for movie in movies_dict[year]:
            current_dict = movies_dict[year][movie]
            new_dict[year][current_dict['individualURL']] = current_dict
            new_dict[year][current_dict['individualURL']]['id'] = '%s_%s' % (year, movie)
    return new_dict

# Creates the url for each individual movie based off of it's unique identifier
def getMovieUrls(movies):
    urls = {}
    for year in movies:
        urls[year] = []
        for rank in movies[year]:
            urls[year].append(base_url + movies[year][rank]['individualURL'])
    return urls

# Grequests call for all of the individual movie pages
def getIndividualMovies(movies):
    # Converts the keys into a list, keys are the urls
    urls = list(movies.keys())
    # Splits the urls into lists of 100, Box Office Mojo anti-ddos protocals kick in with more requests
    split_urls = [urls[i:i + 25] for i in range(0, len(urls), 25)]
    responses = []
    # Loops through each list of 100
    for lst in tqdm(split_urls, desc='Box Office Mojo Individual'):
        # Grequest module adds each url in the set of 100 to the request object
        grequest = (grequests.get(base_url + str(url)) for url in lst)
        # Adds the responses to the overall list to be returned. grequests.map sends the requests asynchronously
        responses += (grequests.map(grequest))
        if len(split_urls) > 2:
            time.sleep(45)
    return responses

# Checks the status of each response
def checkStatusCode(response, attempts=0):
    if response:
        # If a valid response, return it
        if response and response.status_code == 200:
            return response
        # If the response is a server error, reattempt the response up to 25 times
        elif response and response.status_code == 503 and attempts<=25:
            attempts += 1
            # Give extra sleep time if sending a lot of requests
            if attempts>20:
                time.sleep(3)
            # Makes individual request
            r=requests.get(response.url)
            checkStatusCode(r, attempts)
        # If the response has a nonvalid or server error response, add it to the errors file
        else:
            errors[response.url] = {
                'status' : response.status_code,
                'id' : response.url[response.url[:-1].rfind('/')+1:-1],
                'attempts' : attempts
            }
            return None
    # If response is none, log the response in the log file
    else:
        sys.stdout = log
        print('After %s attempts: %s' % (attempts, response))
        sys.stdout = primary_stdout

# Checks if the responses are valid and only returns if a valid value exists
def determineValidResponse(individual_movies):
    valid_responses = []
    for response in individual_movies:
        checked_response = checkStatusCode(response)
        if checked_response:
            valid_responses.append(checked_response)
    return valid_responses

# Parses out the box office results for each region
def getTableInformation(valid_movie_responses, converted_movies, retry=False, individual_movies_by_year=None):
    # Determines if this is a single retry attempt or not
    if retry:
        movie_information = individual_movies_by_year
    else:
        movie_information = {}
    for response in valid_movie_responses:
        # Converts response to a beautiful soup object
        response_bs = BS(response.content, 'lxml')
        # Grabs all tables with the releases-by-region class
        tables = response_bs.findAll('table', {'class' : 'releases-by-region'})
        # Gets the unique ID for the movie from the response URL
        url_id = response.url[response.url[:-1].rfind('/')+1:-1]
        # Gets the div for url to the cast info - Used in another script to pull that data
        cast_div = response_bs.find('div', {'a-box-inner'})
        # Gets the speicifc link from the cast_div
        cast_url = cast_div.findAll('a', href=True)[0]['href']
        # Creates the dictionary instance for the individual movie and adds necessary details
        movie_information[url_id] = {
            'id': converted_movies[url_id]['id'],
            'individualURL': url_id,
            'movieName' : converted_movies[url_id]['movieName'],
            'castURL' : cast_url,
            'markets' : {}
        }
        # Parses through each table for market information
        for table in tables:
            # Finds all Table Rows
            rows = table.findAll('tr')
            # Pulls the market name from the first row of the table
            market = marketKey(rows[0].getText())
            # Adds the current market to the movie market dictionary
            movie_information[url_id]['markets'][market] = []
            # Parses through each table row - skipping the first line that contains the market name and second line that contains the table headers
            for row in rows[2:]:
                # Finds all the columns in the table
                cols = row.findAll('td')
                # Pulls the country name from the first column
                country = cols[0].getText()
                # Sanitizes all columns that have numerical data
                sanitized_cols = sanitizeCols(cols[2:])
                # Appends the current market information from the country to the list
                movie_information[url_id]['markets'][market].append({
                        'country' : country,
                        'countryReleaseDate' : getDateTime(cols[1].getText().lower()),
                        'countryOpeningAmount' : sanitized_cols[0],
                        'countryGrossAmount' : sanitized_cols[1]
                })
    return movie_information
  
# Determines which movies were not able to have their individual page retrieved
def determineMoviesNotFound(individual_movies_by_year, converted_movies, year):
    missing_movies = np.setdiff1d(converted_movies, individual_movies_by_year)
    # Logs the missing movies
    for movie in missing_movies:
        sys.stdout = log
        print('Movie ID %s was not determined in %s. Re-attempting...' % (movie, year))
        sys.stdout = primary_stdout
    return missing_movies

def main():
    init()
    # Sets the current start time for the script
    start_time = datetime.now()
    # Sets the output to the log file
    sys.stdout = log
    #Prints the start time for the script to the log file
    print('\nScript began running at: %s' % start_time)
    # Reverts standard out to the console
    sys.stdout = primary_stdout
    # Loads in the box office movies from the JSON file written in box_office_mojo_scrape
    movies_dict = json.load(open(os.path.join(data_path, 'box_office_movies.json')))
    # Calls the convertDict function for loaded movies
    converted_movies = convertDict(movies_dict)
    # Creates the individual movie dictionary
    # Loops through each year of the movies
    for year in converted_movies:
        year_file = os.path.join(data_path, 'movies_by_market', '%s_movies_by_market.json' % year)
        current_year = datetime.now().year
        if not os.path.exists(year_file) or (year == str(current_year) or year == str(current_year-1)):
            print('\nGetting movies for %s...' % year)
            # Calls the getIndividualMovies function for all movies in the current year
            individual_movies = getIndividualMovies(converted_movies[year])
            print('\nMovies Retrieved.\nDetermining valid responses for %s...' % year)
            # Calls the determineValidResponses function
            movie_responses = determineValidResponse(individual_movies)
            print('\nValid Responses Determined.\nParsing movies for %s...' % year)
            # Calls the getTableInformation function
            individual_movies_by_year = getTableInformation(movie_responses, converted_movies[year])
            # Converts the dictionary keys to lists, pulling all movies from the original dictionary and current year to compare with individual pages pulled
            missing_movies = determineMoviesNotFound(list(individual_movies_by_year.keys()), list(converted_movies[year].keys()), year)
            # If there are missing movies, attempts to recall those movies-
            if len(missing_movies) > 0:
                new_requests = []
                # Makes the requests for all missing movies
                for movie in missing_movies:
                    new_requests.append(requests.get(base_url + movie))
                # Determines if the retried requests are valid
                retried_movie_responses = determineValidResponse(new_requests)
                # Calls the getTableInformation and sets the retry flag to True
                individual_movies_by_year = getTableInformation(retried_movie_responses, converted_movies[year], True, individual_movies_by_year)
            # Writes data to new JSON file
            with open(year_file, 'w') as outfile:
                json.dump(individual_movies_by_year, outfile, sort_keys=True, indent=4)
            print('\nMovies Parsed. Sleeping for anti DDOS...')
            # Adds in a sleep time between years to further prevent inadvertant DDOSing
            for i in range(100):
                time.sleep(.2)
                if int(year) > 2015:
                    time.sleep(.1)
    # Writes errors dict to errors.json, if any exist
    if len(errors) > 0:
        with open(os.path.join(log_path, 'movies_by_market', 'errors.json'), 'w') as outfile:
            json.dump(errors, outfile, sort_keys=True, indent=4)
    # Prints the run time of the script to the log file
    sys.stdout = log
    print('Time to run: %s' % (datetime.now() - start_time))

if __name__ == '__main__':
    main()