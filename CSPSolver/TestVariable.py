'''
Created on Feb 16, 2012

@author: Shenra
'''
import unittest
from Variable import Variable
from EventSystem import AsnDmcEventSystem
from collections import deque, Counter

class Test(unittest.TestCase):
	"""Currently tests Variable only with the AsnDmcEventSystem"""
	def setUp(self):
		self.pq = deque()
		self.es = AsnDmcEventSystem(self.pq)
		self.es.subscribe('p0', 0)
		self.es.subscribe('p1', 1)
		self.v = Variable([0,1,2,3], self.es)
		
	def testVariableInit(self):
		self.assertEquals(self.v._domain, set([0,1,2,3]))
		self.assertFalse(self.v.assigned)
		self.assertIs(self.v._eventSystem, self.es)
		
	def testRemoveFromDomain(self):
		self.v.removeFromDomain([0,1,3])
		
		self.assertEquals(self.v._domain, set([2]))
		self.assertTrue(self.v.assigned)
		
		self.assertTrue(len(self.pq) == 2)
		self.assertIn('p1', self.pq)
		self.assertIn('p0', self.pq)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()