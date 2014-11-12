#!/bin/python
#hecher markus 7/2013
#helping stuff for grounded extension

from PredicateHandler import *
from DflatDecomposition import *

class DflatPredicateReader(PredicateReader):

	BAGINPUT = 0
	CHILDTAB = 1
	MODEL = 2

	def __init__(self):
		BI = DflatPredicateReader.BAGINPUT
		CT = DflatPredicateReader.CHILDTAB
		MD = DflatPredicateReader.MODEL
		
		super(DflatPredicateReader, self).__init__({
			#"current" : BI, "childNode" : BI, "childBag" : BI, "root" : BI,
			"currentNode" : BI, "childNode" : BI, "final" : BI, "current" : BI,
			"root" : CT, "childItem" : CT, "childCost" : CT, "sub" : CT, 
			"childAnd" : CT, "childOr" : CT, "childAccept" : CT, "childReject" : CT, "childAuxItem" : CT,  
			"itemTreeNodeHasAddress" : MD, "itemTreeNodeExtends" : MD })
		#self._decomp = {}	#whole decomposition
		self._decompByID = {}	#whole decomposition
		self._decelem = None	#current node/element of the decomp
		
		self._node = None
		self._bag = []		#bag contents
		self._childnodes = []	#child nodes
		self._root = False
	
		self._prev = DflatPredicateReader.BAGINPUT	
		self._rows = {}		#childrows accessed by RID (temporary)
		#self._decelems = {}
		#self._rowAtLv = []	#rows
		#self._rowByRID = {}	#already found childrows accessed by RID

	#def getDecomp(self):
	#	return self._decomp

	def onMatch(self, inpt):
		#print inpt
		for i in inpt:
			if type(i) is list:
				typ = self._preds.get(i[0])
				if typ == DflatPredicateReader.BAGINPUT:
					if not self._decelem is None: #clear
						#for chld in self._decelem.prev():
						#	chld.clearIds()
						self._clearTmpIDs()
						self._decelem = None
					if i[0] == "currentNode":
						self._node = i[1]
					elif i[0] == "current":
						self._bag.append(i[1])
					elif i[0] == "childNode":
						elem = self._decompByID.get(i[1])
						#print "CHILD", i[1], elem
						assert (not elem is None)
						self._childnodes.append(elem)
					self._prev = typ
				elif typ >= DflatPredicateReader.CHILDTAB:
					self._makeDecompNode()
					if self._prev == DflatPredicateReader.BAGINPUT:
						if i[0] == "root":
							#assert(len(self._rows) == 0)
							#self._decelem.addTmpRow(self._addTmpRow(i[1]))
							self._decelem.addRow(self._addTmpRow(i[1]))
						elif i[0] == "childItem" or i[0] == "childAuxItem":
							#print "ITEM", i[1], i[2]
							r = self._addTmpRow(i[1])
							r.add(i[2])
							if i[0] == "childAuxItem":
								r.addAux(i[2])
							#print self._addTmpRow(i[1])
						elif i[0] == "childCost":
							self._addTmpRow(i[1]).setCost(i[2])
						elif i[0] == "sub":
							rpar = self._addTmpRow(i[1])
							rsub = self._addTmpRow(i[2])
							#print "SUUUUUB", rpar, rsub
							#rpar.addTmpRow(rsub)
							rpar.addRow(rsub)
						elif i[0] == "childAnd":
							self._addTmpRow(i[1]).setFlag(DflatRow.AND_ROW)
						elif i[0] == "childOr":
							self._addTmpRow(i[1]).setFlag(DflatRow.OR_ROW)
						elif i[0] == "childAccept":
							self._addTmpRow(i[1]).setFlag(DflatRow.ACCEPT_ROW)
						elif i[0] == "childReject":
							self._addTmpRow(i[1]).setFlag(DflatRow.REJECT_ROW)

							#rsub.setUsed()
					if typ == DflatPredicateReader.MODEL:
						#if not self._decelem.getTmpRows() is None:
							#print "FINISH"
						#	self._decelem.finishRows()
						if i[0] == "itemTreeNodeHasAddress":
							if not self._root:
								addr = self._rows.get(i[1])
								assert(not addr is None)
								self._decelem.getIds()[i[2]] = addr
						elif i[0] == "itemTreeNodeExtends":
							#print i
							elem = self._rows.get(i[1])
							assert(not elem is None)
							tp = i[2]
							if len(tp) >= 1 and tp[0] == "tuple" and len(self._decelem.next()) >= len(tp) - 1:
								prev = []
								for j in range(1, len(tp), 1):
									#print self._decelem.next()
									afrchild = self._decelem.next()[j - 1].getIds()[tp[j]]
									afrchild.addNext(elem)
									prev.append(afrchild)
								#assert(len(elem.prev()) == 0)
								elem.addPrev(prev)
							else:	
								assert(False)
						self._prev = typ					
			elif type(i) is str:
				typ = self._preds.get(i)
				if typ == DflatPredicateReader.BAGINPUT and i == "final":
					#print "ROOT"
					self._root = True
#	@staticmethod
#	def getLvVal(i):	
#		lv = 0
#		if len(i) == 2:
#			val = i[1]
#		else:
#			lv = int(i[1])
#			val = i[2]
#		return (lv, val)

	def _makeDecompNode(self):
		if self._decelem is None:
			assert(not self._node is None)
			self._decelem = DflatDecomposition(self._bag)
			self._decelem.setNr(self._node)
			#self._decelems[self._decelem.id()] = self._decelem
			#self._decomp[self._decelem.id()] = self._decelem
			self._decompByID[self._node] = self._decelem
			#print "CHILDS", self._childnodes
			self._decelem.setNext(self._childnodes)
			for k in self._childnodes:
				k.addPrev(self._decelem)
				del self._decompByID[k.nr()]
			#clear
			self._childnodes = []
			self._bag = []
			self._rows = {}
			self._node = None


	def _clearTmpIDs(self):
		DflatPredicateReader._clearTmpIDsOf(self._decelem)

	@staticmethod
	def _clearTmpIDsOf(elem):
		for j in elem.prev():
			j.clearIds()


	def onFinish(self):
	#	print "FIN"

		self._makeDecompNode()
		#assert(len(self._decompByID) == 1)
		for k in self._decompByID:
			i = self._decompByID[k]
			self._clearTmpIDsOf(i)
			i.clearIds()
			self._childnodes.append(i) #for non-root tree case
	
		if len(self._decompByID) > 1: #non-root tree
			self._node = -1
			self._bag.append("...")
			self._decelem = None
			self._makeDecompNode() #make inofficial super-root
		
		#if not self._decelem is None:
		#	self._decelem.clearIds()
		#else:
		#	self._makeDecompNode()

	def _addTmpRow(self, k):
		itm = self._rows.get(k)
		if itm is None:
			itm = DflatGUIRow()
			self._rows[k] = itm
		#print "GOING TO ADD", itm, k
		return itm

	def getRoot(self):
		#print self._root

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	
		#REMOVED ALL THE ROOT CHECK!
		#if not self._root:
		#	return None
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	
		return self._decelem

#	def _findChildRow(self, p, k, v):
#		#print "TOADD", k, self._rows
#		if self._rowByRID.get(k) is None:
#			f = self._getRowSafe(p, v)
#			#print "SARCHING", k, v.id(), p, f
#			if not f is None:
#				for j in v.next():
#					r = self._rows[j]
#					if not self._findChildRow(f, j, r):
#						return False
#					v.addRow(r)
#				v.setNext([])
#				#print "ADDED", k
#				self._rowByRID[k] = f
#			else:
#				return False
#		#print "ROWS", self._rows
#		return True

#	def _getRowSafe(self, p, n):
#		n.addZeroCost()
#		return p.rows().get(n.id())
			

#	def _commitRow(self):
#		if len(self._rowAtLv) > 0:
#			p = self._decelem
##			for it in self._rowAtLv:
#				itm = self._getRowSafe(p, it)
#				if itm is None:
#					itm = it
#					p.addRow(it)
#					itm.setPrev([it.prev()])	
#					#it.setNext([]) #remove parents
#				else:
#					for i in it.prev(): #add parent refs
#						i.addNext(itm)
#					itm.addPrev(it.prev())	
#				#print "PREVADD", itm, itm.prev()
#				p = itm
#			self._rowAtLv = []
#	
##	def _allocateRowSpace(self, lv):
#		while len(self._rowAtLv) < lv + 1: 
#			self._rowAtLv.append(DflatGUIRow())

					

