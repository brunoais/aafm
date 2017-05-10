from PyQt4 import QtGui, QtCore

class ListWidget(QtGui.QListWidget):
	def __init__(self):
		super(ListWidget, self).__init__()
		self.initUI()

	def initUI(self):               
		self.setViewMode(QtGui.QListView.ListMode)
		self.setIconSize(QtCore.QSize(400, 400))
		self.setResizeMode(QtGui.QListWidget.Adjust);

		item1 = QtGui.QListWidgetItem(QtGui.QIcon("./../res/pics/a.jpg"), "a.jpg")
		item1.text() #hide
		self.addItem(item1)

		item2 = QtGui.QListWidgetItem(QtGui.QIcon("./../res/pics/b.jpg"), "b.jpg")
		item2.icon() #hide
		self.addItem(item2)

		item3 = QtGui.QListWidgetItem(QtGui.QIcon("./../res/pics/c.jpg"), "c.jpg")
		self.addItem(item3)

	def toggleMode(self):
		viewMode = self.viewMode()
		if viewMode == QtGui.QListView.ListMode:
			self.setIconMode()
		elif viewMode == QtGui.QListView.IconMode:
			self.setListMode()

	def setListMode(self):
		self.setViewMode(QtGui.QListView.ListMode)

	def setIconMode(self):
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

