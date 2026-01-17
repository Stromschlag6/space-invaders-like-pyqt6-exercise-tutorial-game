from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView, QGraphicsTextItem
from PyQt6.QtCore import Qt, QTimer, QObject, QUrl
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import random, sys, resources

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
                score.increase()

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
        # TODO Mechanism for losing the game
        if self.pos().y() + self.rect().height() > view.height():
            scene.removeItem(self)
            del self
            health.decrease()
            return
        
        self.setPos(self.pos().x(), self.pos().y() + 5)


class Score(QGraphicsTextItem):
    def __init__(self, parent=None):
        super().__init__()

        self.__score = 0

        self.setPlainText(f"Score: {self.__score}")
        self.setDefaultTextColor(Qt.GlobalColor.blue)
        self.setFont(QFont("times", 16))

    def increase(self):
        self.__score += 1
        self.setPlainText(f"Score: {self.__score}")

    def getScore(self):
        return self.__score
    

class Health(QGraphicsTextItem):
    def __init__(self, parent=None):
        super().__init__()

        self.__score = 3

        self.setPlainText(f"Health: {self.__score}")
        self.setDefaultTextColor(Qt.GlobalColor.red)
        self.setFont(QFont("times", 16))

    def decrease(self):
        self.__score -= 1
        self.setPlainText(f"Health: {self.__score}")

    def getHealth(self):
        return self.__score


app = QApplication(sys.argv)

scene = QGraphicsScene()

view = QGraphicsView(scene)

player = MyRect()

media_player = QMediaPlayer()
audio_output = QAudioOutput()

score = Score()
health = Health()

view.setFixedSize(800, 600)
view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

scene.setSceneRect(0, 0, 800, 600)

player.setPos((view.width() - player.rect().width()) / 2, view.height() - player.rect().height())
player.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsFocusable)
player.setFocus()

health.setPos(health.pos().x(), health.pos().y() + 25)

scene.addItem(player)
scene.addItem(score)
scene.addItem(health)
# TODO background music not repeating itself
media_player.setAudioOutput(audio_output)
media_player.setSource(QUrl("qrc:/space_invader_game/sounds/background_music_test.mp3"))
audio_output.setVolume(50)
media_player.play()

view.show()

app.exec()