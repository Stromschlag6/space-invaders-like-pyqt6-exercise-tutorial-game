from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt6.QtCore import QRectF, Qt, QTimer, QObject
import sys

class MyRect(QGraphicsRectItem):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.pos().x() - 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Right:
            self.setPos(self.pos().x() + 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Up:
            self.setPos(self.pos().x(), self.pos().y() - 10)
        
        elif event.key() == Qt.Key.Key_Down:
            self.setPos(self.pos().x(), self.pos().y() + 10)
        
        elif event.key() == Qt.Key.Key_Space:
            bullet = Bullet()
            bullet.setPos(rect_done.pos().x(), rect_done.pos().y())
            scene.addItem(bullet)


class Bullet(QGraphicsRectItem, QObject):
    def __init__(self):
        super().__init__()

        self.setRect(0, 0, 5, 15)

        self.timer = QTimer()

        self.timer.timeout.connect(self.move)
        self.timer.start(50)

        print("I happen")

    def move(self):
        self.setPos(self.pos().x(), self.pos().y() - 10)


app = QApplication(sys.argv)

scene = QGraphicsScene()

rect = QRectF(0, 0, 100, 100)

rect_done = MyRect(rect)

scene.addItem(rect_done)

rect_done.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsFocusable)
rect_done.setFocus()

view = QGraphicsView(scene)
view.setVerticalScrollBar(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
view.show()

app.exec()