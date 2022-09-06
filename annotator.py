import os
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import (
    QPixmap
)
from PyQt5.QtWidgets import (
    QDialog,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QGridLayout,
    QMainWindow,
    QStatusBar,
    QWidget,
    QSizePolicy,
    QListWidget,
    QDockWidget
)


class ImageScene(QGraphicsScene):

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        print("Mouse pressed at:", event.scenePos())
        super().mouseMoveEvent(event)


class ImageViewer(QMainWindow):

    def __init__(self, directory):
        super().__init__()
        self.setWindowTitle("annotator")
        # self.setWindowState(Qt.WindowMaximized)

        self.directory = directory

        files = os.listdir(directory)
        self.files = files

        scene = ImageScene()
        pixmap = QPixmap(os.path.join(directory, files[0]))
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        print("Scene rectangle:", scene.sceneRect())
        self.scene = scene

        view = QGraphicsView(scene)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.scale(0.25, 0.25)

        view.setCursor(Qt.CrossCursor)
        self.setCentralWidget(view)

        files_list = QListWidget()
        for filename in files:
            files_list.addItem(filename)
        files_list.setCurrentRow(0)
        files_list.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        dw = QDockWidget("Files")
        dw.setWidget(files_list)
        self.addDockWidget(Qt.RightDockWidgetArea, dw)

        objects_list = QListWidget()
        objects_list.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        dw = QDockWidget("Objects")
        dw.setWidget(objects_list)
        self.addDockWidget(Qt.RightDockWidgetArea, dw)

        self.show()

        files_list.currentRowChanged.connect(self.set_row)

    def set_row(self, row):
        fp = os.path.join(self.directory, self.files[row])
        pixmap = QPixmap(fp)
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.scene.addItem(item)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    viewer = ImageViewer(r"E:\Pictures\Food")
    sys.exit(app.exec())
