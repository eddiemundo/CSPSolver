'''
Created on Feb 10, 2012

@author: Shenra
'''
import unittest
from collections import deque
from Variable import Variable

class Test(unittest.TestCase):


	def test__init__(self):
		pq = deque()
		vd = Variable(0,1, pq)
		# test assignments
		self.assertEquals(vd.lb, 0)
		self.assertEquals(vd.ub, 1)
		self.assertEquals(vd.failed, False)
		self.assertEquals(vd.assigned, False)
		self.assertEquals(vd._propagatorQueue, pq)
		self.assertEquals(vd._idx, [0, 0, 0, 0, 0, 0])
		self.assertEquals(vd._deps, [])
		
		# test branches
		vd = Variable(0, 0, pq)
		self.assertEquals(vd.assigned, True)
		self.assertEquals(vd.failed, False)
		
		vd = Variable(1, 0, pq)
		self.assertEquals(vd.failed, True)
		self.assertEquals(vd.assigned, False)
		
	def testSuscribe(self):
		pq = deque()
		vd = Variable(0, 0, pq)
		vd.subscribe('p1', 4)
		self.assertEquals(vd._idx[4], 0)
		self.assertEquals(vd._deps[vd._idx[4]], 'p1')
		vd.subscribe('p2', 0)
		self.assertEquals(vd._idx[4], 1)
		self.assertEquals(vd._idx[0], 0)
		self.assertEquals(vd._deps[vd._idx[4]], 'p1')
		self.assertEquals(vd._deps[vd._idx[0]], 'p2')
		vd.subscribe('p3', 0)
		self.assertEquals(vd._idx[4], 2)
		self.assertEquals(vd._idx[0], 0)
		self.assertEquals(vd._deps[vd._idx[4]], 'p1')
		self.assertEquals(vd._deps[vd._idx[0]], 'p3')
		self.assertEquals(vd._deps[vd._idx[0] + 1], 'p2')
		
	def testCancel(self):
		pq = deque()
		vd = Variable(0, 0, pq)
		vd.subscribe('p1', 4)
		vd.subscribe('p2', 0)
		vd.subscribe('p3', 0)
		self.assertEquals(vd._deps[vd._idx[0]], 'p3')
		self.assertEquals(vd._deps[vd._idx[0]+1], 'p2')
		vd.cancel('p2', 0)
		self.assertEquals(not 'p2' in vd._deps, True)
		self.assertEquals(vd._idx[4], 1)
		vd.cancel('p1', 4)
		self.assertEquals(not 'p1' in vd._deps, True)
		self.assertEquals(vd._deps[vd._idx[0]], 'p3')
		self.assertRaises(ValueError, vd.cancel, 'p2', 0)
		
	def testSchedule(self):
		pq = deque()
		vd = Variable(0, 0, pq)
		vd.subscribe('p1', 4)
		vd.subscribe('p2', 0)
		vd.subscribe('p3', 0)
		vd.schedule(0, 4)
		self.assertEquals(pq.popleft(), 'p3')
		self.assertEquals(pq.popleft(), 'p2')
		self.assertEquals(pq.popleft(), 'p1')
		
	def testSetters(self):
		pq = deque()
		vd = Variable(0, 0, pq)
		vd.subscribe('p1', 4)
		vd.setlb(0)
		self.assertFalse(pq)
		vd.setub(-1)
		self.assertTrue(vd.failed)
		self.assertFalse(pq)
		vd = Variable(0, 10, pq)
		vd.subscribe('asn', 0)
		vd.subscribe('lbc', 1)
		vd.subscribe('ubc', 2)
		
		vd.setlb(1)
		self.assertTrue(vd.lb == 1)
		self.assertTrue('lbc' in pq)
		vd.setub(5)
		self.assertTrue('ubc' in pq)
		vd.setlb(5)
		self.assertTrue('asn' in pq)
		self.assertTrue(vd.assigned)
		

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()