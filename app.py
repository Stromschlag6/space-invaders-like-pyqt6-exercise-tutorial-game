from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QTimer, QObject, QUrl
from PyQt6.QtGui import QFont, QPixmap, QBrush, QImage, QPainterPath, QPen, QPainter, QColor, QPainterPathStroker
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import random, sys, resources

class Player(QGraphicsPixmapItem, QObject):
    def __init__(self):
        super().__init__()

        self.setPixmap(QPixmap(":/images/images/tank.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.contour_path = self.create_contour_path()

        self.timer = QTimer()

        self.timer.timeout.connect(self.spawn)
        self.timer.start(3000)

    def create_contour_path(self):
        """
        Erstellt einen QPainterPath entlang der sichtbaren Pixel (Alpha > 0)
        """
        image = self.pixmap().toImage()
        width = image.width()
        height = image.height()
        path = QPainterPath()

        # einfache Kontur-Algorithmus:
        # wir überprüfen jeden Pixel; wenn Alpha > 0 und irgendein Nachbar Alpha=0, ist er Rand
        for y in range(height):
            for x in range(width):
                color = image.pixelColor(x, y)
                if color.alpha() == 0:
                    continue  # unsichtbar

                # Prüfe Nachbarn
                neighbors = [
                    (x-1, y), (x+1, y),
                    (x, y-1), (x, y+1)
                ]
                for nx, ny in neighbors:
                    if nx < 0 or nx >= width or ny < 0 or ny >= height:
                        is_edge = True
                    else:
                        if image.pixelColor(nx, ny).alpha() == 0:
                            is_edge = True
                        else:
                            is_edge = False
                    if is_edge:
                        # zeichne kleinen Punkt an Rand
                        path.addRect(x, y, 1, 1)
                        break

        # optional: Pfad glätten, indem wir QPainterPathStroker nutzen
        stroker = QPainterPathStroker()
        stroker.setWidth(1.5)  # Linienstärke
        stroker.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        stroker.setCapStyle(Qt.PenCapStyle.RoundCap)
        return stroker.createStroke(path)
    
    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(0, 0, 255, 50), 1.5)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # nur Kontur zeichnen
        painter.drawPath(self.contour_path)

    def shape(self):
        return self.contour_path

    def spawn(self):
        enemy = Enemy()
        scene.addItem(enemy)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            if self.pos().x() >= 0:
                self.setPos(self.pos().x() - 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Right:
            if self.pos().x() + self.pixmap().width() < view.width():
                self.setPos(self.pos().x() + 10, self.pos().y())

        elif event.key() == Qt.Key.Key_Space:
            bullet = Bullet()
            bullet.bang()
            bullet.setPos(player.pos().x() + (player.pixmap().width() / 2 - bullet.pixmap().width() / 2) , player.pos().y())
            print(bullet.pixmap().isNull())
            scene.addItem(bullet)
    

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

        self.contour_path = self.create_contour_path()

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

    def create_contour_path(self):
        """
        Erstellt einen QPainterPath entlang der sichtbaren Pixel (Alpha > 0)
        """
        image = self.pixmap().toImage()
        width = image.width()
        height = image.height()
        path = QPainterPath()

        for y in range(height):
            for x in range(width):
                color = image.pixelColor(x, y)
                if color.alpha() == 0:
                    continue 

                neighbors = [
                    (x-1, y), (x+1, y),
                    (x, y-1), (x, y+1)
                ]
                for nx, ny in neighbors:
                    if nx < 0 or nx >= width or ny < 0 or ny >= height:
                        is_edge = True
                    else:
                        if image.pixelColor(nx, ny).alpha() == 0:
                            is_edge = True
                        else:
                            is_edge = False
                    if is_edge:
                        path.addRect(x, y, 1, 1)
                        break

        stroker = QPainterPathStroker()
        stroker.setWidth(1.5)  # Linienstärke
        stroker.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        stroker.setCapStyle(Qt.PenCapStyle.RoundCap)
        return stroker.createStroke(path)
    
    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(255, 0, 0, 50), 1.5)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawPath(self.contour_path)

    def shape(self):
        return self.contour_path


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

player = Player()

media_player = QMediaPlayer()
audio_output = QAudioOutput()

score = Score()
health = Health()

view.setFixedSize(800, 600)
view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

scene.setSceneRect(0, 0, 800, 600)
scene.setBackgroundBrush(QBrush(QImage(":/images/images/background.jpg")))

player.setPos((view.width() - player.pixmap().width()) / 2, view.height() - player.pixmap().height())
player.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsFocusable)
player.setFocus()

health.setPos(health.pos().x(), health.pos().y() + 25)

scene.addItem(player)
scene.addItem(score)
scene.addItem(health)
# TODO background music not repeating itself
media_player.setAudioOutput(audio_output)
media_player.setSource(QUrl("qrc:/sounds/sounds/war_background_music.mp3"))
audio_output.setVolume(50)
media_player.play()

view.show()

app.exec()