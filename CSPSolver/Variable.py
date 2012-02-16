class EmptyVariable:
	"""For fast copying"""
	__slots__ = ('lb', 'ub', 'assigned', '_propagatorQueue', '_idx', '_deps', '_solver')

class Variable(object):
	"""
	Represents an integer variable in the CSP.
	
	A Variable has a _domain represented by a set()
	
	A Variable can be failed, meaning it can contain no values.
	
	A Variable can be assigned, meaning it can contain only one value.
	
	Usually is a subclass of an EventSystem.
	"""
	__slots__ = ('_domain', 'assigned', '_eventSystem')
	def __init__(self, initialSetOfValues, eventSystem):	
		self._domain = set(initialSetOfValues)
		self.assigned = len(initialSetOfValues) == 1
		self._eventSystem = eventSystem
		
	def __repr__(self):
		return (self.lb, self.ub).__repr__()
	
	def __str__(self):
		return self.__repr__()
	
	def removeFromDomain(self, elements):
		"""Removes elements from variable's _domain"""
		
		# Everything below depends on the event system used. In order to
		# decouple it all, the event system either has to use a unique number
		# for every set of events possible, or calculate the intersections 
		# between the propagator conditions and the modification events
		
		# Another solution is to have a Variable factory that spits out a
		# variable that has a removeFromDomain() that sends the right
		# modification events depending on which EventSystem it got
		
		# Currently we're assuming that the event system is an AmcDmcEventSystem
		domain = self._domain
		_len = len
		initialCardinality = _len(domain)
		
		domain.difference_update(elements)
		
		currentCardinality = _len(domain)
		dmc = currentCardinality < initialCardinality
		asn = currentCardinality == 1
		if dmc and asn:
			self.assigned = True 
			self._eventSystem.schedule(1)
		elif dmc:
			self._eventSystem.schedule(0)
			
				
			
	
	
	