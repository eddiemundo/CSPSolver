'''
Created on Feb 4, 2012

@author: Shenra
'''

from collections import deque
class EmptySpace:
	__slots__ = ('variableNames', 'variableDomains', 'store', 'assigned', 'failed')

class Space:
	__slots__ = ('variableNames', 'variableDomains', 'store', 'assigned', 'failed')
	def __init__(self, variableNames=[], variableDomains=[], initialPropagators):
		self.variableNames = variableNames
		self.variableDomains = variableDomains
		self.store = dict(zip(variableNames, variableDomains))
		self.propagatorQueue = deque(initialPropagators)
		self.assigned = True
		self.failed = False
		for vd in variableDomains:
			vd.space = self
			if not vd.assigned:
				self.assigned = False
			if vd.failed:
				self.failed = True
	
	def copy(self):
		copy = EmptySpace()
		copy.__class__ = self.__class__
		# copy instance variables
		copy.variableNames = self.variableNames
		copy.variableDomains = [vd.copy() for vd in self.variableDomains]
		copy.store = dict(zip(self.variableNames, copy.variableDomains))
		copy.propagatorQueue = self.propagatorQueue
		copy.assigned = self.assigned
		copy.failed = self.failed
		
		return copy