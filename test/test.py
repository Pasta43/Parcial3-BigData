import csv
from bs4 import BeautifulSoup
import unittest

def srappingElTiempo():
	f = open('results/El_tiempo.html',"r",encoding='utf-8')
	txt=f.read()
	
	soup = BeautifulSoup(txt,'html.parser')
	articles=soup.find_all('article') #All of these articles, are news

	csvFile = open('results/results.csv', 'w',encoding='utf-8')
	writer = csv.writer(csvFile,dialect='unix')
	row=['title','section','url']
	writer.writerow(row)
	for article in articles:
		category_anchor=article.find("a",{'class':'category'})
		title_anchor= article.find("a",{'class':'title'})
		if(category_anchor and title_anchor):
			category=category_anchor.getText()
			title=title_anchor.getText()
			url='https://www.eltiempo.com'+title_anchor.get('href')
			row=[title,category,url]
			writer.writerow(row)

	csvFile.close()
	f.close()
	return True
def srappingPublimetro():
	f = open('results/Publimetro.html',"r",encoding='utf-16')
	txt=f.read()
	csvFile = open('results/resultsPublimetro.csv', 'w',encoding='utf-16')
	writer = csv.writer(csvFile,dialect='unix')
	row=['title','section','url']
	writer.writerow(row)
	soup = BeautifulSoup(txt,'html.parser')
	mainDiv=soup.find(id='main')
	divNews=mainDiv.find_all('div',{'class':'container layout-section'})
	usefulDivNews=divNews[1]
	for row in usefulDivNews:
		headers=row.find_all('h4')
		if(len(headers)!=0):  
			for header in headers:
				section = header.text
				nextElement=header.nextSibling
				if nextElement:
					if(header.parent.name=='main'):
						items = nextElement.find_all('div',{'class':'list-item'})
						for news in items:
							anchor=news.find_all('a')[0]
							url = "https://www.publimetro.co"+anchor.get('href')
							title= anchor.get('title')
							row=[title,section,url]
							writer.writerow(row)
					else:
						articles=nextElement.find('article')
						
						if articles:
							for article in articles:
								
								anchors = article.find_all('a')
								if anchors:
									for anchor in anchors:
										if anchor.find('img'):
											pass
										else:
											url = "https://www.publimetro.co"+anchor.get('href')
											title = anchor.getText()
											row=[title,section,url]
											writer.writerow(row)
	f.close()
	csvFile.close()
	return True
class TestScrapperElTiempo(unittest.TestCase):

	# def test_elTiempo(self):
	# 		self.assertEqual(srappingElTiempo(), True)
	def test_publimetro(self):
			self.assertEqual(srappingPublimetro(), True)


if __name__ == '__main__':
		unittest.main()