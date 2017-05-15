import os
import glob
from PyQt4 import QtGui, QtCore

class ListWidget(QtGui.QListWidget):
	""" A specialized QListWidget that displays the
        	list of files in a given directory with thumbnails. """

	def __init__(self):
		super(ListWidget, self).__init__()
#		self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
		self.setPath("./../res/pics/")
		self.iconSize = QtCore.QSize(50, 50)
		self.initUI()

	def initUI(self):               
		self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.setSelectionRectVisible(True)
		self.setViewMode(QtGui.QListView.ListMode)
		self.setIconSize(self.iconSize)
		self.setResizeMode(QtGui.QListWidget.Adjust);
		self.setUniformItemSizes(True)
		self.setStyleSheet("""
			QListWidget
			{
	                    background: #444444;
        	        }""")
#			QListView::item:deselected
#			{
#				border: 1px solid black;
#				border-radius: 6px;
#				color: black;
#			}
#			QListView::item:selected
#			{
#				background: white;
#				border: 4px solid blue;
#			}
#			""")

#		files=list()
#		files.append("./../res/pics/a.jpg")
#		files.append("./../res/pics/b.jpg")
#		files.append("./../res/pics/c.jpg")
#		files.append("./../res/pics/d.jpg")
#		files.append("./../res/pics/e.jpg")
#		files.append("./../res/pics/f.jpg")
#		files.append("./../res/pics/g.jpg")
#		files.append("./../res/pics/h.jpg")
#		files.append("./../res/pics/i.jpg")
#		files.append("./../res/pics/j.jpg")
#
##		item.icon() #hide
##		item.text() #hide
#
#		self.items=list()
#		for e in files:
#			item = QtGui.QListWidgetItem(QtGui.QIcon(e), e)
#			self.items.append(item)
#
#		for e in self.items:
#			e.setSizeHint(QtCore.QSize(50, 50))
##			e.setTextAlignment(QtCore.Qt.AlignHCenter)
#			e.setTextColor(QtGui.QColor("white"))
#		for e in self.items:
#			self.addItem(e)

	def toggleMode(self):
		viewMode = self.viewMode()
		if viewMode == QtGui.QListView.ListMode:
			self.setIconMode()
		elif viewMode == QtGui.QListView.IconMode:
			self.setListMode()

	def setListMode(self):
		self.setIconSize(QtCore.QSize(50, 50))
		for e in self.items:
			e.setSizeHint(QtCore.QSize(50, 50))
		self.setViewMode(QtGui.QListView.ListMode)

	def setIconMode(self):
		self.setIconSize(QtCore.QSize(400, 400))
		for e in self.items:
			e.setSizeHint(QtCore.QSize(400, 400))
		self.setViewMode(QtGui.QListView.IconMode)

#	def mousePressEvent(self, QMouseEvent):
#		pass
##		print QMouseEvent.pos()

#	def mouseReleaseEvent(self, QMouseEvent):
#		cursor =QtGui.QCursor()
##		print cursor.pos()        

#	def wheelEvent(self, event):
#		pass
#		print("scrolled")

	def createContextMenu(self):
		menu = QtGui.QMenu(self)
		quitAction = menu.addAction("Refresh")
		quitAction = menu.addAction("Quit")
		return menu

	def contextMenuEvent(self, event):
		menu = self.createContextMenu()
		action = menu.exec_(self.mapToGlobal(event.pos()))
		if action == quitAction:
			qApp.quit()

	def supportedImageExtensions(self):
		""" Get the image file extensions that can be read. """
		formats = QtGui.QImageReader().supportedImageFormats()
		# Convert the QByteArrays to strings
		return [str(fmt) for fmt in formats]

	def _images(self):
		""" Return a list of file-names of all
			supported images in self.path. """

		# Start with an empty list
		images = []

		# Find the matching files for each valid
		# extension and add them to the images list.
		for extension in self.supportedImageExtensions():
			pattern = os.path.join(self.path, '*.%s'%extension)
			images.extend(glob.glob(pattern))
	 
		return images

	def _populate(self):
		""" Fill the list with images from the
		current directory in self.path. """

		# In case we're repopulating, clear the list
		self.clear()

		self.items=list()

		# Create a list item for each image file,
		# setting the text and icon appropriately
		for image in self._images():
			self.createListWidgetItem(image)

	def setPath(self, path):
		""" Set the current image directory and refresh the list. """
		self.path=path
		self._populate()

	def createListWidgetItem(self, path):
		item = QtGui.QListWidgetItem(self)
		item.setText(path)
		item.setIcon(QtGui.QIcon(path))
#		item.setTextAlignment(QtCore.Qt.AlignHCenter)
		item.setTextColor(QtGui.QColor("white"))

		self.addItem(item)
