'''
Created on Feb 4, 2012

@author: Shenra
'''
from VariableDomain import VariableDomain

def main():
	
	names = ['p'+str(i)+str(j) for i in range(9) for j in range(9)]
	print(names)

main()



def solve(s):
	for p in s.propagatorQueue:
		p.propagate()

	s1, s2 = s.branch()
	solve(s1)
	solve(s2)
	
	




	