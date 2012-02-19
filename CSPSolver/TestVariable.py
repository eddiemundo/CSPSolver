'''
Created on Feb 16, 2012

@author: Shenra
'''
import unittest
from Variable import Variable

class Test(unittest.TestCase):
	"""Currently tests Variable only with the AsnDmcEventSystem"""
	def setUp(self):
		self.v = Variable('v1', range(21))
		
	def testInit(self):
		self.assertEquals(self.v.name, 'v1')
		self.assertEquals(self.v.domain, set(range(21)))
		self.assertFalse(self.v.assigned)
		
	def testCopy(self):
		v1_copy = self.v.copy()
		self.assertEquals(v1_copy.name, self.v.name)
		self.assertEquals(v1_copy.domain, self.v.domain)
		self.assertFalse(v1_copy.assigned)
		
	def testPruneFromDomain(self):
		self.v.pruneFromDomain(range(2,21))
		self.assertEquals(self.v.domain, set([0,1]))
		self.assertFalse(self.v.assigned)
		self.v.pruneFromDomain([0])
		self.assertEquals(self.v.domain, set([1]))
		self.assertTrue(self.v.assigned)
	
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()