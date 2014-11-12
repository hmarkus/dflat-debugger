#!/bin/python

from pyparsing import *
import signal
import os
import io
import re
import sys
from DflatPredicateHandler import *
from DflatGUI import *
#from DflatDecomposition import *

#def safeClose(f):
#	try:
#		f.close()
#	except IOError:
#		pass

class DflatDebugger:
	def __init__(self):
		self._ui = DflatDebuggerGUI()
		self._pr = DflatPredicateReader()
		self._ph = PredicateHandler(self._pr, self._pr)

	def interrupt(self):
		return self._ph.interrupt()

	def ui(self):
		return self._ui

	def predReader(self):
		return self._pr
	
	def parse(self, inptf, outpf):
		try:
			self._ph.read(inptf)
			self._ph.write(outpf)
		except IOError as e:
			print e
		safeClose(inptf)
		#safeClose(outpf)
		
	

#def test(inptf):
#	d.parse(inptf, sys.stdout)
#	de = d.predReader().getRoot()
	
#	dc = d.predReader().getDecomp()
#	print dc
#	print
#	print
#	for i in dc:
#		if i == "[]":
#			print dc[i].rows()
#			print
#			for j in dc[i].rows():
#				print "!!"#, g.getDecomp()[i].rows()[j]
#				printDec(1, dc[i].rows()[j])
#			#for j in g.getDecomp()[i].rows():
#			#	p = g.getDecomp()[i].rows()[j]
#				#while not p is None:
#			#	print p
#			#	for j in p.prev():
#			#		print "->", j
#				#for k in g.getDecomp()[i].next():
#				#	for l in k.rows():
#				#		for m in k.rows()[l].next():
#				#			if m.id() == j:
#				#				print m
#				
#				#print j.rows()
#				#print
#			#print i + ": " + str(g.getDecomp()[i])
#			print

#	d.ui().main(de)

#def printDec(i, p):
#	print p
	#print "ROW", p, p.prev()
	#for j in p.:
		#p = g.getDecomp()[i].rows()[j]
		#while not p is None:
		#print p.rows()[j]
		#print "PREV", p.rows()[j].prev()
#	for k in p.prev():
		#print k
#		print "->" * i#, j
#		for d in k:
#			printDec(i + 1, d)
#		print

def signal_handler(signal, frame):
	if d.interrupt():
		sys.exit(0)

#debugger
d = None

if __name__ == "__main__":
	d = DflatDebugger()
	fi = sys.stdin
	#fo = sys.stdout
	if len(sys.argv) > 1:
		#fo = file(sys.argv[1], "w")
		#if len(sys.argv) > 2:
			fi = file(sys.argv[2], "r")
			if len(sys.argv) > 1:
				print "usage: python " + __name__ + " <inputfile?>"
				sys.exit(1)
	signal.signal(signal.SIGINT, signal_handler)
	
	d.parse(fi, sys.stdout)
	de = d.predReader().getRoot()
	d.ui().main(de)

