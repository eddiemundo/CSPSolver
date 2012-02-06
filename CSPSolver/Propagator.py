'''
Created on Feb 4, 2012

@author: Shenra
'''
class EmptyPropagator:
	__slots__ = ()

class Propagator:
	__slots__ = ()
	def __init__(self, store, variableNames):
		self.store = store
		self.variableNames = variableNames
		
	def propagate(self):
		print("Override me")
	
	def copy(self):
		copy = EmptyPropagator()
		copy.__class__ = self.__class__
		# copy instance variables
		copy.store = self.store
		copy.variableNames = self.variableNames
		