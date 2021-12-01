import unittest
def testReading():
    f = open("SPY_TICK_TRADE.csv",encoding='utf-8')
    i=0
    for line in f:
        print(line.split(',')[1])
        i+=1
        if i ==100:
            break
    f.close()
    return True
class Test(unittest.TestCase):

	def test_publimetro(self):
			self.assertEqual(testReading(), True)


if __name__ == '__main__':
		unittest.main()
    