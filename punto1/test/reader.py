import requests
import unittest
def getHTMLNewspaper(name, url):	
	r = requests.get(url)
	print("Creating temporaly file...")
	filepath="results/"+name+".html"
	f = open(filepath,"w",encoding="utf16")
	print("Saving file from "+name)
	f.write(r.text)
	f.close()
	#s3.meta.client.upload_file(data['file'],data['bucket'] , data['path'])
	return True
class TestReader(unittest.TestCase):

	def test_publimetro(self):
			self.assertEqual(getHTMLNewspaper("Publimetro","https://www.publimetro.co/"), True)
	def test_elTiempo(self):
			self.assertEqual(getHTMLNewspaper("El_tiempo","https://www.eltiempo.com/"), True)

if __name__ == '__main__':
		unittest.main()