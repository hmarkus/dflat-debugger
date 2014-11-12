#!/usr/bin/env python

import os
import pygtk
pygtk.require('2.0')
import gtk
import re

import DflatGUINode
import DflatDecomposition

class DflatGUISolutionContainer:
	def __init__(self, solmdl):
		self._mdl = solmdl

	def search(self, searchfor, modi, results):
		found = False
		iroot = self._mdl.get_iter_root()
		while not iroot is None:
			sol = self._mdl.get_value(iroot, 1)
			if sol.search(searchfor, modi, results):
				found = True
			iroot = self._mdl.iter_next(iroot)
		return found

class DflatSearchGUI:

	@staticmethod
	def rowcontent_only(obj):
		if type(obj) is DflatDecomposition.DflatDecomposition:
			return None
		else:
			return obj.content()

	@staticmethod
	def safe_aux(obj):
		if type(obj) is DflatDecomposition.DflatGUIRow:
			return obj.auxContent()
		else:
			return None

	def show_results(self, widget, event = None, data = None):
		if event is None or event.button == 1:
			if self._auxcol.get_visible(): #search for item/auxitem/all
				DflatGUINode.DflatGUINode.unselect(self._decomp, None)
				mdliter = self._results.get_selection().get_selected()
                        	if not mdliter[1] is None:
                                	sol = mdliter[0].get_value(mdliter[1], 1)
					DflatGUINode.DflatGUINode.select_row(sol) #.rowNode())
			else: #search for solutions
				self._solview_release(widget, event, data)	

	def do_search(self, widget, data = None):
		txt = self._txt.get_text()
		qSearch = txt
		if self._regexp.get_active():
			try:
				qSearch = re.compile(txt)
			except Exception as e:
				dialog = gtk.MessageDialog(self._dialog, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, str(e))
				dialog.run()
				dialog.destroy()
				txt = None
		
		modi = lambda inp : [DflatSearchGUI.rowcontent_only(inp)]
		obj = self._decomp
		content = ([], {})
		self._auxcol.set_visible(True)
		if not txt is None:
			#if self._sols.get_active() or self._items.get_active():
			#	modi = lambda inp : [inp.content()]
			if self._sols.get_active():
				obj = self._solutioncont
				self._auxcol.set_visible(False)
			elif self._aux.get_active():
				modi = lambda inp : [DflatSearchGUI.safe_aux(inp)]
			elif self._all.get_active():
				modi = lambda inp : [DflatSearchGUI.rowcontent_only(inp), DflatSearchGUI.safe_aux(inp)]
			mdl = self._results.get_model()
			mdl.clear()
			obj.search(qSearch, modi, content)
	                self._rescol.set_title(str(len(content[0])) + " results for '" + txt + "'")
			for i in content[0]:
				mdl.append(None, [i.content(), i, DflatSearchGUI.safe_aux(i)])
			self._dialog.hide()
			self._tabs.set_current_page(1)

	def setDecomp(self, decomp):
		self._decomp = decomp

	def __init__(self, builder, solutions, solview_release):
		self._decomp = None
		self._solutions = solutions
		self._solutioncont = DflatGUISolutionContainer(solutions.get_model())
		self._sols = builder.get_object("optSol")
		self._regexp = builder.get_object("chkRegexp")
		self._results = builder.get_object("treeview_search")
		self._rescol = builder.get_object("colResults")
		self._auxcol = builder.get_object("colAux")
		self._results.set_model(gtk.TreeStore(str, object, str))

		self._solview_release = solview_release
	
		self._dialog = builder.get_object("frmsearch")
		self._tabs = builder.get_object("worksection")
		self._txt = builder.get_object("txtSearch")
		self._items = builder.get_object("optItems")
		self._aux = builder.get_object("optAuxItems")
		self._all = builder.get_object("optAllItems")
	
		self._results = builder.get_object("treeview_search")
