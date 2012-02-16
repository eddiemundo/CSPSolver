"""
Created on Feb 4, 2012

@author: Jonathan Shen

Gecode style event system. It has 4 events.

		dmc
       /   \
	lbc	    ubc
	   \   /
		asn

(Simplified) Propagation conditions:
4: {asn, lbc, ubc, dmc}
3: {asn, lbc, ubc}
2: {asn, ubc}
1: {asn, lbc}
0: {asn}

(Simplified) Modification events:
4: {asn, lbc, ubc, dmc} schedule(0, 4)
3: {lbc, ubc, dmc} (bbc) schedule(1, 4)
2: {lbc, dmc} (lbc) schedule(1, 1); schedule(3, 4)
1: {ubc, dmc} (ubc) schedule(2, 4)
0: {dmc} (inner) schedule(4, 4)

Gecode uses an indexed dependency array to store the propagator dependencies in
the Variable. In theory you could use a simple array for every propagation
condition instead, but they don't.

The reasoning is that they can iterate over multiple propagation conditions
without overhead if they store all the propagators in one array. This is C++
code btw, so this may not be useful in pure python coding.


(Normal) Propagation conditions:
7: {asn, lbc, ubc, dmc}
6: {asn, lbc, ubc}
5: {asn, lbc}
4: {asn, ubc}
3: {lbc, ubc}
2: {ubc}
1: {lbc}
0: {asn}

(Normal) Modification events:
6: {asn, lbc, ubc, dmc} schedule(0-7)
5: {lbc, ubc, dmc} schedule(1-7)
4: {asn, ubc, dmc} schedule(0,2-7)
3: {asn, lbc, dmc} schedule(0-1,3-7)
2: {ubc, dmc} schedule(2-4,6-7)
1: {lbc, dmc} schedule(1,3,5-7)
0: {dmc} schedule(7)
"""
import abc

class EventSystem(object):
	__slots__ = ()
	__metaclass__ = abc.ABCMeta
	
	@abc.abstractclassmethod
	def subscribe(self, p, cond):
		"""Subscribe propagator p for condition cond to variable"""
		return
	
	@abc.abstractclassmethod
	def cancel(self, p, cond):
		"""Cancel p for condition cond from this variable's subscription"""
		return
	
	@abc.abstractclassmethod
	def schedule(self, me):
		"""Schedule propagators for these modification events"""
		return

	
class DmcEventSystem(EventSystem):
	"""
	An event system containing a single "domain change" event (dmc).
	
	Propagation conditions (ANY EVENTS):
	0:{dmc}
	Modification events (ALL EVENTS):
	0:{dmc}
	"""
	__slots__ = ('_pq', '_dmc')
	def __init__(self, propagatorQueue):
		self._pq = propagatorQueue
		self._dmc = []
	
	def subscribe(self, p, cond=0):
		"""Subscribe a propagator to dmc events for this variable"""
		self._dmc.append(p)
		
	def cancel(self, p, cond=0):
		"""Cancels propagator suscribed to condition"""
		# raises exception if p is not in the list
		self._dmc.remove(p)
			
	def schedule(self, me=0):
		"""Schedules propagators listening to any event in me"""
		self._pq.extend(self._dmc)


class AsnDmcEventSystem(EventSystem):
	"""
	An event system containing two events: "asn", and "dmc".
	
	Propagator conditions (ANY EVENTS):
	1:{asn, dmc}
	0:{asn}
	Modification Events (ALL EVENTS):
	1:{asn, dmc} schedule(0-1)
	0:{dmc} schedule(1)
	"""
	__slots__ = ('_pq', '_asn', '_asndmc')
	def __init__(self, propagatorQueue):
		self._pq = propagatorQueue
		self._asn = []
		self._asndmc = []
		
	def subscribe(self, p, cond):
		"""Subscribe a propagator to dmc events for this variable"""
		# can remove if statement by using a dict
		if cond == 0:
			self._asn.append(p)
		elif cond == 1:
			self._asndmc.append(p)
		
	def cancel(self, p, cond):
		"""Cancels propagator suscribed to condition"""
		# can remove if statement by using a dict
		if cond == 0:
			self._asn.remove(p)
		elif cond == 1:
			self._asndmc.remove(p)
		
	def schedule(self, me):
		"""Schedules propagators listening to any event in me"""
		if me == 0:
			self._pq.extend(self._asndmc)
		elif me == 1:
			self._pq.extend(self._asn)
			self._pq.extend(self._asndmc)
			

class GecodeEventSystem(EventSystem):
	"""
	An event system containing "asn", "lbc", "ubc", "dmc" events.
	
	(Simplified) Propagation conditions:
	4: {asn, lbc, ubc, dmc}
	3: {asn, lbc, ubc}
	2: {asn, ubc}
	1: {asn, lbc}
	0: {asn}
	
	(Simplified) Modification events:
	4: {asn, lbc, ubc, dmc} schedule(0-4)
	3: {lbc, ubc, dmc} (bbc) schedule(1-4)
	2: {lbc, dmc} (lbc) schedule(1, 3-4)
	1: {ubc, dmc} (ubc) schedule(2-4)
	0: {dmc} (inner) schedule(4)
	"""
	__slots__ = ('_pq', '_asn', '_asnlbc', '_asnubc', '_asnlbcubc',
				'_asnlbcubcdmc')
	def __init__(self, propagatorQueue):
		self._pq = propagatorQueue
		self._asn = []
		self._asnlbc = []
		self._asnubc = []
		self._asnlbcubc = []
		self._asnlbcubcdmc = []
	
	def subscribe(self, p, cond):
		"""Subscribe a propagator to this variable for condition"""
		# can remove the if statements by using a dict
		if cond == 0:
			self._asn.append(p)
		elif cond == 1:
			self._asnlbc.append(p)
		elif cond == 2:
			self._asnubc.append(p)
		elif cond == 3:
			self._asnlbcubc.append(p)
		elif cond == 4:
			self._asnlbcubcdmc.append(p)
	
	def cancel(self, p, cond):
		"""Cancels propagator suscribed to condition"""
		# can remove the if statements by using a dict
		if cond == 0:
			self._asn.remove(p)
		elif cond == 1:
			self._asnlbc.remove(p)
		elif cond == 2:
			self._asnubc.remove(p)
		elif cond == 3:
			self._asnlbcubc.remove(p)
		elif cond == 4:
			self._asnlbcubcdmc.remove(p)
			
	def schedule(self, me):
		"""Schedules propagators listening to any event in me"""
		if me == 4:
			self._pq.extend(self._asn)
			self._pq.extend(self._asnlbc)
			self._pq.extend(self._asnubc)
			self._pq.extend(self._asnlbcubc)
			self._pq.extend(self._asnlbcubcdmc)
		elif me == 3:
			self._pq.extend(self._asnlbc)
			self._pq.extend(self._asnubc)
			self._pq.extend(self._asnlbcubc)
			self._pq.extend(self._asnlbcubcdmc)
		elif me == 2:
			self._pq.extend(self._asnlbc)
			self._pq.extend(self._asnlbcubc)
			self._pq.extend(self._asnlbcubcdmc)
		elif me == 1:
			self._pq.extend(self._asnubc)
			self._pq.extend(self._asnlbcubc)
			self._pq.extend(self._asnlbcubcdmc)
		elif me == 0:
			self._pq.extend(self._asnlbcubcdmc)
			