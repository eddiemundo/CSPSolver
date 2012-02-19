'''
Created on Feb 4, 2012

@author: Shenra


There are no propagators implemented yet so currently it just searches and
accepts the entire domain.
'''


from Space import Space
from Variable import Variable

import cProfile
import pstats


def branch(s):
	s_copy = s.copy()
	for vn in s.variable_store:
		if not s.variable_store[vn].assigned:
			s_copy.variable_store[vn].popFromDomain()
			s.variable_store[vn].pruneFromDomain(s_copy.variable_store[vn].domain)
			break
	return s, s_copy

def solve(s):
	if s.assigned():
		#print(s.variable_store)
		return
	
	(s1, s2) = branch(s)
	solve(s1)
	solve(s2)

def main():
	initial_variable_store = [
							Variable('v1', range(21)),
							Variable('v2', range(21)),
							Variable('v3', range(21)),
							Variable('v4', range(21)),
							]
	s = Space(initial_variable_store)
	solve(s)

if __name__ == "__main__":
	cProfile.run('main()', 'SolverProfile')
	p = pstats.Stats('SolverProfile')
	p.strip_dirs().sort_stats('time').print_stats()
	
	
	
	
	
	