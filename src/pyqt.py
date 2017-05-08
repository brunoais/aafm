import sys
from PyQt4 import QtGui, QtCore

class ui(QtGui.QWidget):
	def __init__(self):
		super(ui, self).__init__()
		self.initUI()

	def initUI(self):               
		self.setGeometry(0, 0, 1024, 768)
		self.setWindowTitle('pwd')

		self.listWidget = QtGui.QListWidget()
#		self.listWidget.setViewMode(QtGui.QListView.IconMode)
		self.listWidget.setViewMode(QtGui.QListView.ListMode)
		self.listWidget.setIconSize(QtCore.QSize(400, 400))
		self.listWidget.setResizeMode(QtGui.QListWidget.Adjust);

		item1 = QtGui.QListWidgetItem(QtGui.QIcon("./../res/pics/a.jpg"), "a.jpg")
		item1.text() #hide
		self.listWidget.addItem(item1)

		item2 = QtGui.QListWidgetItem(QtGui.QIcon("./../res/pics/b.jpg"), "b.jpg")
		item2.icon() #hide
		self.listWidget.addItem(item2)

		item3 = QtGui.QListWidgetItem(QtGui.QIcon("./../res/pics/c.jpg"), "c.jpg")
		self.listWidget.addItem(item3)

		layout = QtGui.QHBoxLayout()
		layout.setMargin(0)
		layout.addWidget(self.listWidget)
		self.setLayout(layout)

		self.show()

	def wheelEvent(self, event):
		print("scrolled")
		self.listWidget.setViewMode(QtGui.QListView.IconMode)

	def mousePressEvent(self, QMouseEvent):
		print QMouseEvent.pos()
		self.listWidget.setViewMode(QtGui.QListView.IconMode)

	def mouseReleaseEvent(self, QMouseEvent):
		cursor =QtGui.QCursor()
		print cursor.pos()        
		self.listWidget.setViewMode(QtGui.QListView.IconMode)

if __name__=="__main__":
	app = QtGui.QApplication(sys.argv) 
	ui = ui()
	sys.exit(app.exec_())
