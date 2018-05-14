import requests
import sys
from bs4 import BeautifulSoup
from operator import itemgetter
from tabulate import tabulate
import config
from difflib import SequenceMatcher

def get_html(URL):
	r = requests.get(URL)
	return r.text.encode('utf-8')

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def parse_html(html):
	soup = BeautifulSoup(html, 'html.parser')
	now_showing = soup.find("section", {"class":"now-showing"})
	titles = now_showing.find_all("a", {"class":"__movie-name"})

	movie_list = []

	for movie in titles:
		movie_list.append([str(movie.text), "https://in.bookmyshow.com"+str(movie["href"])])

	return movie_list

def print_result(result):
	print result[0]+" is already out, click on the URL below to start booking"
	print result[1]

def check_available(movie_list, movie):
	max_val = 0
	for i in movie_list:
		sim = similar(movie,i[0])
		if sim == 1:
			max_val = 1
			result = i
			break
		elif sim > max_val:
			max_val = sim
			result = i
	if max_val == 1:
		print_result(result)
	elif max_val > 0.7:
		print "Did you mean " + result[0] + "?"
		print_result(result)
	elif max_val > 0.4:
		print "Sorry " + movie + " is not out yet."
		print "Showing closest match with similarity ", max_val
		print_result(result)
	else:
		print "Sorry " + movie + " is not out yet."
		print "To see all running movies do: python bookmyshow.py"

def get_match(url, movie):
	html = get_html(url)
	movie_list = parse_html(html)
	if movie:
		check_available(movie_list, movie)
	else:
		print_all(movie_list)

def print_all(movie_list):
	print tabulate(movie_list, headers=['Name', 'URL'])


def main():
	url = "https://in.bookmyshow.com/hyderabad/movies"

	if len(sys.argv) > 1:
		movie = str(sys.argv[1])
	else:
		print "To search for a specific movie do:"
		print "usage: python bookmyshow.py <movie_name>"
		print "############################################"
		print "Showing All Movies Out Now"
		movie = None


	get_match(url, movie)

if __name__ == '__main__':
	main()