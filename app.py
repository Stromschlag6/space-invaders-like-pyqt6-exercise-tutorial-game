from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt6.QtCore import QRectF, Qt, QTimer, QObject
import random, sys

class MyRect(QGraphicsRectItem, QObject):
    def __init__(self):
        super().__init__()

        self.setRect(0, 0, 100, 100)

        self.timer = QTimer()

        self.timer.timeout.connect(self.spawn)
        self.timer.start(3000)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            if self.pos().x() >= 0:
                self.setPos(self.pos().x() - 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Right:
            if self.pos().x() + self.rect().width() < view.width():
                self.setPos(self.pos().x() + 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Space:
            bullet = Bullet()
            bullet.setPos(player.pos().x(), player.pos().y())
            scene.addItem(bullet)
    
    def spawn(self):
        enemy = Enemy()
        scene.addItem(enemy)


class Bullet(QGraphicsRectItem, QObject):
    def __init__(self):
        super().__init__()

        self.setRect(0, 0, 5, 15)

        self.timer = QTimer()

        self.timer.timeout.connect(self.move)
        self.timer.start(50)

    def move(self):
        self.setPos(self.pos().x(), self.pos().y() - 10)
        if self.collidingItems():
            colliding_item = self.collidingItems()[0]
            if type(colliding_item) is Enemy:
                scene.removeItem(self)
                scene.removeItem(colliding_item)
                del self
                del colliding_item

        elif self.pos().y() < 0 - self.rect().height():
            scene.removeItem(self)
            del self

    
class Enemy(QGraphicsRectItem, QObject):
    def __init__(self):
        super().__init__()

        width = 100

        self.setRect(random.randint(width, view.width() - width), 0, width, 100)

        self.timer = QTimer()

        self.timer.timeout.connect(self.move)
        self.timer.start(250)

    def move(self):
        # Losing the game
        """ if self.pos().y() + self.rect().height() > view.height():
            del player
            print("You lost!") """
        self.setPos(self.pos().x(), self.pos().y() + 5)
        


app = QApplication(sys.argv)

scene = QGraphicsScene()

view = QGraphicsView(scene)

player = MyRect()

view.setFixedSize(800, 600)
view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

scene.setSceneRect(0, 0, 800, 600)

player.setPos((view.width() - player.rect().width()) / 2, view.height() - player.rect().height())
player.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsFocusable)
player.setFocus()

# Spawn enemies

scene.addItem(player)
view.show()

app.exec()