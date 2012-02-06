'''
Created on Feb 4, 2012

@author: Shenra
'''
import collections
from VariableDomain import VariableDomain

class Store(collections.MutableMapping):
	"""A dictionary containing VariableDomains"""
	def __init__(self, *args, **kwargs):
		self.store = dict()
		self.update(dict(*args, **kwargs))
		for v in self.store.values():
			if not isinstance(v, VariableDomain):
				raise TypeError
	
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
	
	def copy(self):
		return Store(self.store)
		