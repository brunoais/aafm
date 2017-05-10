from PyQt4 import QtGui, QtCore

class ListWidget(QtGui.QListWidget):
	def __init__(self):
		super(ListWidget, self).__init__()
		self.iconSize = QtCore.QSize(100, 100)
		self.initUI()

	def initUI(self):               
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

		files=list()
		files.append("./../res/pics/a.jpg")
		files.append("./../res/pics/b.jpg")
		files.append("./../res/pics/c.jpg")

#		item.icon() #hide
#		item.text() #hide

		self.items=list()
		for e in files:
			item = QtGui.QListWidgetItem(QtGui.QIcon(e), e)
			self.items.append(item)

		for e in self.items:
			e.setSizeHint(QtCore.QSize(100, 100))
#			e.setTextAlignment(QtCore.Qt.AlignHCenter)
			e.setTextColor(QtGui.QColor("white"))
		for e in self.items:
			self.addItem(e)

	def toggleMode(self):
		viewMode = self.viewMode()
		if viewMode == QtGui.QListView.ListMode:
			self.setIconMode()
		elif viewMode == QtGui.QListView.IconMode:
			self.setListMode()

	def setListMode(self):
		self.setIconSize(QtCore.QSize(100, 100))
		for e in self.items:
			e.setSizeHint(QtCore.QSize(100, 100))
		self.setViewMode(QtGui.QListView.ListMode)

	def setIconMode(self):
		self.setIconSize(QtCore.QSize(400, 400))
		for e in self.items:
			e.setSizeHint(QtCore.QSize(400, 400))
		self.setViewMode(QtGui.QListView.IconMode)

	def mousePressEvent(self, QMouseEvent):
		pass
#		print QMouseEvent.pos()

	def mouseReleaseEvent(self, QMouseEvent):
		cursor =QtGui.QCursor()
#		print cursor.pos()        

	def wheelEvent(self, event):
		pass
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
