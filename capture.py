__authon__ = "Aman Nagpal"
__email__ = "amannagpal4@gmail.com"

import csv
import webbrowser
from bs4 import BeautifulSoup
import requests

# countrys whose best netflix movies you want to get
COUNTRY = 'tag-india-netflix'
count = 1

def main(url = 'https://agoodmovietowatch.com/netflix/'):
    soup = get_website(url)
    get_params(soup)


def get_website(url):
    code = requests.get(url)
    soup = BeautifulSoup(code.text, 'html.parser')
    return soup

def get_params(soup):
    movie_data = [] # a list that contains movie names and descriptions and star rating
    # figure out how to get name and rating of a movie - from the same page
    data = soup.find_all('article', {'class': COUNTRY})
    for article in data:
        link = article.find('a')
        # finds the single movie link
        movie_soup = get_website(link.get('href'))
        # goes to the link of a single movie
        movie_data.append({'name': movie_soup.find('span', {'class': 'moviename'}).get_text(), 'description': movie_soup.find('span', {'itemprop': 'reviewBody'}).get_text(), 'genre': movie_soup.find('span', {'itemprop': 'genre'}).get_text()})
    save_data(movie_data)

def save_data(movie_data):
    global count
    fw = open('movies.csv', 'a')
    writer = csv.writer(fw)
    if count == 1:
        writer.writerow(("NAME", "DESCRIPTION", "GENRE"))
    for movie in movie_data:
        writer.writerow((movie['name'], movie['description'], movie['genre']))
    count = count + 1
    if count <= 5:
        main('https://agoodmovietowatch.com/netflix/page/' + str(count))
    else:
        # play the alarm specified video when the task in completed
       alarm()

def alarm():
    videos = ""
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(videos)
    exit(0)

if __name__ == "__main__":
    main()