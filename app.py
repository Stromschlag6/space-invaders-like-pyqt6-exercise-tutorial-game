from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt6.QtCore import QRectF, Qt, QTimer, QObject
import sys

class MyRect(QGraphicsRectItem):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.setPos(self.pos().x() - 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Right:
            self.setPos(self.pos().x() + 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Space:
            bullet = Bullet()
            bullet.setPos(player.pos().x(), player.pos().y())
            scene.addItem(bullet)


class Bullet(QGraphicsRectItem, QObject):
    def __init__(self):
        super().__init__()

        self.setRect(0, 0, 5, 15)

        self.timer = QTimer()

        self.timer.timeout.connect(self.move)
        self.timer.start(50)

    def move(self):
        self.setPos(self.pos().x(), self.pos().y() - 10)
        if self.pos().y() < 0 - self.rect().height():
            scene.removeItem(self)


app = QApplication(sys.argv)

scene = QGraphicsScene()

view = QGraphicsView(scene)

rect = QRectF(0, 0, 100, 100)

player = MyRect(rect)

view.setFixedSize(800, 600)
view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

scene.setSceneRect(0, 0, 800, 600)

player.setPos((view.width() - rect.width()) / 2, view.height() - rect.height())
player.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsFocusable)
player.setFocus()

scene.addItem(player)
view.show()

app.exec()