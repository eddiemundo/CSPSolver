'''
Created on Feb 4, 2012

@author: Shenra
'''
import collections
from VariableDomain import VariableDomain

class EmptyStore(collections.MutableMapping):
	__slots__ = ('store')

class Store(collections.MutableMapping):
	__slots__ = ('store')
	"""
	A dictionary containing mapping variable names to VariableDomains.
	
	A store can be failed, meaning that one of its VariableDomains is the empty
	set.
	
	A store can be assigned, meaning that all of its VariableDomains contain
	exactly one value.
	"""
	def __init__(self, *args, **kwargs):
		self.store = dict()
		self.update(dict(*args, **kwargs))
		#self.failed = False
		#self.assigned = True
		for v in self.store.values():
			if not isinstance(v, VariableDomain):
				raise TypeError
		#	self.failed |= v.failed
	#		self.assigned &= v.assigned
	
	def copy(self):
		pass
	
	def __repr__(self):
		return str(self.store)
	
	def __str__(self):
		return self.__repr__()
	
	def __getitem__(self, key):
		return self.store[key]
	
	def __setitem__(self, key, value):
		self.store[key] = value
	
	def __delitem__(self, key):
		del self.store[key]
	
	def __iter__(self):
		return iter(self.store)
	
	def __len__(self):
		return len(self.store)
	
	def assigned(self):
		for vd in self.store.values():
			if not vd.assigned:
				return False
		return True
	
	def failed(self):
		for vd in self.store.values():
			if vd.failed:
				return True
		return False