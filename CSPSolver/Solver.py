'''
Created on Feb 4, 2012

@author: Jonathan Shen

A CSP solver, and an example of it solving a Sudoku puzzle with an all-different
constraint propagator
'''

from Space import Space
from collections import deque

import cProfile
import pstats


def branch(s):
	"""
	Input: a Space s
	
	Returns: references to two Spaces s1, and s2 such that, s1 U s2 == s
	
	Note: This function determines the branching strategy, and value ordering
	of our CSP solver  
	""" 
	s_copy = s.copy()

	for vn in s.variable_store:
		if not s.variable_store[vn].assigned:
			s_copy.variable_store[vn].popFromDomain()
			s.variable_store[vn].pruneFromDomain(s_copy.variable_store[vn].domain)
			break
	return s_copy, s

def solve(s):
	"""
	Input: a Space s
	
	Function: Prints solutions to the CSP
	"""
	s_pq_popleft = s.pq.popleft
	while s.pq:
		p, v = s_pq_popleft()
		# if propagator failes a domain
		if (p.propagate(v, s.variable_store)):
			return
	
	if s.assigned():
		print(s)
		return
	
	(s1, s2) = branch(s)
	solve(s2)
	solve(s1)
	
def loopSolve(s):
	stack = deque((s,))
	stack_pop = stack.pop
	stack_push = stack.extend
	
	
	while stack:
		s = stack_pop()
		failed = False
		
		while s.pq:
			p, v = s.pq.popleft()
			failed = p.propagate(v, s.variable_store) 
			if failed:
				break
		if failed:
			continue
		
		if s.assigned():
			print(s)
			continue
		
		stack_push(branch(s))
		
	
	


class AllDifferent(object):
	"""
	Propagator for all different constraints. Should only be run when an asn
	event occurs
	"""
	def __init__(self):
		self.name = None
		self.variable_names = []
	
	def propagate(self, variable, variable_store):
		"""
		Input: The assigned variable that scheduled the propagator
		
		Function: Prune the domains of the Variables in variable_store
		"""
		domain_to_prune = variable.domain
		
		for v_name in self.variable_names:
			if variable_store[v_name] is not variable:
				variable_store[v_name].pruneFromDomain(domain_to_prune)
				if not variable_store[v_name].domain:
					return True
		return False


def main():
	"""An example Sudoku puzzle solver"""
	# propagators
	row1 = AllDifferent()
	row2 = AllDifferent()
	row3 = AllDifferent()
	row4 = AllDifferent()
	row5 = AllDifferent()
	row6 = AllDifferent()
	row7 = AllDifferent()
	row8 = AllDifferent()
	row9 = AllDifferent()
	col1 = AllDifferent()
	col2 = AllDifferent()
	col3 = AllDifferent()
	col4 = AllDifferent()
	col5 = AllDifferent()
	col6 = AllDifferent()
	col7 = AllDifferent()
	col8 = AllDifferent()
	col9 = AllDifferent()
	box11 = AllDifferent()
	box12 = AllDifferent()
	box13 = AllDifferent()
	box21 = AllDifferent()
	box22 = AllDifferent()
	box23 = AllDifferent()
	box31 = AllDifferent()
	box32 = AllDifferent()
	box33 = AllDifferent()
	
	# Below we put all the variable info into the right structure so Space can
	# take it and construct its state. This is less annoying than handcoding it
	# but more complicated
	
	# variables_info[var_name] = (domain, deps)
	# deps = (((propagator1, ...), condition1), ...)
	variables_info = {}
	for row in range(1, 10):
		for col in range(1, 10):
			# the propagator for this row
			row_prop = locals()['row' + str(row)]
			row_prop.name = 'row' + str(row)
			row_prop.variable_names.append(str(row) + str(col))
			# the propagator for this column
			col_prop = locals()['col' + str(col)]
			col_prop.name = 'col' + str(col)
			col_prop.variable_names.append(str(row) + str(col))
			# the propagator for the box this variable is located in
			box_row = (row - 1) // 3 + 1
			box_col = (col - 1) // 3 + 1
			box_prop = locals()['box' + str(box_row) + str(box_col)]
			box_prop.name = 'box' + str(box_row) + str(box_col)
			box_prop.variable_names.append(str(row) + str(col))
			
			# the dictionary containing all the info space needs to construct
			# its variable store. Note range(1, 10) is the initial domain
			variables_info[str(row) + str(col)] = (range(1, 10), (((row_prop, col_prop, box_prop), 0),))
	
	# creating our initial problem Space object
	s = Space(variables_info)

	# Setting up the Sudoku puzzle
	s.variable_store['14'].assign(9)
	s.variable_store['17'].assign(6)
	s.variable_store['18'].assign(5)

	s.variable_store['21'].assign(9)
	s.variable_store['24'].assign(6)
	s.variable_store['25'].assign(1)
	s.variable_store['29'].assign(7)
	
	s.variable_store['35'].assign(2)
	s.variable_store['37'].assign(1)
	
	s.variable_store['42'].assign(2)
	s.variable_store['44'].assign(5)
	s.variable_store['47'].assign(4)
	s.variable_store['48'].assign(6)
	
	s.variable_store['53'].assign(4)
	s.variable_store['57'].assign(8)
	
	s.variable_store['62'].assign(7)
	s.variable_store['63'].assign(8)
	s.variable_store['66'].assign(1)
	s.variable_store['68'].assign(3)
	
	s.variable_store['73'].assign(5)
	s.variable_store['75'].assign(7)
	
	s.variable_store['81'].assign(6)
	s.variable_store['85'].assign(5)
	s.variable_store['86'].assign(2)
	s.variable_store['89'].assign(3)
	
	s.variable_store['92'].assign(3)
	s.variable_store['93'].assign(7)
	s.variable_store['96'].assign(6)
	
	
#	test_info = {}
#	test_info['v1'] = (range(0,15), [])
#	test_info['v2'] = (range(0,15), [])
#	test_info['v3'] = (range(0,15), [])
#	test_info['v4'] = (range(0,15), [])
#	
#	s2 = Space(test_info)
	
	#loopSolve(s2)
	
	# solve the puzzle
	solve(s)
	
if __name__ == "__main__":
	# profiler for speed checking
	cProfile.run('main()', 'SolverProfile')
	p = pstats.Stats('SolverProfile')
	p.strip_dirs().sort_stats('time').print_stats()
