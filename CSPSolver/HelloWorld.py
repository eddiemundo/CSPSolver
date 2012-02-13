'''
Created on Feb 4, 2012

@author: Shenra
'''
import timeit
from collections import namedtuple, deque
from copy import copy, deepcopy
from VariableDomain import VariableDomain
from Store import Store


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


class fakedict(dict):
	__slots__ = ()



def main():	
	pq = deque()
	names = ['a']
	values = [VariableDomain(0,0, pq)]
	def test():
		f = dict(zip(names, values))
		f['a'] == values[0]
		
		#print(f['a'])
	
	counts = [10, 100, 1000, 10000]
	for count in counts:
		print('n=' + str(count) + ': ' + str(min(timeit.Timer(test).repeat(7, count)) / count))
	

main()
