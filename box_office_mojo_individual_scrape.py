#! /usr/bin/python3

from bs4 import BeautifulSoup as BS
import numpy as np
import grequests
import json, csv, sys, time, requests
from datetime import datetime
from progressbar import ProgressBar as pb

base_url = 'https://www.boxofficemojo.com/releasegroup/'
errors = {}
primary_stdout = sys.stdout
log = open("box_office_mojo_individual.log", "a")

def marketKey(market):
    return {
        'Domestic' : 'domestic',
        'Europe, Middle East, and Africa' : 'emea',
        'Latin America' : 'latine_america',
        'Asia Pacific' : 'asia_pacific',
        'China' : 'china'
    }.get(market, market)

def charsToReplace(char):
    return {
        '$' : '',
        ' ' : '',
        ',' : ''
    }.get(char, char)

def sanitizeCols(cols):
    sanitized = []
    for col in cols:
        text = col.getText().replace(u'\u2013', u'-').replace('\n', '').replace(',', '').replace(' ', '')
        if text != '-':
            text = float(text[1:])
        sanitized.append(text)
    return sanitized

def getDateTime(date):
    if date != '':
        date = datetime.strptime(date, '%b %d, %Y').strftime('%m/%d/%Y')
    return date

def convertDict(movies_dict):
    new_dict = {}
    for year in movies_dict:
        new_dict[year] = {}
        for movie in movies_dict[year]:
            current_dict = movies_dict[year][movie]
            new_dict[year][current_dict['individual_url']] = current_dict
            new_dict[year][current_dict['individual_url']]['id'] = '%s_%s' % (year, movie)
    return new_dict

def getMovieUrls(movies):
    urls = {}
    for year in movies:
        urls[year] = []
        for rank in movies[year]:
            urls[year].append(base_url + movies[year][rank]['individual_url'])
    return urls

def getIndividualMovies(movies):
    urls = list(movies.keys())
    split_urls = [urls[i:i + 100] for i in range(0, len(urls), 100)]
    responses = []
    bar = pb()
    for lst in bar(split_urls):
        grequest = (grequests.get(base_url + str(url)) for url in lst)
        responses += (grequests.map(grequest))
        time.sleep(5)
        if len(urls) > 600:
            time.sleep(5)
    return responses

def checkStatusCode(response, attempts=0):
    if response:
        if response and response.status_code == 200:
            return response
        elif response and response.status_code == 503 and attempts<=25:
            attempts += 1
            if attempts>20:
                time.sleep(3)
            r=requests.get(response.url)
            checkStatusCode(r, attempts)
        else:
            errors[response.url] = {
                'status' : response.status_code,
                'id' : response.url[response.url[:-1].rfind('/')+1:-1],
                'attempts' : attempts
            }
            return None
    else:
        sys.stdout = log
        print('After %s attempts: %s' % (attempts, response))
        sys.stdout = primary_stdout

def determineValidResponse(individual_movies):
    valid_responses = []
    bar = pb()
    for response in bar(individual_movies):
        checked_response = checkStatusCode(response)
        if checked_response:
            valid_responses.append(checked_response)
    return valid_responses

def getTableInformation(valid_movie_responses, converted_movies, retry=False, individual_movies_by_year=None):
    if retry:
        movie_information = individual_movies_by_year
    else:
        movie_information = {}
    bar = pb()
    for response in bar(valid_movie_responses):
        response_bs = BS(response.content, 'lxml')
        tables = response_bs.findAll('table', {'class' : 'releases-by-region'})
        url_id = response.url[response.url[:-1].rfind('/')+1:-1]
        cast_div = response_bs.find('div', {'a-box-inner'})
        cast_url = cast_div.findAll('a', href=True)[0]['href']
        movie_information[url_id] = {
            'id': converted_movies[url_id]['id'],
            'individual_url': url_id,
            'name' : converted_movies[url_id]['name']
        }
        movie_information[url_id]['castURL'] = cast_url
        movie_information[url_id]['markets'] = []
        for table in tables:
            rows = table.findAll('tr')
            market = marketKey(rows[0].getText())
            for row in rows[2:]:
                cols = row.findAll('td')
                country = cols[0].getText()
                sanitized_cols = sanitizeCols(cols[2:])
                country_key = country.replace(' ', '_').lower()
                movie_information[url_id]['markets'].append({
                    market : {
                        country_key : {
                            'country' : country,
                            'release_date' : getDateTime(cols[1].getText().lower()),
                            'opening_amount' : sanitized_cols[0],
                            'gross_amount' : sanitized_cols[1]
                        }
                    }
                })
    return movie_information

def determineMoviesNotFound(individual_movies_by_year, converted_movies, year):
    missing_movies = np.setdiff1d(converted_movies, individual_movies_by_year)
    for movie in missing_movies:
        sys.stdout = log
        print('Movie ID %s was not determined in %s. Re-attempting...' % (movie, year))
        sys.stdout = primary_stdout
    return missing_movies

def main():
    start_time = datetime.now()
    sys.stdout = log
    print('\nScript began running at: %s' % start_time)
    sys.stdout = primary_stdout
    movies_dict = json.load(open('box_office_movies.json'))
    converted_movies = convertDict(movies_dict)
    individual_movies_by_year = {}
    for year in converted_movies:
        print('\nGetting movies for %s...' % year)
        individual_movies = getIndividualMovies(converted_movies[year])
        print('Movies Retrieved.\nDetermining valid responses for %s...' % year)
        movie_responses = determineValidResponse(individual_movies)
        print('Valid Responses Determined.\nParsing movies for %s...' % year)
        individual_movies_by_year[year] = getTableInformation(movie_responses, converted_movies[year])
        missing_movies = determineMoviesNotFound(list(individual_movies_by_year[year].keys()), list(converted_movies[year].keys()), year)
        if len(missing_movies) > 0:
            new_requests = []
            for movie in missing_movies:
                new_requests.append(requests.get(base_url + movie))
            retried_movie_responses = determineValidResponse(new_requests)
            individual_movies_by_year[year] = getTableInformation(retried_movie_responses, converted_movies[year], True, individual_movies_by_year[year])
        print('Movies Parsed. Sleeping for anti DDOS...')
        timer_bar = pb()
        for i in timer_bar(range(100)):
            time.sleep(.2)
            if int(year) > 2015:
                time.sleep(.1)
    with open('box_office_movies_by_market.json', 'w') as outfile:
        json.dump(individual_movies_by_year, outfile, sort_keys=True, indent=4)
    if len(errors) > 0:
        with open('errors.json', 'w') as outfile:
            json.dump(errors, outfile, sort_keys=True, indent=4)
    print('Time to run: %s' % (datetime.now() - start_time))

if __name__ == '__main__':
    main()