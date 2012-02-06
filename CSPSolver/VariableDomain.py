'''
Created on Feb 4, 2012

@author: Shenra
'''
class EmptyVariableDomain:
	__slots__ = ('lb', 'ub', 'assigned', 'failed')

class VariableDomain:
	__slots__ = ('lb', 'ub', 'assigned', 'failed', 'space', 'deps')
	def __init__(self, lb, ub, deps=[[], [], []]):
		self.lb = lb
		self.ub = ub
		self.assigned = lb == ub
		self.failed = lb > ub
		self.space = None
		self.deps = deps
	
	def copy(self):
		"""Returns a copy of this VariableDomain"""
		copy = EmptyVariableDomain()
		copy.__class__ = self.__class__
		# copy instance variables
		copy.lb = self.lb
		copy.ub = self.ub
		copy.assigned = self.assigned
		copy.failed = self.failed
		copy.space = self.space
		
		return copy
