#!/bin/python

class DflatIdentifiable(object):

	#SHOW_ALL = lambda _ : False	

	def __init__(self, keys):
		self._keys = keys
	
	def add(self, val):
		self._keys.append(val)

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return str(self._keys)

	def id(self):
		return DflatIdentifiable.idstr(self._keys)

	def keys(self):
		return self._keys

	#for the caller: catch regex exception!
	def search(self, searchfor, modi, results):
		#if regex:
		#	searchfor = re.compile(searchfor)
		#else:
		#	searchfor = None
		m = modi(self) #.content()
		#print m
		for i in m: #keys():
			#print i
			if not i is None:
				pos = None
				if not type(searchfor) is str:
					pos = searchfor.match(i)
					res = not pos is None
				else:
					pos = i.find(searchfor)
					res = pos >= 0
				if res:
					r = results[1].get(self)
					if r is None:
						results[1][self] = [pos]
					else:
						r.append(pos)
		
		if results[1].get(self):
			results[0].append(self)
			return True
		else:
			return False	
	
	@staticmethod	
	def idstr(val):
		val.sort()
		return str(val)

	def content(self):
		self.id()
		return DflatIdentifiable.contentStr(self._keys, lambda _ : False) #DflatIdentifiable.SHOW_ALL)

	@staticmethod	
	def contentItemStr(val):
		if type(val) is list:
			res = ""
			i = 0
			for j in val:
				if i == 0:
					res += j + "("
				else: #if not exc(j):
					if i > 1:
						res += ", "
					res += DflatIdentifiable.contentItemStr(j)
				i += 1
			res += ")"
			return res
		else:
			return val

	@staticmethod	
	def contentStr(val, exc):
		res = "["
		for j in val:
			if not exc(j):
				if len(res) > 1:
					res += ", "
				res += DflatIdentifiable.contentItemStr(j)
		res += "]"
		return res

class DflatSolution(DflatIdentifiable):
	#def __init__(self):
	#	super(DflatSolution, self).__init__({})
	
	def __init__(self, sol):
		if sol is None:
			sol = {}
		else:
			sol = dict(sol.keys())
		super(DflatSolution, self).__init__(sol)

        def content(self):
                self.id()
                return DflatIdentifiable.contentStr(self._keys, lambda x : x == "[]")

	def add(self, val):
		for i in val.keys():
			self._addID(DflatIdentifiable.contentItemStr(i), val)
			#self._addID(str(i), val)
		if len(val.keys()) == 0: # also consider empty sets
			#self._addID(str([]), val)
			self._addID(DflatIdentifiable.contentStr([], lambda _ : False), val) #DflatIdentifiable.SHOW_ALL), val)

	def _addID(self, ids, val):
		k = self._keys.get(ids)
		if k is None:
			self._keys[ids] = [val]
		else:
			k.append(val)


	def id(self):
		return DflatIdentifiable.idstr(self._keys.keys())


class DflatRowContainer(DflatIdentifiable):
	def __init__(self, keys):
		super(DflatRowContainer, self).__init__(keys)
		self._next = []
		self._prev = []
		#self._rows = {}
		self._rows = []
		self._node = None
		#self._tmprows = []

	#def getTmpRows(self):
	#	return self._tmprows
	
	#def addTmpRow(self, row):
		#self._tmprows.append(row)
	#	self._rows.append(row)

	#def finishRows(self):
	#	pass
		#for i in self._tmprows:
		#	self._rows[i.id()] = i
		#j	i.finishRows()
		#self._tmprows = None

	#def content(self):
	#	return DflatIdentifiable.contentStr(self._rows)

	#def contentHeader(self):
	#	return super(DflatRowContainer, self).content()

	def setNode(self, n):
		self._node = n

	def node(self):
		return self._node

	def prev(self):
		return self._prev

	def next(self):
		return self._next

	def rows(self):
		return self._rows
			
	def setPrev(self, child):
		self._prev = child

	def setNext(self, child):
		self._next = child

	def addPrev(self, child):
		self._prev.append(child)

	def addNext(self, child):
		self._next.append(child)

	def addRow(self, row):
		#self._rows[row.id()] = row
		self._rows.append(row)

	#for the caller: catch regex exception!
	def search(self, searchfor, modi, results):
		res = super(DflatRowContainer, self).search(searchfor, modi, results)
		for i in self._rows:
			if i.search(searchfor, modi, results):
				res = True
		return res
	
	#def getRow(self, id):
	#	return self._rows.get(id)

	def __str__(self):
		#return super(DflatDecomposition, self).__str__(self._keys) + str(self._next)
		return super(DflatRowContainer, self).__str__() + "@" #+ str(self.prev()) # + "->" + str(self._next)

class DflatDecomposition(DflatRowContainer):

	def __init__(self, keys):
		super(DflatDecomposition, self).__init__(keys)
		self._ids = {} #temporary ids (memory adresses of some rows
		self._nr = 0

	def setNr(self, nr):	
		self._nr = nr

	def nr(self):
		return self._nr

	def content(self):
		return "n" + str(self._nr) + ": " + super(DflatDecomposition, self).content()

        def getIds(self):
                return self._ids

	def search(self, searchfor, modi, results):
		res = super(DflatDecomposition, self).search(searchfor, modi, results)
                for i in self._next:
                        if i.search(searchfor, modi, results):
                                res = True
                return res

        def clearIds(self):
                self._ids = None
	

class DflatRow(DflatRowContainer):

	_empty = None

	AND_ROW = 1
	OR_ROW = 2
	ACCEPT_ROW = 4
	REJECT_ROW = 8

	FLAG_SIGNS = [(AND_ROW, "&"), (OR_ROW, "|"), (ACCEPT_ROW, "A"), (REJECT_ROW, "R")]

	def __init__(self):
		super(DflatRow, self).__init__([])
		self._cost = 0
		self._flags = 0
		self._aux = {}
		#self._sub = None
		#self._preds = []
	#	self._used = False

	def addAux(self, a):
		self._aux[str(a)] = a

	def auxId(self):
		return DflatIdentifiable.idstr(self._aux.keys())
		
	def content(self):
		return DflatIdentifiable.contentStr(self._keys, lambda x : self._aux.has_key(str(x)))
	
	def auxContent(self):
		v = self._aux.values()
		v.sort()
		return DflatIdentifiable.contentStr(v, lambda _ : False) #DflatIdentifiable.SHOW_ALL)
	
	def setCost(self, c):
		self._cost = int(c)

	def costs(self):
		return self._cost

	def hasNoFlag(self):
		return self._flags == 0
	
	def hasFlag(self, flag):
		return self._flags & flag	

	def setFlag(self, flag):
		self._flags |= flag

	def flagString(self):
		rstr = ""
		for i in DflatRow.FLAG_SIGNS:
			if self.hasFlag(i[0]) > 0:
				if len(rstr) > 0:
					rstr += ", "
				rstr +=	i[1]
		if len(rstr) > 0:
			rstr += ", "
		rstr += "C = " + str(self._cost)
		return rstr

	#def addSub(self, subRow):
	#	self._sub.append(subRow)

	#def addPred(self, pred):
	#	self._preds.append(pred)

	#def isUsed(self):
#		return self._used
#	
#	def setUsed(self):
#		self._used = True
#		return self

	#def addZeroCost(self):
	#	found = False
	#	for i in self._keys:	
	#		if i[0] == "@cost":
	#			found = True
	#	if not found:
	#		self.add(["@cost", "0"])
	#	return self

	#@staticmethod
	#def emptyID():
	#	if DflatRow._empty is None:
	#		DflatRow._empty = DflatRow()
	#	return DflatRow._empty.addZeroCost().id()

#class DflatTmpRow(DflatRow):
#	def __init__(self):
#		super(DflatRow, self).__init__([])
#		#self._sub = None
#		#self._preds = []
#		self._parent = -1
#
#	def setParent(self, v):
#		self._parent = v
#
#	def getParent(self):
#		return self._parent

class DflatGUIRow(DflatRow):
	FLAG_ICONS = [(DflatRow.AND_ROW, "logical_and_u2227_icon.png"), (DflatRow.OR_ROW, "logical_or_u2228_icon.png"), (DflatRow.ACCEPT_ROW, "gtk-apply"), (DflatRow.REJECT_ROW, "gtk-stop")]#"gtk-cancel")]
	#FLAG_ICONS = [(DflatRow.AND_ROW, "logical_and_u2227_icon.png"), (DflatRow.OR_ROW, "logical_and_u2227_icon.png"), (DflatRow.ACCEPT_ROW, "gtk-apply"), (DflatRow.REJECT_ROW, "gtk-stop")]#"gtk-cancel")]
	#FLAG_ICONS = [(DflatRow.AND_ROW, "user-idle"), (DflatRow.OR_ROW, "list-add"), (DflatRow.ACCEPT_ROW, "dialog-ok"), (DflatRow.REJECT_ROW, "dialog-error")]
	
	def flagIcon(self):
		for i in DflatGUIRow.FLAG_ICONS:
			if self.hasFlag(i[0]):
				return i[1]
		return ""

	def __init__(self):
		super(DflatGUIRow, self).__init__()
		self._rownode = None

	def setRowNode(self, node):
		self._rownode = node
	
	def rowNode(self):
		return self._rownode

