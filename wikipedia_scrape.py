#! python

from bs4 import BeautifulSoup as BS
import grequests
import json, requests, sys
from datetime import datetime
from progressbar import ProgressBar as pb

wikipedia_url = 'https://en.wikipedia.org'
errors = {}
# Sets the log file location
log = open("logs/wikipedia_scrape.log", "a")
# Sets the standard output to console
primary_stdout = sys.stdout

def sanitizeCols(cols):
    sanitized = []
    for col in cols:
        text = col.getText().split(' ')
        text = text[0].split('[')
        text = text[0].split('/')
        text = text[0].replace(u'\u2013', u'-').replace('\n', '').replace(',', '').replace(' ', '')
        sanitized.append(int(text))
    return sanitized

def determineMovies(response):
    html = BS(response.content, 'lxml')
    movies_table = html.find('table', {'class': 'wikitable sortable'})
    movies_table_body = movies_table.find('tbody')
    movie_rows = movies_table_body.find_all('tr')
    movies = {}
    total_award_rows = 0
    total_nominations_rows = 0
    award_row = 0
    nominations_row = 0
    current_year = None
    current_awards = None
    current_nominations = None
    bar = pb()
    for movie in bar(movie_rows[1:]):
        cols = movie.find_all('td')
        title = cols[0].getText().replace('\n', '')
        a_ref = cols[0].find('a')
        if a_ref:
            wiki_link = a_ref['href']
        if movie.has_attr('style'):
            best_picture = True
        else:
            best_picture = False
        if len(cols) > 1:
            sanitized_cols = sanitizeCols(cols[1:])
            if len(sanitized_cols) == 3:
                if cols[2].has_attr('rowspan'):
                    total_award_rows = int(cols[2]['rowspan'])
                    award_row = 0
                if cols[3].has_attr('rowspan'):
                    total_nominations_rows = int(cols[3]['rowspan'])
                    nominations_row = 0
                current_year = sanitized_cols[0]
                current_awards = sanitized_cols[1]
                current_nominations = sanitized_cols[2]
            elif len(sanitized_cols) == 2:
                if cols[1].has_attr('rowspan'):
                    total_award_rows = int(cols[1]['rowspan'])
                    award_row = 1
                else:
                    award_row += 1
                if cols[2].has_attr('rowspan'):
                    total_nominations_rows = int(cols[2]['rowspan'])
                    nominations_row = 1
                else: 
                    nominations_row += 1
                current_awards = sanitized_cols[0]
                current_nominations = sanitized_cols[1]
            else:
                row_span = 0
                col_span = 0
                awards_and_noms = False
                if cols[1].has_attr('rowspan'):
                    row_span = int(cols[1]['rowspan'])
                if cols[1].has_attr('colspan'):
                    col_span = int(cols[1]['colspan'])
                    awards_and_noms = True
                if awards_and_noms:
                    current_awards = sanitized_cols[0]
                    current_nominations = sanitized_cols[0]
                    total_nominations_rows = col_span
                    total_award_rows = col_span
                    nominations_row = 1
                    award_row = 1
                elif award_row < total_award_rows:
                    award_row += 1
                    total_nominations_rows = row_span
                    nominations_row = 1
                    current_nominations = sanitized_cols[0]
                else:
                    nominations_row += 1
                    total_award_rows = row_span
                    award_row = 1
                    current_awards = sanitized_cols[0]
        else:
            award_row += 1
            nominations_row += 1
        movie_key = wikipedia_url + wiki_link
        movies[movie_key] = {
            'title' : title, 
            'wikiLink' : movie_key,
            'year' : current_year,
            'awards' : current_awards,
            'nominations' : current_nominations,
            'bestPicture' : best_picture
            }
    return movies

def getMoviesOnWikipedia(movies):
    response = (grequests.get(movies[movie]['wikiLink']) for movie in movies)
    return grequests.map(response)

def checkStatusCode(response):
    if response:
        # If a valid response, return it
        if response and response.status_code == 200:
            return response
        # If the response is a server error, reattempt the response up to 25 times
        elif response and response.status_code == 503:
            # Makes individual request
            r=requests.get(response.url)
            checkStatusCode(r)
        # If the response has a nonvalid or server error response, add it to the errors file
        else:
            errors[response.url] = {
                'status' : response.status_code,
                'id' : response.url[response.url[:-1].rfind('/')+1:-1]
            }
            return None
    # If response is none, log the response in the log file
    else:
        print('%s' % response)

def parseWikipediaPages(response):
    response_bs = BS(response.text, features='lxml')
    hrefs = response_bs.find_all('a', href=True)
    rotten_tomatoes_links = 'N/A'
    for url in hrefs:
        if 'rottentomatoes.com' in url.get('href') and 'web.archive.org' not in url.get('href'):
            rotten_tomatoes_links = url.get('href')
    return rotten_tomatoes_links

def determineIfValidRepsonse(response):
    if response.status_code == 200:
        return True
    elif response.status_code == 503:
        r = requests.get(wikipedia_url + '/wiki/List_of_Academy_Award-winning_films')
        determineIfValidRepsonse(r)

def main():
    # Sets the current start time for the script
    start_time = datetime.now()
    # Sets the output to the log file
    sys.stdout = log
    #Prints the start time for the script to the log file
    print('\nScript began running at: %s' % start_time)
    sys.stdout = primary_stdout
    all_award_winners_wiki = requests.get(wikipedia_url + '/wiki/List_of_Academy_Award-winning_films')
    print('\nAll Academy Award winners retrieved. Determining response...')
    if determineIfValidRepsonse(all_award_winners_wiki):
        print('Wikipedia returned a valid response. Parsing movies...')
        movies = determineMovies(all_award_winners_wiki)
        print('Movies parsed. Requesting Individual movie pages...')
        individual_movie_wikis = getMoviesOnWikipedia(movies)
        print('\nIndividual movie pages retrieved. Parsing each page...')
        bar = pb()
        for response in bar(individual_movie_wikis):
            if checkStatusCode(response):
                movies[response.url]['rotten_tomatoes'] = parseWikipediaPages(response)
            else:
                sys.stdout = log
                print('Unable to retrieve %s' % response.url)
                syst.stdout = primary_stdout
        print('Individual movie pages parsed. Saving results to data/movies_from_wikipedia.json...')
        with open('data/movies_from_wikipedia.json', 'w') as outfile:
            json.dump(movies, outfile, sort_keys=True, indent=4)
        print('\nFile Saved.')
        sys.stdout = log
        print('File completed at %s in %s' % (datetime.now(), (datetime.now()-start_time)))
    else:
        sys.stdout = log
        print('Unable to retrieve base Wikipedia page.')

if __name__ == '__main__':
    main()
