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
	content = soup.find("div", {"class":"cha-words"})
	return unicode(str(content), "utf-8")

def get_chapters(session, URL, bookid):
	data = {
		'_csrfToken': session.cookies['_csrfToken'],
		'bookId': bookid,
	}
	response = session.get(URL, params=data)
	data = json.loads(response.text)
	data = data["data"]
	name = data["bookInfo"]["bookName"].encode("utf-8")
	chapters = []
	for item in data["volumeItems"]:
		chapters.extend(item["chapterItems"])
	return name, chapters

def create_book(name, chapters, bookid, session):
	URL = "https://www.webnovel.com/book/" + str(bookid) + "/"
	book = epub.EpubBook()

	# set metadata
	book.set_identifier(str(bookid))
	book.set_title(name)
	book.set_language('en')

	chap_list = []
	for chap in chapters:
		if chap["isVip"] != 0:
			break;
		# create chapter
		c = epub.EpubHtml(title=chap["name"], file_name='chap_'+str(chap["index"])+'.xhtml', lang='en')
		html = get_html(session, URL+chap["id"])
		c.content = u"<h1>" + chap["name"] + u"</h1>" + parse_html(html)
		# c.content = parse_html(html)
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

def get_book(session, bookid):
	URL = 'https://www.webnovel.com/apiajax/chapter/GetChapterList'
	name, chapters = get_chapters(session, URL, bookid)
	create_book(name, chapters, bookid, session)

def main():
	URL = 'https://www.webnovel.com/'

	if len(sys.argv) > 1:
		bookid = int(sys.argv[1])
	else:
		print "Usage: python webnovel.py <bookid>"

	session = setup(URL)

	get_book(session, bookid)


if __name__ == '__main__':
	main()