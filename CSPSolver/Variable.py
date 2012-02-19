class EmptyVariable(object):
	__slots__ = ('name', 'domain', 'assigned')


class Variable(object):
	__slots__ = ('name', 'domain', 'assigned')
	
	def __init__(self, name, domain_values):
		self.name = name
		self.domain = set(domain_values)
		self.assigned = len(domain_values) == 1
		
	def __repr__(self):
		return str(self.domain)
	
	def copy(self):
		self_copy = EmptyVariable()
		self_copy.__class__ = self.__class__
		self_copy.name = self.name
		self_copy.domain = self.domain.copy()
		self_copy.assigned = self.assigned
		return self_copy
	
	def pruneFromDomain(self, domain_values):
		self.domain.difference_update(domain_values)
		if len(self.domain) == 1:
			self.assigned = True
	
	def popFromDomain(self):
		if len(self.domain) == 2:
			self.assigned = True
		return self.domain.pop()