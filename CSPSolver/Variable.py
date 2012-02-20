'''
Created on Feb 4, 2012

@author: Jonathan Shen

Variables classes go here.

Additional possibilies include Bounds variables, and different event systems 
'''
from collections import deque

class EmptyVariable(object):
	__slots__ = ('name', 'domain', 'assigned', 'pool', 'pq', 'asn', 'asndmc')

class Variable(object):
	"""Represents a variable in a CSP"""
	__slots__ = ('name','domain', 'assigned', 'pool', 'pq', 'asn', 'asndmc')
	
	def __init__(self, name, domain_values, propagator_queue):
		# for our event system
		self.pq = propagator_queue
		self.asn = []
		self.asndmc = []
		# for our variable
		self.name = name
		self.domain = set(domain_values)
		self.assigned = len(domain_values) == 1
		
	def __repr__(self):
		return str(self.domain)
	
	def copy(self):		
		self_copy = EmptyVariable()
		self_copy.__class__ = Variable
		self_copy.name = self.name
		self_copy.domain = self.domain.copy()
		self_copy.assigned = self.assigned
		self_copy.asn = self.asn[:]
		self_copy.asndmc = self.asndmc[:]
		# self_copy.pq is set in Space, when space is copied
		
		return self_copy
	
	def pruneFromDomain(self, domain_values):
		"""
		Input: an iterable domain_values containing values to prune from the
		domain
		
		Function: Removes values in domain_values from self.domain. Schedules
		propagators depending on what events the removals produce.
		
		Returns: True/False - whether or not the domain becomes empty 
		"""
		self.domain.difference_update(domain_values)
		# if already assigned, and domain doesn't change then don't schedule
		# anything. Kinda sloppy, but saves some CPU time
		if not self.assigned:
			if len(self.domain) == 1:
				self.assigned = True
				self.schedule(0)
				return False
		# if domain is not empty
		if self.domain:
			return False
		else:
			return True

	def popFromDomain(self):
		"""
		Function: Removes an arbitrary element from the domain. Will schedule
		propagators depending on what events occur.
		
		Returns: True/False - whether or not the domain becomes empty
		
		Note: Does NOT return what is popped off
		"""
		self.domain.pop()
		# we don't do the same check as pruneFromDomain cause popFromDomain
		# is only used by branch(), and branch does the assign check beforehand
		
		if len(self.domain) == 1:
			self.assigned = True
			self.schedule(0)
			return False
		elif self.domain:
			return False
		else:
			return True  

	def assign(self, i):
		"""
		Input: an integer i that is contained in self.domain
		
		Function: Assign the domain of this variable to i. Also schedules any
		propagators listening to events on this variable, if those events
		occur from this assigning.
		
		Note: this is a convenience method
		"""
		self.pruneFromDomain(self.domain.symmetric_difference((i,)))
		
	# below is a very barebones listener pattern for only 2 events asn, and dmc
	def subscribe(self, props, cond):
		"""
		Input: An iterable props containing propagators, and a integer cond
		
		Function: Subscribes propagators in props to this variable for condition
		cond. 
		"""
		pairs = [(p, self) for p in props] 
		# can remove if statement by using classes for the conditions, but
		# too much overhead
		if cond == 0:
			self.asn.extend(pairs)
		elif cond == 1:
			self.asndmc.extend(pairs)

	def cancel(self, p, cond):
		"""
		Input: A propagator p, and a integer cond
		
		Function: Cancels propagator p subscribed to this variable with
		condition cond
		"""
		if cond == 0:
			self.asn.remove((p, self))
		elif cond == 1:
			self.asndmc.remove((p, self))

	def schedule(self, me):
		"""
		Input: an integer me that is either 0 or 1. 
		0 is an asn event, and a dmc event
		1 is a dmc event (any event that doesn't result in an assigned domain)
		
		Function: Schedules propagators listening to any event me
		"""
		if me == 0:
			self.pq.extend(self.asn)
			self.pq.extend(self.asndmc)
		elif me == 1:
			self.pq.extend(self.asndmc)
	