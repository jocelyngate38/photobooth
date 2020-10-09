import xml.etree.ElementTree as ET
import sys
from PyQt5.QtCore import (QUrl, QFile, QFileInfo, QPoint, QRect, QRectF, QSettings, QSize, QPointF,
                          Qt, QTextStream, QThread, pyqtSignal, pyqtSlot, QTimer, QDateTime, QIODevice, QElapsedTimer)

from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QBrush, QPixmap, QPainter, QPen, QColor, QPainterPath, \
                         QDesktopServices, QFontMetrics)
from PyQt5.QtWidgets import (QMenu, QAction, QLabel, QApplication, QMainWindow, QDialog, QProgressBar, QLabel,
                             QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QGroupBox, QComboBox,
                             QSpacerItem, QSizePolicy, QInputDialog)
import os
import glob
import sys

def savePicture( pixmap, path, w, h, format):
	normPath = os.path.normpath(path)
	file = QFile(normPath)
	file.open(QIODevice.WriteOnly)
	if w == 0 or h == 0:
		pixmap.save(file, format)
	else:
		pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation).save(file, format)
	return normPath

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mylist = [f for f in glob.glob("C:/Users/gate/Desktop/captures/*.jpg")]

	for files in mylist:

		# print(files)
		if os.path.isfile(files):

			outPixmap=QPixmap(files)
			painter = QPainter(outPixmap)
			painter.setRenderHint(QPainter.Antialiasing)

			pix = QPixmap("C:/Users/gate/Desktop/captures/lay.png")
			painter.drawPixmap(0, 0, pix)
			#savedPath = savePicture(outPixmap, files, 0, 0, "JPG")
			outPixmap.save(files,"JPG")
			del painter
	sys.exit(1)
