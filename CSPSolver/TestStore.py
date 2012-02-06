'''
Created on Feb 4, 2012

@author: Shenra
'''
import unittest
from Store import Store
from VariableDomain import VariableDomain

class Test(unittest.TestCase):
	def setUp(self):
		self.store = Store()

	def test_init(self):
		Store(a=VariableDomain(0,0))
		self.assertRaises(TypeError, Store.__init__, self.store, a=1)
		
	def test_getitem(self):
		k = VariableDomain(0,0)
		s = Store(a=k)
		self.assertIs(s['a'], k)
		
	def test_setitem(self):
		pass
		
		
		
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testInit']
	unittest.main()