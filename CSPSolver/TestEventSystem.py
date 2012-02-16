'''
Created on Feb 16, 2012

@author: Shenra
'''
import unittest
from EventSystem import AsnDmcEventSystem
from collections import deque, Counter

class Test(unittest.TestCase):
	"""
	Currently tests only the AsnDmcEventSystem
	
	Tests only functionality. Need to test for exceptions, bad inputs, funny
	cases.
	"""
	def setUp(self):
		self.pq = deque()
		self.es = AsnDmcEventSystem(self.pq)

	def testAmcDmcInit(self):
		self.assertEquals(self.es._asn, [])
		self.assertEquals(self.es._asndmc, [])
		self.assertIs(self.es._pq, self.pq)
		
	def testAmcDmcSubscribe(self):
		self.es.subscribe('p1', 1)
		self.assertIn('p1', self.es._asndmc)
		self.es.subscribe('p0', 0)
		self.assertIn('p0', self.es._asn)
		self.es.subscribe('p2',1)
		self.es.subscribe('p2',0)
		self.assertIn('p2', self.es._asn)
		self.assertIn('p2', self.es._asndmc)

	def testAmcDmcCancel(self):
		self.es.subscribe('p1', 1)
		self.es.subscribe('p1', 0)
		self.es.cancel('p1', 1)
		self.assertNotIn('p1', self.es._asndmc)
		self.assertIn('p1', self.es._asn)
		self.es.cancel('p1', 0)
		self.assertNotIn('p1', self.es._asn)
		
	def testAmcDmcSchedule(self):
		self.es.subscribe('p1', 1)
		self.es.subscribe('p2', 1)
		self.es.subscribe('p0', 0)
		self.es.schedule(1)
		self.assertTrue(len(self.pq) == 3)
		self.assertIn('p1', self.pq)
		self.assertIn('p2', self.pq)
		self.assertIn('p0', self.pq)
		
		self.es.schedule(0)
		
		c = Counter(self.pq)
		self.assertTrue(len(self.pq) == 5)
		self.assertTrue(c['p1'] == 2)
		self.assertTrue(c['p2'] == 2)
		self.assertIn('p0', self.pq)
		
		

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()