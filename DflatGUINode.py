#!/usr/bin/env python

import os
import pygtk
pygtk.require('2.0')
import gtk
from DflatDecomposition import *

class DflatGUINode:

	_sols = []
	_refr_solution = None
	_coltypes = [object, str, str, str, str] #, object, object]
	_colnames = ["atoms", "auxitems", "type", "costs"]
	_startcol = 0
		
	def __init__(self):
		self._decelem = None
		self._treestore = None
		self._treeview = None
		self._pane = None
		self._columns = []
		
        	self._cellr = [] #gtk.CellRendererText()

	def request_size(self):
		return self._treeview.size_request()

	def position(self, x, y):
		self._par.move(self._pane, x, y)

	def show(self, parent):
		#self._treeview.show()
		parent.add(self._pane)
		self._pane.add(self._treeview)
		self._pane.show_all()
		self._par = parent

	def getView(self):
		return self._treeview

	def getDecElem(self):
		return self._decelem

	@staticmethod
	def getSol():
		return DflatGUINode._sols

	@staticmethod
        def _button_release(widget, event = None, data = None):
                #print "press", event
                #if event.button == 1:
                        mdl = widget.get_selection().get_selected_rows()
			elem = None
                        #print widget.get_selection().get_selected_rows()[1]
                        #print mdl[0].get_value(mdl[1], 1)
                        #rows = mdl[0].get_value(mdl[1], 2)
			DflatGUINode._sols = []
			for i in mdl[1]:
				#print i
				it = mdl[0].get_iter(i)
				row = mdl[0].get_value(it, 0)
				if elem is None: # first run
                        		elem = row.node().getDecElem()
					#getView() mdl[0].get_value(it, 1)
			#		DflatGUINode._unselect(elem, True)
			#		DflatGUINode.unselect(elem, False)
				
				s = DflatSolution(None)
				s.add(row)
				DflatGUINode._sols.append(s)
				DflatGUINode._select(elem, row, s)
			sols = {}
			for i in DflatGUINode._sols:
				sols[i.id()] = i
			DflatGUINode._sols = sols
			DflatGUINode._refr_solution(sols)
			#for j in sols:
			#	print j
                        #print elem
			
                        #mdl = widget.get_selection().get_selected_rows()
			#DflatGUINode._select(elem, row)

	@staticmethod
	def _expand_all(k, expand, counter, rev = False):
		#v = k.node().getView()
		if expand and (counter is None or counter > 0):
			k.node().getView().expand_all()
			if not counter is None:
				counter -= 1
		else:
			k.node().getView().collapse_all()
		#for i in k.rows():
		#	v.expand_row(k.rows()[i].rowNode().get_path(), True)
		if rev:
			b = k.prev()
		else:
			b = k.next()
		for i in b:
			DflatGUINode._expand_all(i, expand, counter, rev)
	
	@staticmethod
	def expand_all(k, rev = False):
		DflatGUINode._expand_all(k, True, None, rev)

	@staticmethod
	def collapse_all(k, rev = False):
		DflatGUINode._expand_all(k, False, None, rev)

	@staticmethod
	def refresh_visible(row):
		row.node().getView().get_model().refilter()
		for i in row.next():
			#i.node().getView().get_model().refilter()
			DflatGUINode.refresh_visible(i)

	@staticmethod
	def select_row(k):
		p = k.rowNode().get_path()
		#expand parent nodes
		for e in range(1, len(p)):
			k.node().getView().expand_row(p[:e], False)
		k.node().getView().get_selection().select_path(p)
				

#	@staticmethod
#	def select_solution():
#		sol = DflatGUINode._sols
#		for s in sol:
#			DflatGUINode.select_row(s)
	
	@staticmethod
	def _select(elem, row, sin):	
		#for i in elem.next():
			#sel = i.node().getView().get_selection()
		ss = [sin]
		for j in range(1, len(row.prev())): #first solution already set!
			ss.append(DflatSolution(sin))
			DflatGUINode._sols.append(ss[-1])
		for i in range(0, len(row.prev())):
			j = row.prev()[i]
			s = ss[i] #DflatSolution(sin)
			#DflatGUINode._sols.append(s)
			for k in j:
				#print k, type(k)
				s.add(k)
				DflatGUINode.select_row(k)
				#if type(elem) is DflatRow:
				#	k.node()[0].get_select().select_path(elem.node()[1].get_path())
				DflatGUINode._select(elem, k, s)	
			#for j in i.rows():
			#	r = i.rows()[j]
			#	for rs in r.next():
			#		if row is rs:
			#			#sel.select_path(r.node().path)
			#			sel.select_path(r.node().get_path())
			#			#sel.select_iter(r.node())
			#			#print i, r.node().get_path()
			#			DflatGUINode._select(i, r)
 
	@staticmethod
	def unselect(elem, exclude): #, down):
		#if down:
	#		sub = elem.next()
		#else:
		#	sub = elem.prev()
	
		if not elem.node().getView() is exclude:	
			elem.node().getView().get_selection().unselect_all()
		for i in elem.next(): # sub: #elem.prev():
			#i.node()[0].getView().get_selection().unselect_all()
			#print i, i.node()
			#if not i.node().getView() is exclude:
			#	i.node().getView().get_selection().unselect_all()
			DflatGUINode.unselect(i, exclude)
			
	#@staticmethod	
	#def visible_func(model, iter, filter):
		#print model.get_value(iter, 0)
		#if model.get_value(iter, 0).hasFlag(DflatRow.REJECT_ROW) == 0:
	#		return True
		#return False


	def fillWith(self, decelem, resize, context_menu, calc_solutions, refresh_solutions, visible_func):
		self._treestore = gtk.TreeStore(*DflatGUINode._coltypes)
		self._treefilter = self._treestore.filter_new()
		#self._treefilter.set_visible_column(1)
		self._pane = gtk.Fixed()
		self._treeview = gtk.TreeView(self._treefilter)#_treestore)#_treefilter)
		self._treeview.set_reorderable(False)
		self._pane.set_border_width(20)
		self._treeview.set_border_width(20)
		#self._treeview.set_border_height(20)
		self._treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
		self._treeview.connect("size-allocate", resize, None) #"row-expanded", resize, None)
		self._treeview.connect("button_press_event", context_menu, decelem)
		DflatGUINode._refr_solution = refresh_solutions
		self._treeview.connect("button_release_event", calc_solutions, decelem)
		self._treeview.connect("cursor-changed", calc_solutions, decelem)
		j = 1
		DflatGUINode._colnames[0] = decelem.content()
		for i in DflatGUINode._colnames:
			#if self._currcolumns[j] == True:
			if j == len(DflatGUINode._colnames) - 1:
				self._cellr.append(gtk.CellRendererPixbuf())
			else:
				self._cellr.append(gtk.CellRendererText())
			self._columns.append(gtk.TreeViewColumn(i))
			self._treeview.append_column(self._columns[-1])
			self._columns[-1].pack_start(self._cellr[-1], True)
			#sort
			#self._columns[-1].set_sort_column_id(j)
			if j != 1 + DflatGUINode._startcol:
				self._columns[-1].set_visible(False)
			if j == len(DflatGUINode._colnames) - 1:
				self._columns[-1].add_attribute(self._cellr[-1], "stock-id", j)
				#self._columns[-1].add_attribute(self._cellr[-1], "gicon", j)
				#self._columns[-1].add_attribute(self._cellr[-1], "pixbuf", j)
			else:
				self._columns[-1].add_attribute(self._cellr[-1], "text", j)
			j = j + 1
		#for j in decelem.rows():
		self._decelem = decelem
		self._fillRow(None, decelem)
		self._treefilter.set_visible_func(visible_func, self._treefilter)
		return self

	def _fillRow(self, parent, elem):
		#print "filling", elem
		#for j in elem.rows():
		for r in elem.rows():
			#r = elem.rows()[j]
			if len(r.auxId()) > 2:
				self._columns[1 + DflatGUINode._startcol].set_visible(True)
			if len(r.flagIcon()) > 0:
				self._columns[2 + DflatGUINode._startcol].set_visible(True)
			if r.costs() > 0:
				#print r.costs()
				self._columns[3 + DflatGUINode._startcol].set_visible(True)

			#ic =gtk.StatusIcon()
			#ic.set_from_file(r.flagIcon())
			#piter = self._treestore.append(parent, [r, r.content(), r.auxContent(), gtk.from_file(r.flagIcon()), r.costs()])
			#piter = self._treestore.append(parent, [r, r.content(), r.auxContent(), ic.get_gicon(), r.costs()])
			#icon = None
			#pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("gnome-image.png", 64, 128, False)#
			if r.flagIcon().endswith("png"):
			#	icon = gtk.gdk.pixbuf_new_from_file(r.flagIcon())
				#icon = gtk.image_new_from_file(r.flagIcon())
				try:
					stock_ids = gtk.stock_list_ids()
					if r.flagIcon() not in stock_ids:
						factory = gtk.IconFactory()
						pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.dirname(os.path.realpath(__file__)) + "/" + r.flagIcon())
						iconset = gtk.IconSet(pixbuf)
						factory.add(r.flagIcon(), iconset)
						factory.add_default()
				except Exception:
					pass
		#	else:
			#	icon = self.getView().render_icon(r.flagIcon(), gtk.ICON_SIZE_MENU)
				#icon = gtk.image_new_from_stock(r.flagIcon(), gtk.ICON_SIZE_MENU)
			#print r.flagIcon(), icon
			#print icon.get_gicon()
			#print icon.get_pixbuf()
			piter = self._treestore.append(parent, [r, r.content(), r.auxContent(), r.flagIcon(), r.costs()])
			#piter = self._treestore.append(parent, [r, r.content(), r.auxContent(), icon.get_gicon(), r.costs()])
			#piter = self._treestore.append(parent, [r, r.content(), r.auxContent(), icon.get_pixbuf(), r.costs()])
			#piter = self._treestore.append(parent, [r, r.content(), r.auxContent(), icon, r.costs()])
			#print self._treestore[self._treestore.get_path()]
			#r.setNode(self._treestore[-1])
			#r.setNode(piter)
		
			#provide treeview + rowreference within the row (as guinode)
			r.setNode(self)
			r.setRowNode(gtk.TreeRowReference(self._treestore, self._treestore.get_path(piter)))
			self._fillRow(piter, r)

