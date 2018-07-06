import requests
import sys
from bs4 import BeautifulSoup
import json
from ebooklib import epub


def setup(URL):
	session = requests.session()
	r = session.get(URL)
	return session

def get_html(session, URL):
	r = session.get(URL)
	return r.text.encode('utf-8')

def parse_html(html):
	soup = BeautifulSoup(html, 'html.parser')
	strong = soup.find_all("strong")
	chap = {}
	chap["name"] = strong[1].text.encode('ascii', 'ignore')
	chap["content"] = ""
	con = soup.find("div", {"class":"entry-content"})
	p = con.find_all("p")
	for i in range(2, len(p)-1):
		chap["content"] += "<p>" + p[i].text.encode('ascii', 'ignore') + "</p>\n"
	return chap

def create_book(name, session):
	URL = 'http://volarenovels.com/transmigrator-meets-reincarnator/tmr-chapter-'
	book = epub.EpubBook()

	# set metadata
	book.set_identifier("123456")
	book.set_title(name)
	book.set_language('en')

	chap_list = []
	for chapter in range(1,361):
		html = get_html(session, URL+str(chapter))
		chap = parse_html(html)
		# create chapter
		c = epub.EpubHtml(title=chap["name"], file_name='chap_'+str(chapter)+'.xhtml', lang='en')
		c.content = "<h1>" + chap["name"] + "</h1>\n" + chap["content"]
		# add chapter
		book.add_item(c)
		chap_list.append(c)

	# define Table Of Contents
	book.toc = tuple(chap_list)

	# add default NCX and Nav file
	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())

	# basic spine
	book.spine = ['nav']
	book.spine.extend(chap_list)

	# write to the file
	epub.write_epub('ebooks/' + name +'.epub', book, {})

def get_book(session):
	# name, chapters = get_chapters(session, URL, bookid)
	create_book("Tranmigrator Meets Reincarnator", session)

def main():
	URL = 'http://volarenovels.com'

	# if len(sys.argv) > 1:
	# 	bookid = int(sys.argv[1])
	# else:
	# 	print "Usage: python webnovel.py <bookid>"

	session = setup(URL)

	get_book(session)


if __name__ == '__main__':
	main()
