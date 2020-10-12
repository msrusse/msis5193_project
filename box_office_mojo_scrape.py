#! python

from bs4 import BeautifulSoup as BS
import grequests
import json, requests, datetime, csv
from get_html import getHTML
from progressbar import ProgressBar as pb

base_url = 'https://www.boxofficemojo.com/'

def getAllYears():
    grequest = (grequests.get(base_url + 'year/world/%s' % year) for year in range(1977, int(datetime.datetime.now().year)+1))
    return grequests.map(grequest)

def parseBoxOfficeYear(year_page):
    response_bs = BS(year_page, 'lxml')
    table_div = response_bs.find('div', {'class': 'imdb-scroll-table-inner'})
    table = table_div.find('table')
    movies = table.findAll('tr')[1:]
    movies_dict = {}
    for movie in movies:
        movie_info = movie.findAll('td')
        year_rank = movie_info[0].getText()
        movies_dict[year_rank] = {
            'name' : movie_info[1].getText(),
            'worldwide' : movie_info[2].getText(),
            'domestic' : movie_info[3].getText(),
            'domestic_perc' : movie_info[4].getText(),
            'foreign' : movie_info[5].getText(),
            'foreign_perc' : movie_info[6].getText(),
            'individual_url' : movie_info[1].find('a')['href']
        }
    return movies_dict

def getMoviesByYear(mapped_response):
    bar = pb()
    movies_by_year = {}
    for response in bar(mapped_response):
            if response is not None and response.status_code == 200:
                movies_by_year[response.url[-5:-1]] = parseBoxOfficeYear(response.content)
    return movies_by_year

def writeBoxOfficeToCSV(movies):
    with open('box_office_movies.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['unique_id', 'movie_name', 'year_rank', 'year', 'worldwide', 'domestic', 'domestic_perc', 'foreign', 'foreign_perc'])
        for year in movies:
            for movie_rank in movies[year]:
                unique_id = '%s_%s' % (year, movie_rank)
                movie = movies[year][movie_rank]
                writer.writerow([unique_id, movie['name'], movie_rank, year, movie['worldwide'], movie['domestic'], movie['domestic_perc'], movie['foreign'], movie['foreign_perc']])

def main():
    movies = getMoviesByYear(getAllYears())
    writeBoxOfficeToCSV(movies)
    with open('box_office_movies.json', 'w') as outfile:
        json.dump(movies, outfile, sort_keys=True, indent=4)

if __name__ == '__main__':
    main()