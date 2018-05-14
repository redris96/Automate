import requests
import sys
from bs4 import BeautifulSoup
from operator import itemgetter
from tabulate import tabulate
import config

def login():
	session = requests.session()

	URL = 'https://forum.snahp.it/ucp.php?mode=login'

	username = config.username
	password = config.password

	login_data = {
		'username'	:	username,
		'password'	:	password,
		'login'	:	'Login',
		'redirect'	:	'./index.php'	
	}

	r = session.post(URL, data=login_data)

	return session

def get_html(session, URL):
	r = session.get(URL)
	return r.text.encode('utf-8')

def parse_html(file):
	with open(file, 'r') as myfile:
		html=myfile.read()
	soup = BeautifulSoup(html, 'html.parser')
	a = soup.find_all("div", {"class":"forumbg"})
	text = a[1]

	content = []

	for i in text.find_all("a", {"class":"topictitle"}):
		content.append([i.text, 'https://forum.snahp.it'+i['href'][1:]])

	for i,j in enumerate(text.find_all("dd", {"class":"views"})):
		if i == 0:
			continue
		content[i-1].insert(1, int(j.text.split()[0]))

	content = sorted(content, key = itemgetter(1), reverse=True)

	return content

def print_top(session, url, file_name, top):
	html = get_html(session, url)

	file = open(file_name, "w")
	file.write(html)
	file.close()

	content = parse_html(file_name)
	print tabulate(content[:top], headers=['Name', 'Views', 'URL'])

def main():
	movies_url = 'https://forum.snahp.it/viewforum.php?f=26'
	tv_url = 'https://forum.snahp.it/viewforum.php?f=31'

	if len(sys.argv) > 1:
		top = int(sys.argv[1])
	else:
		top = 5

	session = login()

	print "Movies"
	print_top(session, movies_url, "movies.html", top)

	print "\n###################################################\n"

	print "Tv Shows"
	print_top(session, tv_url, "tv.html", top)


if __name__ == '__main__':
	main()