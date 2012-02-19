'''
Created on Feb 17, 2012

@author: Shenra
'''
from collections import deque

class EmptySpace(object):
	__slots__ = ('propagator_queue', 'variable_store')

class Space(object):
	__slots__ = ('propagator_queue', 'variable_store')
	
	def __init__(self, variables):
		self.variable_store = dict(zip([v.name for v in variables], variables))
		
	def copy(self):
		self_copy = EmptySpace()
		self_copy.__class__ = self.__class__
		self_copy.variable_store = {}
		for vn, v in self.variable_store.items():
			if v.assigned:
				self_copy.variable_store[vn] = v
			else:
				self_copy.variable_store[vn] = v.copy()
		return self_copy
		
	def assigned(self):
		for v in self.variable_store.values():
			if not v.assigned:
				return False
		return True