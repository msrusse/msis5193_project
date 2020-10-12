#! python

from bs4 import BeautifulSoup as BS

def getHTML(page):
    html = BS(page.text, features='lxml')        
    return {
        'html': html,
        'status': page.status_code
    }