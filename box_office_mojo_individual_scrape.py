#! python

from bs4 import BeautifulSoup as BS
import grequests
import json, csv, sys, time
from datetime import datetime
from progressbar import ProgressBar as pb

base_url = 'https://www.boxofficemojo.com/releasegroup/'
errors = {}

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
    for lst in split_urls:
        grequest = (grequests.get(base_url + str(url)) for url in lst)
        responses.append(grequests.map(grequest))
        time.sleep(10)
    return responses[0]

def determineValidResponse(individual_movies):
    valid_responses = []
    for response in individual_movies:
        if response is not None and response.status_code == 200:
            valid_responses.append(response)
        else:
            errors[response.url] = {
                'status' : response.status_codes
            }
    return valid_responses

def getTableInformation(valid_movie_responses, individual_movies):
    movie_information = individual_movies
    for response in valid_movie_responses:
        response_bs = BS(response.content, 'lxml')
        tables = response_bs.findAll('table', {'class' : 'releases-by-region'})
        url_id = response.url[response.url[:-1].rfind('/')+1:-1]
        cast_div = response_bs.find('div', {'a-box-inner'})
        cast_url = cast_div.findAll('a', href=True)[0]['href']
        movie_information[url_id]['castURL'] = cast_url
        for table in tables:
            rows = table.findAll('tr')
            market = marketKey(rows[0].getText())
            movie_information[url_id][market] = {}
            for row in rows[2:]:
                cols = row.findAll('td')
                country = cols[0].getText()
                sanitized_cols = sanitizeCols(cols[2:])
                country_key = country.replace(' ', '_').lower()
                movie_information[url_id][market][country_key] = {
                    'country' : country,
                    'release_date' : getDateTime(cols[1].getText().lower()),
                    'opening_amount' : sanitized_cols[0],
                    'gross_amount' : sanitized_cols[1]
                }
    return movie_information

def main():
    movies_dict = json.load(open('box_office_movies.json'))
    converted_movies = convertDict(movies_dict)
    bar = pb()
    for year in bar(converted_movies):
        individual_movies = getIndividualMovies(converted_movies[year])
        valid_movie_responses = determineValidResponse(individual_movies)
        converted_movies[year] = getTableInformation(valid_movie_responses, converted_movies[year])
    with open('box_office_movies_by_market.json', 'w') as outfile:
        json.dump(converted_movies, outfile, sort_keys=True, indent=4)
    with open('errors.json', 'w') as outfile:
        json.dump(errors, outfile, sort_keys=True, indent=4)
if __name__ == '__main__':
    main()