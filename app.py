from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt6.QtCore import QRectF, Qt
import sys

class MyRect(QGraphicsRectItem):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.pos().x() - 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Right:
            self.setPos(self.pos().x() + 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Up:
            self.setPos(self.pos().x(), self.pos().y() + 10)
        
        elif event.key() == Qt.Key.Key_Down:
            self.setPos(self.pos().x(), self.pos().y() - 10)
            

app = QApplication(sys.argv)

scene = QGraphicsScene()

rect = QRectF(0, 1, 200, 200)

rect_done = MyRect(rect)

scene.addItem(rect_done)

rect_done.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsFocusable)
rect_done.setFocus()

view = QGraphicsView(scene)
view.show()

app.exec()