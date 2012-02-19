'''
Created on Feb 19, 2012

@author: Shenra
'''
import unittest
from Variable import Variable
from Space import Space

class Test(unittest.TestCase):
	def setUp(self):
		variables = [
					Variable('v1', range(1)),
					Variable('v2', range(1)),
					Variable('v3', range(1)),
					Variable('v4', range(1)),
					]
		self.s = Space(variables)

	def testInit(self):
		self.assertEquals(self.s.variable_store['v1'].name, 'v1')
		self.assertEquals(self.s.variable_store['v2'].name, 'v2')
		self.assertEquals(self.s.variable_store['v3'].name, 'v3')
		self.assertEquals(self.s.variable_store['v4'].name, 'v4')
		
	def testCopy(self):
		s_copy = self.s.copy()
		self.assertEquals(s_copy.variable_store['v1'].name, 'v1')
		self.assertEquals(s_copy.variable_store['v2'].name, 'v2')
		self.assertEquals(s_copy.variable_store['v3'].name, 'v3')
		self.assertEquals(s_copy.variable_store['v4'].name, 'v4')
		
	def testAssigned(self):
		self.assertTrue(self.s.assigned())

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()