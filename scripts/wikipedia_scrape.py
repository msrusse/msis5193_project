#! python

from bs4 import BeautifulSoup as BS
import grequests
import json, requests, sys, os
from datetime import datetime

# Sets base URL for wikipedia
wikipedia_url = 'https://en.wikipedia.org'
# Creates errors dictionary
errors = {}
# Sets the log file location
log = open("logs/wikipedia_scrape.log", "a")
# Sets the standard output to console
primary_stdout = sys.stdout

# Sanitizes scraped columns for awards and nominations to convert them to ints
def sanitizeCols(cols):
    sanitized = []
    # Go through each item in the list passed 
    for col in cols:
        # Get the first number in each column, if it has a special note and replace any special characters
        text = col.getText().split(' ')[0].split('[')[0].split('/')[0].replace(u'\u2013', u'-').replace('\n', '').replace(',', '').replace(' ', '')
        # Append sanitized text to the list to return as an int
        sanitized.append(int(text))
    return sanitized

# Get information for the Academy Award Winning movies
def determineMovies(response):
    # Convert the response to a soup object
    html = BS(response.content, 'lxml')
    # Find the table on the page
    movies_table = html.find('table', {'class': 'wikitable sortable'})
    # Get the body from the table
    movies_table_body = movies_table.find('tbody')
    # Get all rows from the table, each row corresponds to an award winning movie
    movie_rows = movies_table_body.find_all('tr')
    # Creates the movies dictionary
    movies = {}
    # Creates variables to work with the logic for row and column spans of the awards and nominations
    total_award_rows = total_nominations_rows = nominations_row = award_row = 0
    current_year = current_awards = current_nominations = None
    wiki_link = ''
    # Creates the progressbar object
    # Loops through each movie, starts with index 1 because index 0 is the header row
    for movie in movie_rows[1:]:
        # Finds all table data in the row, each item corresponds to the title, year, awards, and nominations
        cols = movie.find_all('td')
        # Gets the title and sanitizes it
        title = cols[0].getText().replace('\n', '')
        # Gets the a tag from each row, this has the link to the movies wikipedia page
        a_ref = cols[0].find('a')
        # Determines if an a tag exists in the row
        if a_ref:
            # Grabs the href if the a tag exists
            wiki_link = a_ref['href']
        # Determines if the row has a style attribute, only best picture movies have a style
        if movie.has_attr('style'):
            # Creates and sets best picture to True when style is present
            best_picture = True
        else:
            # Creates best picture set to False when style not present
            best_picture = False
        # If there are more than one column, do logic to get the year, awards, and nominations. Title is always the first column and sometimes will be the only
        if len(cols) > 1:
            # Sanitizes all numeric columns
            sanitized_cols = sanitizeCols(cols[1:])
            # Determines if the sanitized columns contains the year, award, and nominations
            if len(sanitized_cols) == 3:
                # Determines if the awards spans additional rows
                if cols[2].has_attr('rowspan'):
                    # Sets the value of total_award_rows to the amount of rows the awards span
                    total_award_rows = int(cols[2]['rowspan'])
                    # Sets the value of award_row to one, noting this is the first row of the span
                    award_row = 1
                # Determines if the nominations spans additional rows
                if cols[3].has_attr('rowspan'):
                    # Sets the value of total_nominations_rows to the amount of rows the nominations span
                    total_nominations_rows = int(cols[3]['rowspan'])
                    # Sets the value of nominations_row to one, noting this is the first row fo the nominations
                    nominations_row = 1
                # Sets the current year value to the year in the row
                current_year = sanitized_cols[0]
                # Sets the current awards to the number in the current row
                current_awards = sanitized_cols[1]
                # Sets the current nominations to the number in the current row
                current_nominations = sanitized_cols[2]
            # Determines if the sanitized columns have awards and nominations. If there are only two values in the sanitized, it will always be awards and nominations
            elif len(sanitized_cols) == 2:
                # Determines if awards spans multiple rows
                if cols[1].has_attr('rowspan'):
                    # Sets total award rows to the value of the rowspan
                    total_award_rows = int(cols[1]['rowspan'])
                    # Resets award row to 1, denoting this is the first row of the span
                    award_row = 1
                else:
                    # If there is no rowspan, then increment which row we are on
                    award_row += 1
                # Determines if nominations spans multiple rows
                if cols[2].has_attr('rowspan'):
                    # Sets the total nominations to the row span
                    total_nominations_rows = int(cols[2]['rowspan'])
                    # Resets current nominations row to 1
                    nominations_row = 1
                else: 
                    # Increments what nomination row we are on
                    nominations_row += 1
                current_awards = sanitized_cols[0]
                current_nominations = sanitized_cols[1]
            else:
                # Sets row and col spans to 0
                row_span = col_span = 0
                # awards and noms is used if the number spreds across both columns and rows
                awards_and_noms = False
                # Determines if the value spans rows
                if cols[1].has_attr('rowspan'):
                    # Sets the row_span to the total number of rows spanned
                    row_span = int(cols[1]['rowspan'])
                # Determines if the value spans columns
                if cols[1].has_attr('colspan'):
                    # Sets the col_span to how many columns the number spans
                    col_span = int(cols[1]['colspan'])
                    # Sets the value to denote that the number is in both rows and columns
                    awards_and_noms = True
                if awards_and_noms:
                    # Set the current award and nominations value to the rows number
                    current_awards = current_nominations = sanitized_cols[0]
                    # Sets the nominations and rows spans to the amount it spans
                    total_nominations_rows = total_award_rows = col_span
                    # Resets the nominations and award rows to one
                    nominations_row = award_row = 1
                # Determines if the current award row is less than the total rows it spans
                elif award_row < total_award_rows:
                    # Increments the what the current award_row is
                    award_row += 1
                    # Sets the total nominations to the row_span value, because it is the field that changed
                    total_nominations_rows = row_span
                    # Resets nominations row to the first row
                    nominations_row = 1
                    # Changes the current_nominations to the amount spanning rows
                    current_nominations = sanitized_cols[0]
                else:
                    # Increments the nominations row
                    nominations_row += 1
                    # Sets the amount of rows the value spans
                    total_award_rows = row_span
                    # Resets the awards row count
                    award_row = 1
                    # Sets the new value of awards
                    current_awards = sanitized_cols[0]
        else:
            # Increment award and nominations rows, because neither changed
            award_row += 1
            nominations_row += 1
        # Creates the key for the movie as the unique URL for the fild
        movie_key = wikipedia_url + wiki_link
        # Adds the current movie to the movies dict
        movies[movie_key] = {
            'movieName' : title, 
            'wikiLink' : movie_key,
            'year' : current_year,
            'awards' : current_awards,
            'nominations' : current_nominations,
            'bestPicture' : best_picture
            }
    return movies

def getMoviesOnWikipedia(movies):
    # Async request for all the movies, based off the key, which is their URL
    response = (grequests.get(movie) for movie in movies)
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
        sys.stdout = log
        print('%s' % response)
        sys.stdout = primary_stdout

def parseWikipediaPages(response):
    # Converts response to soup object
    response_bs = BS(response.text, features='lxml')
    # Finds all hrefs
    hrefs = response_bs.find_all('a', href=True)
    # Sets the value for the rotten tomatoes link
    rotten_tomatoes_links = 'N/A'
    # Loops through each href on the page
    for url in hrefs:
        # Determines if rottentomatoes has an href link
        if 'rottentomatoes.com' in url.get('href') and 'web.archive.org' not in url.get('href'):
            # Changes the rotten tomatoes link to the variable
            rotten_tomatoes_links = url.get('href')
    return rotten_tomatoes_links

def determineIfValidRepsonse(response):
    # Determines if a valid response code
    if response.status_code == 200:
        return True
    # If the repsonse is a server error
    elif response.status_code == 503:
        # Retries the request
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
        print('\nWikipedia returned a valid response. Parsing movies...')
        movies = determineMovies(all_award_winners_wiki)
        print('\nMovies parsed. Requesting Individual movie pages...')
        individual_movie_wikis = getMoviesOnWikipedia(movies)
        print('\nIndividual movie pages retrieved. Parsing each page...')
        for response in individual_movie_wikis:
            if checkStatusCode(response):
                movies[response.url]['rottenTomatoes'] = parseWikipediaPages(response)
            else:
                sys.stdout = log
                print('Unable to retrieve %s' % response)
                sys.stdout = primary_stdout
        print('\nIndividual movie pages parsed. Saving results to data/movies_from_wikipedia.json...')
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