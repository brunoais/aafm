#!/usr/bin/env python2

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import os
import shutil
import socket
import datetime
import stat
import pwd
import grp
#import urllib

if os.name == 'nt':
	import win32api
	import win32con
	import win32security

from TreeViewFile import TreeViewFile

class gui:
	QUEUE_ACTION_CALLABLE = 'callable'
	QUEUE_ACTION_MOVE_IN_HOST = 'move_in_host'

	# These constants are for dragging files to Nautilus
	XDS_ATOM = gtk.gdk.atom_intern("XdndDirectSave0")
	TEXT_ATOM = gtk.gdk.atom_intern("text/plain")
	XDS_FILENAME = 'whatever.txt'

	def __init__(self):
		self.queue = []

		self.hostName = socket.gethostname()
		self.basedir = os.path.dirname(os.path.abspath(__file__))
		self.showHidden = True # Show hidden files and folders
		
		if os.name == 'nt':
			self.get_owner = self._get_owner_windows
			self.get_group = self._get_group_windows
		else:
			self.get_owner = self._get_owner
			self.get_group = self._get_group

		self.init_ui()

	def init_ui(self):
		# Build main window
		self.window=gtk.Window()
		self.window.set_title("File Manager")
		self.window.set_size_request(640, 480)
		self.window.connect('key_press_event', self.on_key_press)

		# Resources
		imageDir = gtk.Image()
		imageDir.set_from_file(os.path.join(self.basedir, './data/icons/folder.png'))
		imageFile = gtk.Image()
		imageFile.set_from_file(os.path.join(self.basedir, './data/icons/file.png'))

		# menu bar
		self.menubar = gtk.MenuBar()
		
		# File menu
		filemenu = gtk.Menu()
		filem = gtk.MenuItem("File")
		filem.set_submenu(filemenu)
		
		exit = gtk.MenuItem("Exit")
		exit.connect("activate", gtk.main_quit)
		filemenu.append(exit)
		
		self.menubar.append(filem)

		# View menu
		viewmenu = gtk.Menu()
		viewm = gtk.MenuItem("View")
		viewm.set_submenu(viewmenu)
		
		showhidden = gtk.CheckMenuItem("showHidden")
        	showhidden .set_active(True)
		showhidden.connect('toggled', self.on_toggle_hidden)
		viewmenu.append(showhidden)

		refreshview = gtk.MenuItem("Refresh")
		refreshview.connect('activate', self.refresh_host_files)
		viewmenu.append(refreshview)

		stat = gtk.CheckMenuItem("View Menubar")
		stat.set_active(True)
		stat.connect("activate", self.on_menubar_view)
		viewmenu.append(stat)

		stat = gtk.CheckMenuItem("View Toolbar")
		stat.set_active(True)
		stat.connect("activate", self.on_toolbar_view)
		viewmenu.append(stat)

		stat = gtk.CheckMenuItem("View Statusbar")
		stat.set_active(True)
		stat.connect("activate", self.on_status_view)
		viewmenu.append(stat)
		
		self.menubar.append(viewm)
		
		# Toolbar
		self.toolbar = gtk.Toolbar()
		self.toolbar.set_style(gtk.TOOLBAR_ICONS)
		
		newtb = gtk.ToolButton(gtk.STOCK_NEW)
		opentb = gtk.ToolButton(gtk.STOCK_OPEN)
		savetb = gtk.ToolButton(gtk.STOCK_SAVE)
		sep = gtk.SeparatorToolItem()
		quittb = gtk.ToolButton(gtk.STOCK_QUIT)
		
		self.toolbar.insert(newtb, 0)
		self.toolbar.insert(opentb, 1)
		self.toolbar.insert(savetb, 2)
		self.toolbar.insert(sep, 3)
		self.toolbar.insert(quittb, 4)
		
		quittb.connect("clicked", gtk.main_quit)

		# TreeView
		self.host_treeViewFile = TreeViewFile(imageDir.get_pixbuf(), imageFile.get_pixbuf())
		hostTree = self.host_treeViewFile.get_tree()
		hostTree.connect('row-activated', self.host_navigate_callback)
		hostTree.connect('button_press_event', self.on_host_tree_view_contextual_menu)
	
		host_targets = [
			('DRAG_SELF', gtk.TARGET_SAME_WIDGET, 0),
			('ADB_text', 0, 1),
			('text/plain', 0, 2)
		]

		hostTree.enable_model_drag_dest(
			host_targets,
			gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE
		)
		hostTree.connect('drag-data-received', self.on_host_drag_data_received)

		hostTree.enable_model_drag_source(
			gtk.gdk.BUTTON1_MASK,
			host_targets,
			gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE
		)
		hostTree.connect('drag_data_get', self.on_host_drag_data_get)
		
		# Progress bar
		self.progress_bar = gtk.ProgressBar()

		# Text Entry
		self.entry = gtk.Entry()

		# status bar
		self.statusbar = gtk.Statusbar()
        	self.statusbar.push(1, "Ready")

		# layout
		vbox = gtk.VBox(False, 2)
		vbox.pack_start(self.menubar, False, False, 0)
		vbox.pack_start(self.toolbar, False, False, 0)
		vbox.pack_start(self.host_treeViewFile.get_view(), True, True, 0)
		vbox.pack_start(self.progress_bar, False, False, 0)
		vbox.pack_start(self.entry, False, False, 0)
		vbox.pack_start(self.statusbar, False, False, 0)
		
		self.window.add(vbox)

		# Some more subtle details...
		self.host_cwd = os.getcwd()

		self.refresh_host_files()

		# And we're done!
		self.window.connect("destroy", gtk.main_quit)
		self.window.show_all()

            	self.progress_bar.hide()
            	self.entry.hide()

	def host_navigate_callback(self, widget, path, view_column):
		row = path[0]
		model = widget.get_model()
		iter = model.get_iter(row)
		is_dir = model.get_value(iter, 0)
		name = model.get_value(iter, 1)

		if is_dir:
			self.host_cwd = os.path.normpath(os.path.join(self.host_cwd, name))
			self.refresh_host_files()

	def refresh_host_files(self, widget=None):
		self.host_treeViewFile.load_data(self.dir_scan_host(self.host_cwd))
		self.window.set_title("%s:%s" % (self.hostName, self.host_cwd))

	def get_treeviewfile_selected(self, treeviewfile):
		values = []
		model, rows = treeviewfile.get_tree().get_selection().get_selected_rows()

		for row in rows:
			iter = model.get_iter(row)
			filename = model.get_value(iter, 1)
			is_directory = model.get_value(iter, 0)
			values.append({'filename': filename, 'is_directory': is_directory})

		return values

	def get_host_selected_files(self):
		return self.get_treeviewfile_selected(self.host_treeViewFile)

	""" Walks through a directory and return the data in a tree-style list 
		that can be used by the TreeViewFile """
	def dir_scan_host(self, directory):
		output = []

		root, dirs, files = next(os.walk(directory))

		if not self.showHidden:
			files = [f for f in files if not f[0] == '.']
			dirs = [d for d in dirs if not d[0] == '.']

		dirs.sort()
		files.sort()

		output.append({'directory': True, 'name': '..', 'size': 0, 'timestamp': '',
				'permissions': '',
				'owner': '',
				'group': ''})

		for d in dirs:
			path = os.path.join(directory, d)
			output.append({
				'directory': True,
				'name': d,
				'size': 0,
				'timestamp': self.format_timestamp(os.path.getmtime(path)),
				'permissions': self.get_permissions(path),
				'owner': self.get_owner(path),
				'group': self.get_group(path)
			})

		for f in files:
			path = os.path.join(directory, f)

			try:
				size = os.path.getsize(path)
				output.append({
					'directory': False,
					'name': f,
					'size': size,
					'timestamp': self.format_timestamp(os.path.getmtime(path)),
					'permissions': self.get_permissions(path),
					'owner': self.get_owner(path),
					'group': self.get_group(path)
				})
			except OSError:
				pass

		return output

	""" The following three methods are probably NOT the best way of doing things.
	At least according to all the warnings that say os.stat is very costly
	and should be cached."""
	def get_permissions(self, filename):
		st = os.stat(filename)
		mode = st.st_mode
		permissions = ''

		bits = [ 
			stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
			stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
			stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH
		]

		attrs = ['r', 'w', 'x']

		for i in range(0, len(bits)):
			bit = bits[i]
			attr = attrs[i % len(attrs)]

			if bit & mode:
				permissions += attr
			else:
				permissions += '-'

		return permissions

	def _get_owner(self, filename):
		st = os.stat(filename)
		uid = st.st_uid
		try:
			user = pwd.getpwuid(uid)[0]
		except KeyError:
			print ('unknown uid %d for file %s' % (uid, filename))
			user = 'unknown'
		return user
		
	def _get_owner_windows(self, filename):
		sd = win32security.GetFileSecurity(filename, win32security.OWNER_SECURITY_INFORMATION)
		owner_sid = sd.GetSecurityDescriptorOwner()
		name, domain, type = win32security.LookupAccountSid(None, owner_sid)
		return name

	def _get_group(self, filename):
		st = os.stat(filename)
		gid = st.st_gid
		try:
			groupname = grp.getgrgid(gid)[0]
		except KeyError:
			print ('unknown gid %d for file %s' % (gid, filename))
			groupname = 'unknown'
		return groupname
	
	def _get_group_windows(self, filename):
		return ""

	def format_timestamp(self, timestamp):
		d = datetime.datetime.fromtimestamp(timestamp)
		return d.strftime(r'%Y-%m-%d %H:%M')

	def on_toggle_hidden(self, widget):
		self.showHidden = widget.get_active()
		self.refresh_host_files()

	def create_context_menu(self):
		context_menu = gtk.Menu()

		menuHostCreateDirectory = gtk.MenuItem("Create directory...")
		menuHostCreateDirectory.connect("activate", self.on_host_create_directory_callback)
		menuHostCreateDirectory.show()

		menuHostRefresh = gtk.MenuItem("Refresh")
		menuHostRefresh.connect("activate", self.on_host_refresh_callback)
		menuHostRefresh.show()

		menuHostDeleteItem = gtk.MenuItem("Delete...")
		menuHostDeleteItem.connect("activate", self.on_host_delete_item_callback)
		menuHostDeleteItem.show()

		menuHostRenameItem = gtk.MenuItem("Rename...")
		menuHostRenameItem.connect("activate", self.on_host_rename_item_callback)
		menuHostRenameItem.show()

		sep = gtk.SeparatorMenuItem()
		sep.show()

		context_menu.append(menuHostCreateDirectory)
		context_menu.append(sep)
		context_menu.append(menuHostRefresh)
		context_menu.append(menuHostDeleteItem)
		context_menu.append(menuHostRenameItem)

		# Greyout unavailable options
		num_selected = len(self.get_host_selected_files())
		has_selection = num_selected > 0

		menuHostDeleteItem.set_sensitive(has_selection)
		menuHostRenameItem.set_sensitive(num_selected == 1)	

		return context_menu
	
	def on_host_tree_view_contextual_menu(self, widget, event):
		if event.button == 3: # Right click
			context_menu=self.create_context_menu()
			context_menu.popup(None, None, None, event.button, event.time)
			return True
		
		# Not consuming the event
		return False

	# Create host directory
	def on_host_create_directory_callback(self, widget):
		directory_name = self.dialog_get_directory_name()

		if directory_name is None:
			return

		full_path = os.path.join(self.host_cwd, directory_name)
		if not os.path.exists(full_path):
			os.mkdir(full_path)
			self.refresh_host_files()

	def on_host_refresh_callback(self, widget):
		self.refresh_host_files()

	def on_host_delete_item_callback(self, widget):
		selected = self.get_host_selected_files()
		items = []
		for item in selected:
			items.append(item['filename'])
			
		result = self.dialog_delete_confirmation(items)

		if result == gtk.RESPONSE_OK:
			for item in items:
				full_item_path = os.path.join(self.host_cwd, item)
				self.delete_item(full_item_path)
				self.refresh_host_files()

	def delete_item(self, path):
		if os.path.isfile(path):
			os.remove(path)
		else:
			shutil.rmtree(path)

	def on_host_rename_item_callback(self, widget):
		old_name = self.get_host_selected_files()[0]['filename']
		new_name = self.dialog_get_item_name(old_name)

		if new_name is None:
			return

		full_src_path = os.path.join(self.host_cwd, old_name)
		full_dst_path = os.path.join(self.host_cwd, new_name)

		shutil.move(full_src_path, full_dst_path)
		self.refresh_host_files()

	def dialog_delete_confirmation(self, items):
		items.sort()
		joined = ', '.join(items)
		dialog = gtk.MessageDialog(
			parent = None,
			flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			type = gtk.MESSAGE_QUESTION,
			buttons = gtk.BUTTONS_OK_CANCEL,
			message_format = "Are you sure you want to delete %d items?" % len(items)
		)
		dialog.format_secondary_markup('%s will be deleted. This action cannot be undone.' % joined)
		dialog.show_all()
		result = dialog.run()
		
		dialog.destroy()
		return result

	def dialog_get_directory_name(self):
		dialog = gtk.MessageDialog(
			None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			gtk.MESSAGE_QUESTION,
			gtk.BUTTONS_OK_CANCEL,
			None)

		dialog.set_markup('Please enter new directory name:')

		entry = gtk.Entry()
		entry.connect('activate', self.dialog_response, dialog, gtk.RESPONSE_OK)

		hbox = gtk.HBox()
		hbox.pack_start(gtk.Label('Name:'), False, 5, 5)
		hbox.pack_end(entry)

		dialog.vbox.pack_end(hbox, True, True, 0)
		dialog.show_all()

		result = dialog.run()

		text = entry.get_text()
		dialog.destroy()

		if result == gtk.RESPONSE_OK:
			return text
		else:
			return None

	def dialog_response(self, entry, dialog, response):
		dialog.response(response)

	def dialog_get_item_name(self, old_name):
		dialog = gtk.MessageDialog(
			None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			gtk.MESSAGE_QUESTION,
			gtk.BUTTONS_OK_CANCEL,
			None)

		dialog.set_markup('Please enter new name:')

		entry = gtk.Entry()
		entry.connect('activate', self.dialog_response, dialog, gtk.RESPONSE_OK)
		entry.set_text(old_name)

		hbox = gtk.HBox()
		hbox.pack_start(gtk.Label('Name:'), False, 5, 5)
		hbox.pack_end(entry)

		dialog.vbox.pack_end(hbox, True, True, 0)
		dialog.show_all()

		result = dialog.run()
		text = entry.get_text()
		dialog.destroy()
		
		if result == gtk.RESPONSE_OK:
			return text
		else:
			return None

	def update_progress(self, value = None):
		if value is None:
			self.progress_bar.set_fraction(0)
			self.progress_bar.set_text("Ready")
			self.progress_bar.pulse()
		else:
			self.progress_bar.set_fraction(value)

			self.progress_bar.set_text("%d%%" % (value * 100))

		if value >= 1:
			self.progress_bar.set_text("Done")
			self.progress_bar.set_fraction(0)

		# Make sure the GUI has some cycles for processing events
		while gtk.events_pending():
			gtk.main_iteration(False)

	def on_minibuffer_view(self, widget):
		if widget.active: 
			self.entry.show()
		else:
			self.entry.hide()

	def on_menubar_view(self, widget):
		if widget.active: 
			self.menubar.show()
		else:
			self.menubar.hide()

	def on_toolbar_view(self, widget):
		if widget.active: 
			self.toolbar.show()
		else:
			self.toolbar.hide()

	def on_status_view(self, widget):
		if widget.active: 
			self.statusbar.show()
		else:
			self.statusbar.hide()

	def on_host_drag_data_get(self, widget, context, selection, target_type, time):
		data = '\n'.join(['file://' + urllib.quote(os.path.join(self.host_cwd, item['filename'])) for item in self.get_host_selected_files()])
		
		selection.set(selection.target, 8, data)

	def on_host_drag_data_received(self, tree_view, context, x, y, selection, info, timestamp):
		data = selection.data
		type = selection.type
		drop_info = tree_view.get_dest_row_at_pos(x, y)
		destination = self.host_cwd
		
		if drop_info:
			model = tree_view.get_model()
			path, position = drop_info
			
			if position in [ gtk.TREE_VIEW_DROP_INTO_OR_BEFORE, gtk.TREE_VIEW_DROP_INTO_OR_AFTER ]:
				iter = model.get_iter(path)
				is_directory = model.get_value(iter, 0)
				name = model.get_value(iter, 1)

				# If dropping over a folder, copy things to that folder
				if is_directory:
					destination = os.path.join(self.host_cwd, name)

		for line in [line.strip() for line in data.split('\n')]:
			if line.startswith('file://'):
				source = urllib.unquote(line.replace('file://', '', 1))

				if type == 'DRAG_SELF':
					self.add_to_queue(self.QUEUE_ACTION_MOVE_IN_HOST, source, destination)
				elif type == 'ADB_text':
					self.add_to_queue(self.QUEUE_ACTION_COPY_FROM_DEVICE, source, destination)

		self.process_queue()

	def add_to_queue(self, action, src_file, dst_path):
		self.queue.append([action, src_file, dst_path])
	
	def process_queue(self):
		task = self.process_queue_task()
		gobject.idle_add(task.next)

	def on_key_press(self, widget, event):
		keyname = gtk.gdk.keyval_name(event.keyval)
#		print "Key %s (%d) was pressed" % (keyname, event.keyval)
		if(event.keyval==58): #:
			self.entry.show()
			self.statusbar.hide()
			self.entry.grab_focus() 
		elif(event.keyval==65307): #ESC
			self.entry.hide()
			self.statusbar.show()
			self.host_treeViewFile.get_view().grab_focus() 
		elif(event.keyval==65293): #Return
			self.cmd=self.entry.get_text()

			if(self.cmd[:4]==":cd "):
				self.host_cwd = self.cmd[4:]
				if(self.host_cwd==""):
					self.host_cwd="/home/alex/"
				self.refresh_host_files()

			#FIXME send event ESC
			self.entry.hide()
			self.statusbar.show()
			self.host_treeViewFile.get_view().grab_focus() 
				
	def process_queue_task(self):
		completed = 0
		self.update_progress()

		while len(self.queue) > 0:
			item = self.queue.pop(0)
			action, src, dst = item

			if action == self.QUEUE_ACTION_CALLABLE:
				src(*dst)
			elif action == self.QUEUE_ACTION_MOVE_IN_HOST:
				shutil.move(src, dst)
				self.refresh_host_files()

			completed += 1
			self.update_progress(float(completed) / float(completed + len(self.queue)))

			yield True

		yield False

	def die_callback(self, widget, data=None):
		self.destroy(widget, data)

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def main(self):
		gtk.main()

if __name__ == '__main__':
	gui = gui()
	gui.main()
