#!/usr/bin/env python

#import os
#import pygtk
#pygtk.require('2.0')
#import gtk

from DflatGUISearch import *
from DflatDecomposition import *
from DflatGUINode import *
from GUISizeProvider import *

class DflatDebuggerGUI:

	DEF_LAYER_DEPTH = 3

	def delete_event(self, widget, event, data = None):
		#print "delete event occurred"
		return False

	def destroy(self, widget, data=None):
		#print "destroy signal occurred"
		gtk.main_quit()

	#def clicked_cb(self, widget, data=None):
	#	print "clicked toolbutton"
 
	def resize_signal2(self, widget, iter, data=None):
		#print "resize"
		if not self._lock:
			self.resize(self._root, 0, 0)

	#def resize_signal(self, widget, iter, path, data=None):
	#	print "resize"
	#	self.resize(self._root, 0, 0)

	def treeview_ctxtmenu(self, widget, event, data = None):
		#print "press", event
		if event.button == 3:
			self._current_selected = data
			self._selected_rows = self._current_selected.node().getView().get_selection().get_selected_rows() 
			#self.soltree_release(widget, event, data)
			self._popup.popup(None, None, None, event.button, event.time)
		
		#elif event.button == 1:
		#	mdl = widget.get_selection().get_selected()
			#print widget.get_selection().get_selected_rows()[1]
			#print mdl[0].get_value(mdl[1], 1)
		#	elem = mdl[0].get_value(mdl[1], 1)
		#	row = mdl[0].get_value(mdl[1], 2)
			#print elem
			
		self._search.setDecomp(self._root)
		#	for i in elem.next():
		#		sel = i.node().getView().get_selection()
		#		sel.unselect_all()
		#		for j in i.rows():
		#			r = i.rows()[j]
		#			for rs in r.next():
		#				if row is rs:
		#					sel.select_path(rs.node().path)
		#					#print j
		#					break
				
	def refresh_solutions(self, s):
		mdl = self._solutions.get_model()
		mdl.clear()
		anz = 0
		for k in s:
			v = s[k]
			mdl.append(None, [v.content(), v])
			anz += 1
		self._solcol.set_title(str(anz) + " items so far")
		#print "refr"

	def soltree_release(self, widget, event = None, data = None):
		#print "release"
		self._lock = True
		DflatGUINode.unselect(self._root, widget)
		DflatGUINode._button_release(widget, event, data)
		self._lock = False
		self.resize_signal2(None, None, None)
	
	def solview_release(self, widget, event = None, data = None):
		if event is None or event.button == 1:
			#print "solclick"
			self._lock = True
			DflatGUINode.unselect(self._root, None)
			#mdliter = self._solutions.get_selection().get_selected()
			mdliter = widget.get_selection().get_selected()
			if not mdliter[1] is None:
				sol = mdliter[0].get_value(mdliter[1], 1)
				#print sol
				#sol = DflatGUINode.getSol()
				for s in sol.keys():
					v = sol.keys()[s]
					for node in v: #list of specific nodes
						DflatGUINode.select_row(node)
				self._lock = False
				self.resize_signal2(None, None, None)


	def show_dialog(self, widget, dialog = None):
		nam = gtk.Buildable.get_name(widget)
		fpos = nam.find("_")
		if fpos > 0:
			nam = nam[:fpos]
		window = self._builder.get_object("frm" + nam)
		window.show_all()

	def close_dialog2(self, widget, data = None):
		window = self._builder.get_object("fr" + gtk.Buildable.get_name(widget))
		window.hide()

	def close_dialog(self, widget, event, data = None):
		widget.hide()
		#print "close"
		return True

	def _refr(self):
		DflatGUINode.refresh_visible(self._root)

#UNHIDE
	def unhide_all(self, widget, data = None):
		#print "unhide"
		self._blocked = {}
		self._current_selected = None
		self._refr()
#HIDE
	def hide_type(self, widget, data = None):
		#print "hide"
		if not self._current_selected is None:
			mdl = self._selected_rows #multiselection
			for i in mdl[1]:
				m = mdl[0].get_iter(i) #get mdl
				if mdl[0].get_value(m, 0).hasNoFlag():
					self._blocked[0] = True
				else:
					for j in DflatRow.FLAG_SIGNS:
						if mdl[0].get_value(m, 0).hasFlag(j[0]) > 0:
							self._blocked[j[0]] = True
			#				found = True
				#if not found:
				#	self._blocked[0] = True
				
			self._refr()
#EXPAND
	def expand_itree(self, widget, data = None):
		if not self._current_selected is None:
			self._current_selected.node().getView().expand_all()

	def collapse_itree(self, widget, data = None):
		if not self._current_selected is None:
			self._current_selected.node().getView().collapse_all()


	def expand_all(self, widget, data = None):
		DflatGUINode.expand_all(self._root)
		#self.resize_signal2(None, None, None)
#UNEXPAND
	def unexpand_all(self, widget, data = None):
		DflatGUINode.collapse_all(self._root)
		#self.resize_signal2(None, None, None)
	
	def _show(self, widget, up, data = None):
		if data is None:
			data = DflatDebuggerGUI.DEF_LAYER_DEPTH
		if not self._current_selected is None:
			DflatGUINode._expand_all(self._current_selected, True, data, up)
			#if up:
			#	next = self._current_selected.prev()
			#else:
			#	next = self._current_selected.next()
			#for j in next:
			#	if data > 0:
			#		DflatGUINode.expand_all(j)
			#	else:	
			#		DflatGUINode.collapse_all(j)
				#for k in j.rows():
				#	j.getView().collapse_row(k.		
			#self._show(widget, up, data - 1)

	def _reselect(self):
		if not self._current_selected is None:
			mdl = self._selected_rows #multiselection
			for i in mdl[1]:
				DflatGUINode.select_row(mdl[0].get_value(mdl[0].get_iter(i) , 0))
			self.soltree_release(self._current_selected.node().getView(), None, None)

	def show_up(self, widget, data = None):
		self.unexpand_all(widget, data)
		self._show(widget, True, data)
		self._show(widget, False, 1)
		self._reselect()
		#if data is None:
		#	data = DEF_LAYER_DEPTH
		#elif data > 0 and not self._current_selected is None:
		#	for j in self._current_selected.prev():
		#		DflatGUINode.collapse_all(j)
		#		#for k in j.rows():
		#		#	j.getView().collapse_row(k.		
		#	self.show_up(widget, data - 1)
		#	#mdl = self._current_selected.getDecomp()

		#	#node().getView().get_selection().get_selected_rows()
		#	#for i in mdl[1]:
		#	#	m = mdl[0].get_iter(i)

	def show_down(self, widget, data = None):
		self.unexpand_all(widget, data)
		self._show(widget, False, data)
		self._show(widget, True, 1)
		self._reselect()

	def show_back(self, widget, data = None):
		self.unexpand_all(widget, data)
		self._show(widget, False, data)
		self._show(widget, True, DflatDebuggerGUI.DEF_LAYER_DEPTH - 1)
		self._reselect()
	
	def show_forward(self, widget, data = None):
		self.unexpand_all(widget, data)
		self._show(widget, True, data)
		self._show(widget, False, DflatDebuggerGUI.DEF_LAYER_DEPTH - 1)
		self._reselect()

	def visible_func(self, model, iter, filter):
		#print self._blocked
		#print model.get_value(iter, 0)
		#for i in DflatRow.FLAG_SIGNS:
		#	if not self._blocked.get(i[0]) is None and model.get_value(iter, 0).hasFlag(i[0]) > 0:
		#		return False
		if not self._blocked.get(0) is None and model.get_value(iter, 0).hasNoFlag():
			return False
		else:
			for i in DflatRow.FLAG_SIGNS:
				if not self._blocked.get(i[0]) is None and model.get_value(iter, 0).hasFlag(i[0]) > 0:
					return False
			return True
 
	def __init__(self):
		self._root = None
		self._blocked = {}
		self._selected_rows = None
		self._current_selected = None
		self._sp = GUISizeProvider()
		self._lock = False
		self._builder = gtk.Builder()
		self._builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/gui.glade")
		#self._btn = self._builder.get_object("toolbutton1")
		self._drawpane = self._builder.get_object("fixed1")
		self._popup = self._builder.get_object("mnuContext")
		
		self._solutions = self._builder.get_object("treeview1")
		self._solutions.set_model(gtk.TreeStore(str, object))

		self._search = DflatSearchGUI(self._builder, self._solutions, self.solview_release)

		self._builder.connect_signals({"unhide_all" : self.unhide_all, "hide_type": self.hide_type,
						"expand_all" : self.expand_all, "unexpand_all" : self.unexpand_all,
						"show_up" : self.show_up, "show_down" : self.show_down,
						"expand_itree" : self.expand_itree, "unexpand_itree" : self.collapse_itree,
						"show_back" : self.show_back, "show_forward" : self.show_forward,
						#"on_fixed1_button_release_event" : self.clicked_cb,
						#"on_toolbutton1_clicked" : self.clicked_cb,
						"solview_release" : self.solview_release,
						"show_dialog" : self.show_dialog,
						"delete_dialog" : self.close_dialog, 
						"close_dialog2" : self.close_dialog2,
						"destroy_prog" : self.destroy,
						"search_clicked" : self._search.do_search,
						"show_search_result" : self._search.show_results })
		self._solcol = self._builder.get_object("colSol")
		self._window = self._builder.get_object("window1")
		self._window.connect("delete_event", self.delete_event)
		self._window.connect("destroy", self.destroy)
		self._window.show_all()
		self._root = None

	def addElem(self, elem):
		elem.setNode(DflatGUINode().fillWith(elem, self.resize_signal2, self.treeview_ctxtmenu, self.soltree_release, self.refresh_solutions, self.visible_func))
		elem.node().show(self._drawpane)
		#print elem.node(), elem.next()
		for j in elem.next():
			self.addElem(j)	

	def resize(self, elem, w, h):
		sz2 = elem.node().request_size()
		sz2 = (sz2[0] + 5, sz2[1] + 5)
		sz = [0, 0]
		for j in elem.next():
			szc = self.resize(j, w + sz[0], h + sz2[1])
			sz[0] += szc[0]
			sz[1] = max(sz[1], szc[1])
		elem.node().position(max(w, sz[0] / 2 - sz2[0] / 2), h)
		return (max(sz[0], sz2[0]), sz[1] + sz2[1])
	
	def main(self, decomp):
		self._root = decomp#.get("[]")
		self._search.setDecomp(self._root)
		assert (not self._root is None)
		self.addElem(self._root)
		self.resize(self._root, 0, 0)
		gtk.main()

