#-*- coding:utf-8 -*-

import  sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class TerminalWidget(QWidget):
	def __init__(self, parent):
		QWidget.__init__(self)
#		self.move(300, 300)

		self.process = QProcess(self)
		self.process.start("xterm", ['-into', str(parent.winId())])
