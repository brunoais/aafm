import sys
from PyQt4 import QtGui, QtCore
from ListWidget import ListWidget
from TerminalWidget import TerminalWidget

#http://stackoverflow.com/questions/5435891/qt-breadcrumb-navigation
#KUrlNavigator

#http://www.qtcentre.org/archive/index.php/t-15739.html
#https://groups.google.com/forum/#!topic/python_inside_maya/sKzq_l6v5hY
#http://doc.qt.io/qt-4.8/graphicsview.html
#https://forum.qt.io/topic/72252/pixmap-and-text-alignment-in-iconview/4
#http://stackoverflow.com/questions/41107202/pyqt-coloring-part-of-text-in-qlistwidget
#http://pythoncentral.io/pyside-pyqt-tutorial-the-qlistwidget/

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.initUI()

	def initUI(self):               
		self.setGeometry(0, 0, 1024, 768)
		self.setWindowTitle('pwd')
		#------------------------------------------
		# ListWidget
		#------------------------------------------
		self.listWidget = ListWidget()
		#------------------------------------------
		# 
		#------------------------------------------
#		self.model = QtGui.QFileSystemModel()
#		self.model.setRootPath("/home/alex/")
#		self.listWidget.setModel_(self.model)
		#------------------------------------------
		# Actions
		#------------------------------------------
		self.home = QtGui.QAction(QtGui.QIcon("../res/icones/basic_home.svg"), "home", self)
		self.home.triggered.connect(self.listWidget.setPath)

		self.toggleView = QtGui.QAction(QtGui.QIcon("../res/icones/arrows_hamburger 2.svg"), "toggleView", self)
		self.toggleView.triggered.connect(self.listWidget.toggleMode)

		self.exitAction=QtGui.QAction(QtGui.QIcon('../res/icones/arrows_remove.svg'), '&Exit', self)
		self.exitAction.setShortcut('Ctrl+Q')
		self.exitAction.setStatusTip('Exit')
		self.exitAction.triggered.connect(QtGui.qApp.quit)

		self.refreshAction=QtGui.QAction(QtGui.QIcon('../res/icones/arrows_clockwise.svg'), '&Refresh', self)
		self.refreshAction.setShortcut('Ctrl+R')
		self.refreshAction.setStatusTip('Refresh')
		#------------------------------------------
		# Menu Bar
		#------------------------------------------
		self.fileMenu=self.menuBar().addMenu('&File')
#		self.fileMenu.addAction(self.restartAction)
		self.fileMenu.addAction(self.exitAction)

		self.helpMenu=self.menuBar().addMenu('&Help')
		self.helpMenu.addAction("About")
		#------------------------------------------
		# ToolBar
		#------------------------------------------
		self.toolBar = self.addToolBar("File")
		self.toolBar.addAction(self.home)
		self.toolBar.addAction(self.toggleView)
		self.toolBar.addAction(self.refreshAction)
		self.toolBar.addAction(self.exitAction)
		
#		self.toolBar.actionTriggered[QAction].connect(self.toolbtnpressed)
		#------------------------------------------
		# Terminal
		#------------------------------------------
#		self.terminalWidget = TerminalWidget(self)
		#------------------------------------------
		# StatusBar
		#------------------------------------------
		self.statusBar().showMessage("Ready")
		#------------------------------------------
		# Central Widget
		#------------------------------------------
		layout = QtGui.QVBoxLayout()
		layout.setMargin(0)
		layout.addWidget(self.listWidget)
#		layout.addWidget(self.terminalWidget)

		self.centralWidget = QtGui.QWidget()
		self.centralWidget.setLayout(layout)

		self.setCentralWidget(self.centralWidget)

		self.show()

if __name__=="__main__":
	app = QtGui.QApplication(sys.argv) 
	mainWindow = MainWindow()
	sys.exit(app.exec_())
