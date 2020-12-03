#! python

from bs4 import BeautifulSoup as BS
import grequests
import json, datetime, os
from tqdm import tqdm
from colorama import init

base_url = 'https://www.boxofficemojo.com/'
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def sanitizeNumbers(numbers):
    sanitized = []
    for number in numbers:
        san_number = number.getText().replace('%', '').replace(',', '').replace('$', '').replace('<', '')
        if san_number != '-':
            san_number = float(san_number)
        sanitized.append(san_number)
    return sanitized 

def getAllYears():
    # Use grequests to asyncronously get all box office results by year from 1977 (the first year) through currenty year.
    grequest = (grequests.get(base_url + 'year/world/%s' % year) for year in range(1977, int(datetime.datetime.now().year)+1))
    return grequests.map(grequest)

def parseBoxOfficeYear(year_page):
    # Converts the returned HTML into a BeautifulSoup Object
    response_bs = BS(year_page, 'lxml')
    # Finds the parent div for the page Table
    table_div = response_bs.find('div', {'class': 'imdb-scroll-table-inner'})
    # Retrieves the table from the div
    table = table_div.find('table')
    # Gets all table rows and excludest the first row, which is just table headers
    movies = table.findAll('tr')[1:]
    movies_dict = {}
    # Loops through all movies for the current year
    for movie in movies:
        movie_info = movie.findAll('td')
        year_rank = movie_info[0].getText()
        individual_url = movie_info[1].find('a')['href']
        individual_url = individual_url[:individual_url.rfind('/')]
        individual_url = individual_url[individual_url.rfind('/')+1:]
        # Sets the box office rank (unique ID) of the movie as the dictionary key
        sanitized_info = sanitizeNumbers(movie_info[2:])
        movies_dict[year_rank] = {
            'movieName' : movie_info[1].getText(),
            'worldwideTotal' : sanitized_info[0],
            'domesticTotal' : sanitized_info[1],
            'domesticPercent' : sanitized_info[2],
            'foreignTotal' : sanitized_info[3],
            'foreignPercent' : sanitized_info[4],
            'individualURL' : individual_url
        }
    return movies_dict

def getMoviesByYear(mapped_response):
    movies_by_year = {}
    # Loops through all years returned and if there is a valid response it parses the HTML and adds it to the movies_by_year dict
    for response in tqdm(mapped_response, 'Box Office Mojo by Year'):
        if response is not None and response.status_code == 200:
            movies_by_year[response.url[-5:-1]] = parseBoxOfficeYear(response.content)
    return movies_by_year

def main():
    init()
    print('\nGetting All Year Box Office Results...')
    all_movies = getAllYears()
    movies_by_year = getMoviesByYear(all_movies)
    # Writes movies dict to JSON file, making it easy to load in another script to grab individual movie details on releases.
    with open(os.path.join(data_path, 'box_office_movies.json'), 'w') as outfile:
        json.dump(movies_by_year, outfile, sort_keys=True, indent=4)
    print('\nAll Box Office Resutls Retrieved.')

if __name__ == '__main__':
    main()