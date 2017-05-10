import sys
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

	def setListMode(self):
		self.setViewMode(QtGui.QListView.ListMode)

	def setIconMode(self):
		self.setViewMode(QtGui.QListView.IconMode)

	def mousePressEvent(self, QMouseEvent):
		print QMouseEvent.pos()
		if QMouseEvent.button() == QtCore.Qt.LeftButton :
			self.setListMode()
		if QMouseEvent.button() == QtCore.Qt.RightButton :
			self.setIconMode()

	def mouseReleaseEvent(self, QMouseEvent):
		cursor =QtGui.QCursor()
#		print cursor.pos()        

	def wheelEvent(self, event):
		pass
#		print("scrolled")

class ui(QtGui.QWidget):
	def __init__(self):
		super(ui, self).__init__()
		self.initUI()

	def initUI(self):               
		self.setGeometry(0, 0, 1024, 768)
		self.setWindowTitle('pwd')

		self.listWidget = ListWidget()
		self.statusBar = QtGui.QStatusBar()
		self.statusBar.showMessage("Ready")

		self.toolBar = QtGui.QToolBar("File")
		
		new = QtGui.QAction(QtGui.QIcon("new.bmp"),"new",self)
		self.toolBar.addAction(new)
		
#		self.toolBar.actionTriggered[QAction].connect(self.toolbtnpressed)

		layout = QtGui.QVBoxLayout()
		layout.setMargin(0)
		layout.addWidget(self.toolBar)
		layout.addWidget(self.listWidget)
		layout.addWidget(self.statusBar)
		self.setLayout(layout)

		self.show()

if __name__=="__main__":
	app = QtGui.QApplication(sys.argv) 
	ui = ui()
	sys.exit(app.exec_())
