'''
Created on Feb 4, 2012

@author: Shenra
'''
import timeit
from collections import namedtuple
from copy import copy, deepcopy
from VariableDomain import VariableDomain

def timef(funcname, *args, **kwargs):
	"""
	timeit a func with args, e.g.
		for window in ( 3, 31, 63, 127, 255 ):
			timef( "filter", window, 0 )
	This doesn't work in ipython; see Martelli, "ipython plays weird tricks with
	__main__" in Stackoverflow        
	"""
	argstr = ", ".join(["%r" % a for a in args]) if args else ""
	kwargstr = ", ".join([ "%s=%r" % (k, v) for k, v in kwargs.items()]) \
		if kwargs  else ""
	comma = ", " if (argstr and kwargstr)  else ""
	fargs = "%s(%s%s%s)" % (funcname, argstr, comma, kwargstr)
	# print "test timef:", fargs
	print("from __main__ import %s" % funcname)
	t = timeit.Timer(fargs, "from __main__ import %s" % funcname)
	ntime = 3
	print("%.0f microsecond %s" % (t.timeit(ntime) * 1e6 / ntime, fargs))


		

def main():	
	
	def test():
		pass
	
	deps = []
	idx = [0, 0, 0, 0, 0, 0]

	def subscribe(p, condition):
		# there are a maximum of 5 propgation conditions, and an end idx
		for i in reversed(range(condition + 1, 6)):
			idx[i] += 1
		deps.insert(idx[condition], p)
	
	def cancel(p, condition):
		"""Cancels propagator suscribed to condition"""
		# will return an error if there is no such propagator
		i = idx[condition] + deps[idx[condition]:idx[condition+1]+1].index(p)
		deps.pop(i)
		for i in reversed(range(condition + 1, 6)):
			idx[i] -= 1
	
	def schedule(conditionStart, conditionEnd):
		"""Schedules propagators that depent on conditionStart to conditionEnd"""
		for i in range(idx[conditionStart], idx[conditionEnd+1] - 1):
			# add propagator to the queue
			pass
			
	
	
	subscribe("v44", 4)
	subscribe("v0", 0)
	subscribe("v00", 0)
	subscribe("v333", 3)
	subscribe("v1", 1)
	subscribe("v11", 1)
	subscribe("v2", 2)
	subscribe("v000", 0)
	subscribe("v3", 3)
	subscribe("v33", 3)
	subscribe("v4", 4)
	cancel("v4", 4)
	schedule(0,4)
	
	print(deps)
	print(idx)
		
	counts = [10, 100, 1000, 10000]
	for count in counts:
		print('n=' + str(count) + ': ' + str(min(timeit.Timer(test).repeat(7, count)) / count))
	

main()
