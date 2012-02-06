'''
Created on Feb 4, 2012

@author: Shenra
'''
import timeit
from collections import namedtuple
from copy import copy, deepcopy
from VariableDomain import VariableDomain

def timef( funcname, *args, **kwargs ):
	"""
	timeit a func with args, e.g.
		for window in ( 3, 31, 63, 127, 255 ):
			timef( "filter", window, 0 )
	This doesn't work in ipython; see Martelli, "ipython plays weird tricks with
	__main__" in Stackoverflow        
	"""
	argstr = ", ".join(["%r" % a for a in args]) if args else ""
	kwargstr = ", ".join([ "%s=%r" % (k,v) for k,v in kwargs.items()]) \
		if kwargs  else ""
	comma = ", " if (argstr and kwargstr)  else ""
	fargs = "%s(%s%s%s)" % (funcname, argstr, comma, kwargstr)
	# print "test timef:", fargs
	print("from __main__ import %s" % funcname)
	t = timeit.Timer(fargs, "from __main__ import %s" % funcname)
	ntime = 3
	print("%.0f microsecond %s" % (t.timeit( ntime ) * 1e6 / ntime, fargs))


		

def main():	
	variableNames = ['v1', 'v2', 'v3']
	variableDomains = [VariableDomain(0,1), VariableDomain(0,0), VariableDomain(1,0)]
	Store = namedtuple('Store', variableNames)
	store = Store._make(variableDomains)
	z = zip(variableNames, variableDomains)
	d = dict(z)
	def test():
		print(isinstance(1, VariableDomain))
			
		
		
	counts = [10,100,1000,10000]
	for count in counts:
		print('n='+str(count)+': '+str(min(timeit.Timer(test).repeat(7, count)) / count))
	

main()