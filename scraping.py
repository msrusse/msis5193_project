#! /usr/bin/python3

from urllib.request import urlopen
import re

class Movie:
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def getHTML(self):
        print('Retrieving %s HTML...\n' % self.name)
        page = urlopen(test_movie.url)
        print('HTML received.\n')
        return page

    def decodeHTML(self, page):
        print('Reading %s HTML...\n' % self.name)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        print('HTML decoded.\n')
        return html

    def sanitizeHTML(self, html):
        print('Sanitizing %s HTML...\n' % self.name)
        html = html.replace(' ', '')
        html = html.replace('\n', '')
        #html = html.replace('\\', '')
        print('HTML sanitized.\n')
        return html

    def findIndexes(self, html):
        print('Determining rating indexes for %s...\n' % self.name)
        search_term = '<spanclass="mop-ratings-wrap__percentage">'
        indexes = [m.start() for m in re.finditer(search_term, html)]
        if len(indexes) != 2:
            # TODO: add logic to determine whether it is a user or critic ranking left off. Can search for href="#audience_reviews"
            pass 
        print('Indexes Determined.\n')
        return (indexes[0]+len(search_term), indexes[1] + len(search_term))

    def getScores(self, html, indexes):
        print('Getting scores for %s...\n' % self.name)
        critics_score = html[indexes[0]:indexes[0]+2]
        audience_score = html[indexes[1]:indexes[1]+2]
        print('Scores retrieved.\n')
        return {
            'critics' : critics_score,
            'audience' : audience_score
        }

test_movie = Movie(url='https://www.rottentomatoes.com/m/learning_to_skateboard_in_a_warzone', name='Star Trek Beyond')
page = test_movie.getHTML()
html = test_movie.decodeHTML(page)
html = test_movie.sanitizeHTML(html)
indexes = test_movie.findIndexes(html)
scores = test_movie.getScores(html, indexes)
print(scores)