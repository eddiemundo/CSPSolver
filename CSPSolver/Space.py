'''
Created on Feb 17, 2012

@author: Jonathan Shen
'''
from Variable import Variable
from collections import deque

class EmptySpace(object):
	__slots__ = ('pq', 'variable_store')

class Space(object):
	"""Contains all the state needed for our CSP solver"""

	__slots__ = ('pq', 'variable_store')
	
	def __init__(self, variables_info):
		"""
		Input: variables_info[var_name] = (domain, deps)
			   deps = (((propagator1, ...), condition1), ...)
			   
		Function: Sets up the space for the solver.
		"""
		self.pq = deque()
		self.variable_store = {}
		for v_name, v_info in variables_info.items():
			# create variable and add it to the variable store
			self.variable_store[v_name] = Variable(v_name, v_info[0], self.pq)
			# subscribe propagators that depend on this variable
			for props, cond in v_info[1]:
				self.variable_store[v_name].subscribe(props, cond)
				# don't forget to give each propagator the variable_store ref
				for p in props:
					p.variable_store = self.variable_store
	
	def __repr__(self):
		"""For sudoku"""
		string = ""
		for row in range(1, 10):
			for col in range(1, 10):
				try:
					num, = self.variable_store[str(row) + str(col)].domain
					string += str(num) + '  '
				except ValueError:
					if not self.variable_store[str(row) + str(col)].domain:
						string += 'E  '
					else:
						string += '_  '
				
			string += '\n'
		string += '--------------------------'
		return string
		#return str(self.variable_store)
		
	def copy(self):
		"""
		Doesn't deep copy variable if variable is assigned. Will be a problem
		for certain CSPs and propagators. This can be fixed by either deep
		copying the variable every time (performance hit), or checking whether
		a Variable.pruneFromDomain() and Variable.popFromDomain would empty the
		variable's domain and NOT empty it, but instead return a flag or code
		telling Space that it is a failed domain/Space. The second option still
		affects performance though
		"""
		self_copy = EmptySpace()
		self_copy.__class__ = self.__class__
		self_copy.pq = deque()
		self_copy.variable_store = {}
		for vn, v in self.variable_store.items():
			if v.assigned:
				self_copy.variable_store[vn] = v
			else:
				self_copy.variable_store[vn] = v.copy()
				# insert pq into the copy here
				self_copy.variable_store[vn].pq = self_copy.pq
			
		return self_copy
		
	def assigned(self):
		"""
		Returns: True/False - whether or not every variable in this Space is
		assigned
		"""
		for v in self.variable_store.values():
			if not v.assigned:
				return False
		return True