
'''
convert files from
commonmark, docbook, docx, epub, haddock, html, json, latex, markdown,
markdown_github, markdown_mmd, markdown_phpextra, markdown_strict, mediawiki, native, odt, opml, org, rst, t2t, textile, twiki
modular -
'''

from bs4 import BeautifulSoup
import urllib.request
import pypandoc
import re
import urllib.request
from bs4 import BeautifulSoup
 
 
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True
 
 
def get_answered_questions():
	
	start_url = "https://www.quora.com/profile/Aman-Goel-9"

	raw = urllib.request.urlopen(start_url)
	soup = BeautifulSoup(raw)
	data = soup.findAll(text=True)
	res = filter(visible,data)
	print(list(res))
	#for line in soup.findAll('span',{'class':'rendered_qtext'}):
		#print(line.text)



def main():
	start_url = "https://amangoel.quora.com/Build-a-solid-career-in-tech-without-a-CS-major"
	raw = urllib.request.urlopen(start_url)

	soup = BeautifulSoup(raw)
	soup = soup.find_all(text=True)
	print(soup.prettify())
	
	file = open("temp.html","w")
	for line in soup :
		file.write(str(line))
	out = pypandoc.convert_file("temp.html",'docx',outputfile='Done.docx')
	file.close()

if __name__ == "__main__":
    #main()
    get_answered_questions()
