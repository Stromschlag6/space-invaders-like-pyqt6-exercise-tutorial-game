from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView, QGraphicsTextItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QTimer, QObject, QUrl
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import random, sys, resources

class Player(QGraphicsRectItem, QObject):
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
            bullet.bang()
            bullet.setPos(player.pos().x(), player.pos().y())
            print(bullet.pixmap().isNull())
            scene.addItem(bullet)
    
    def spawn(self):
        enemy = Enemy()
        scene.addItem(enemy)


class Bullet(QGraphicsPixmapItem, QObject):
    def __init__(self):
        super().__init__()

        self.setPixmap(QPixmap(":/images/images/tank_shell.png").scaled(17, 50, Qt.AspectRatioMode.KeepAspectRatio))

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.timer = QTimer()

        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl("qrc:/sounds/sounds/bullet_sound_test.mp3"))
        self.audio_output.setVolume(50)

        self.timer.timeout.connect(self.move)
        self.timer.start(50)

    def move(self):
        self.setPos(self.pos().x(), self.pos().y() - 10)
        # Collision TODO Problem when bullets collide with each other and enemy at the same time
        if self.collidingItems():
            colliding_item = self.collidingItems()[0]
            if type(colliding_item) is Enemy:
                scene.removeItem(self)
                scene.removeItem(colliding_item)
                del self
                del colliding_item
                score.increase()

        elif self.pos().y() < 0:
            scene.removeItem(self)
            del self
    #TODO if bullet is destroyed too soon, media player gets deleted before entire sound is played, needs longer lifecycle    
    def bang(self):
        self.player.play()

    
class Enemy(QGraphicsPixmapItem, QObject):
    def __init__(self):
        super().__init__()

        self.setPixmap(QPixmap(":/images/images/enemy_tank.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.setPos(random.randint(0, view.width() - self.pixmap().width()), 0)

        self.timer = QTimer()

        self.timer.timeout.connect(self.move)
        self.timer.start(250)

    def move(self):
        # TODO Mechanism for losing the game
        if self.pos().y() + self.pixmap().size().height() > view.height():
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

background = QGraphicsPixmapItem()

player = Player()

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
media_player.setSource(QUrl("qrc:/sounds/sounds/background_music_test.mp3"))
audio_output.setVolume(50)
media_player.play()

view.show()

app.exec()