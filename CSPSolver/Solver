'''
Created on Feb 4, 2012

@author: Shenra


There are no propagators implemented yet so currently it just searches and
accepts the entire domain.
'''


from Store import Store
from VariableDomain import VariableDomain
from collections import deque
import cProfile
import pstats

class Solver:
	"""
	Contains the initial state of the problem to be solved, and some helper
	methods.
	
	self.solve(self.store) actually solve the problem
	"""
	def __init__(self, variableNames, variableDomains, deps=[], initialPropagators=[]):
		"""
		Input:
		variablesNames = variable names in the order you want them assigned
		variableDomains = the domains of the variables. order should reflect
		order of variable names
		deps = what propagator should be scheduled.
		(variablename, propagator, condition)
		initialPropagators = the propagators you want run on the domain
		initially
		
		
		"""
		self.variableNames = variableNames
		self.variableDomains = variableDomains
		self.propagatorQueue = deque(initialPropagators)
		self.store = dict(zip(variableNames, variableDomains))
		# so we can fail a node faster
		self._nodeFailed = self.failed(self.store)
		
		for vn in variableNames:
			self.store[vn]._propagatorQueue = self.propagatorQueue
			# give each variable a reference to the containing solver
			self.store[vn]._solver = self
		
		for vn, p, cond in deps:
			self.store[vn].subscribe(p, cond)
	
	
	def failed(self, s):
		"""Helper method only run during __init__"""
		for vd in s.values():
			if vd.lb > vd.ub:
				return True
		return False
	
	def assigned(self, s):
		for vd in s.values():
			if not vd.assigned:
				return False
		return True
	
	def solve(self, s):
		"""
		Currently does NOT solve sudoku puzzles. It's just currently a test
		template for such a solver.
		
		Solve() only is currently good only for single threaded operation
		
		"""
		pq = self.propagatorQueue
		while pq:
			pq.popleft().propagate()
	
		if self._nodeFailed:
			return
		
		if self.assigned(s):
			#print(s)
			return
		
		# copy our store in order to branch
		scopy = dict()
		for vn, vd in s.items():
			if vd.assigned:
				scopy[vn] = vd
			else:
				scopy[vn] = vd.copy()
		
		# branching strategy is contained here
		for vn in self.variableNames:
			if not s[vn].assigned:
				# recursively solve s
				s[vn].setub(s[vn].lb)
				self.solve(s)
				
				# then solve scopy
				scopy[vn].setlb(scopy[vn].lb + 1)
				self.solve(scopy)
				
				# the reason for the above order is because
				# setlb/setub have side effects that change
				# pq, and since I don't want to copy every branch, we have to do
				# this.
				break


def main():
	variableNames = ['v1', 'v2', 'v3', 'v4']
	
	# set up the variable domains associated with the variableNames
	variableDomains = [
					VariableDomain(0, 20),
					VariableDomain(0, 20),
					VariableDomain(0, 20),
					VariableDomain(0, 20),
					]
	
	sudoku = Solver(variableNames, variableDomains)
	sudoku.solve(sudoku.store)


if __name__ == "__main__":
	cProfile.run('main()', 'SolverProfile')
	p = pstats.Stats('SolverProfile')
	p.strip_dirs().sort_stats('time').print_stats()
	
	
	
	
	
	