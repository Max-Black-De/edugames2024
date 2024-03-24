from pygame import *
from random import randint
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QRadioButton, QHBoxLayout, QGroupBox, QButtonGroup, QTextEdit
from random import shuffle

mixer.init()
font.init()

class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

class Text(sprite.Sprite):
    def __init__(self, text, x, y, colour1, colour2, colour3):
        super().__init__()
        self.text = text
        self.colour1 = colour1
        self.colour2 = colour2
        self.colour3 = colour3
        self.font_ = font.Font(None, 40)
        self.label = self.font_.render(self.text, True, (self.colour1,self.colour2,self.colour3))
        self.rect = self.label.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.label, (self.rect.x, self.rect.y))

class GameSprite(sprite.Sprite):
    def __init__(self, game_image, speed, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(game_image), (w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 435:
            self.rect.y += self.speed

class Enemy_up(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 540:
            self.rect.x = randint(0, 640)
            self.rect.y = 0

class Enemy_left(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 740:
            self.rect.y = randint(0, 460)
            self.rect.x = 0

class Enemy_right(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x <= -40:
            self.rect.y = randint(0, 460)
            self.rect.x = 740

class Enemy_down(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.rect.x = randint(0, 640)
            self.rect.y = 540

def choice():
    if pbt_glav.text() == 'Ответить':
        check_answer()
    elif pbt_glav.text() == 'Перейти к тесту':
        next_question()
    elif pbt_glav.text() == 'Закрыть програму':
        app.quit()

def pbt1_text():
    text.setText('wasd - управление кораблём')
    
def pbt2_text():
    text.setText('Игра состоит из двух частей: викторина, полёт. В зависимости от количества привильных ответов в викторие, во время полёта на корабле вам будут даны дополнительные hp(по умолчанию hp = 1).\nЦель игры: продержаться в космосе 20 секунд')

def show_question():
        Group_training.hide()
        Group_right.hide()
        Group_question.show()
        pbt_glav.setText('Ответить')

def show_right():
    Group_training.hide()
    Group_question.hide()
    pbt_glav.hide()
    Group_right.show()
    pbt_glav.setText('Закрыть програму')

def check_answer():
    if answers[0].isChecked():
        main_win.right += 1 
        main_win.total += 1
        next_question()
    if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
        main_win.wrong += 1
        main_win.total += 1
        next_question()

def ask(q: Question):
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)    
    text_question.setText(q.question)
    reboot()

def reboot():
    pbt_glav.setText('Ответить')
    RadioGroup.setExclusive(False)
    rbt1.setChecked(False)
    rbt2.setChecked(False)
    rbt3.setChecked(False)
    rbt4.setChecked(False)
    RadioGroup.setExclusive(True)
    show_question()


def next_question():
    if main_win.score == len(qlist) - 1:
        your_wrong.setText(f'Всего неправильных {main_win.wrong}')
        your_right.setText(f'Всего правильных {main_win.right}')
        show_right()
    else:
        main_win.score += 1
        q = qlist[main_win.score]
        ask(q)

mixer.music.load('fonk.mp3')
mixer.music.play()

qlist = list()
qlist.append(Question('Назовите спутник Юпитера?', 'Европа', 'Азия', 'Промитей',   'Антарктида'))
qlist.append(Question('Диаметр колец Сатурна?', '250000', '7000', '5000', '230000'))
qlist.append(Question('Какой бог не связан с планетами', 'Борей', 'Зевс', 'Гермес', 'Афрадита'))
qlist.append(Question('Какого цвета Солнце?','Белое',  'жёлтое', 'Casa Blanca',  'Красное'))
shuffle(qlist)

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Инфотест')
main_win.right = 0
main_win.total = 0
main_win.wrong = 0
main_win.score = -1
pbt1 = QPushButton('Управление')
pbt2 = QPushButton('Об игре')
pbt_glav = QPushButton('Перейти к тесту')
text = QTextEdit()
text.setText('Это обучение. Правее расположены кнопки с помощью, которых можно рахобраться в геймплее')
Group_training = QGroupBox('Обучение')
text_question = QLabel('Вопрос')
rbt1 = QRadioButton('1')
rbt2 = QRadioButton('2')
rbt3 = QRadioButton('3')
rbt4 = QRadioButton('4')
Group_question = QGroupBox('Вопросы')
right_answer = QLabel(f'Всего вопросов {len(qlist)}')
your_right = QLabel('Всего правильных')
your_wrong = QLabel('Всего неправильных')
Group_right = QGroupBox('Результаты')

Group = QGroupBox()

answers = [rbt1, rbt2, rbt3, rbt4]

vline_glav_text = QVBoxLayout()
hline_text = QHBoxLayout()
vline_text = QVBoxLayout()
vline = QVBoxLayout()

vline_text.addWidget(pbt1)
vline_text.addWidget(pbt2)
hline_text.addWidget(text)
hline_text.addLayout(vline_text)
vline_glav_text.addLayout(hline_text)
Group_training.setLayout(vline_glav_text)

hline1_group_question = QHBoxLayout()
hline2_group_question = QHBoxLayout()
vline_group_question = QVBoxLayout()
vline_minigrup = QVBoxLayout()

hline1_group_question.addWidget(rbt1)
hline1_group_question.addWidget(rbt2)
hline2_group_question.addWidget(rbt3)
hline2_group_question.addWidget(rbt4)
vline_minigrup.addLayout(hline1_group_question)
vline_minigrup.addLayout(hline2_group_question)
Group.setLayout(vline_minigrup)
vline_group_question.addWidget(text_question, alignment = Qt.AlignCenter)
vline_group_question.addWidget(Group, alignment = Qt.AlignCenter)
Group_question.hide()
Group_question.setLayout(vline_group_question)

vline_group_right = QVBoxLayout()

vline_group_right.addWidget(right_answer, alignment = Qt.AlignCenter)
vline_group_right.addWidget(your_right, alignment = Qt.AlignCenter)
vline_group_right.addWidget(your_wrong, alignment = Qt.AlignCenter)
Group_right.hide()
Group_right.setLayout(vline_group_right)

vline.addWidget(Group_training)
vline.addWidget(Group_question)
vline.addWidget(Group_right)
vline.addWidget(pbt_glav)

main_win.setLayout(vline)

RadioGroup = QButtonGroup()
RadioGroup.addButton(rbt1)
RadioGroup.addButton(rbt2)
RadioGroup.addButton(rbt3)
RadioGroup.addButton(rbt4)



pbt1.clicked.connect(pbt1_text)
pbt2.clicked.connect(pbt2_text)
pbt_glav.clicked.connect(choice)



pbt_glav.clicked.connect(choice)


main_win.show()
app.exec_()

window = display.set_mode((700,500))
display.set_caption('Смертельный полёт')
background = transform.scale(image.load('space.png'),(700,500))
bg_y = 0

player = Player('rocket.png', 10, 350, 400, 60, 50)

meteors_up = sprite.Group()
meteors_left = sprite.Group()
meteors_right = sprite.Group()
meteors_down = sprite.Group()




for i in range(4):
    random = randint(1,3)
    image_rocket = 0
    if random == 1:
        image_rocket = 'астеройд.png'
    if random == 2:
        image_rocket = 'астеройд2.png'
    if random == 3:
        image_rocket = 'пришельцы.png'
    meteor = Enemy_up(image_rocket, randint(1, 3), randint(0, 620),-50, 40, 40)
    meteor.add(meteors_up)

for i in range(4):
    random = randint(1,3)
    image_rocket = 0
    if random == 1:
        image_rocket = 'астеройд.png'
    if random == 2:
        image_rocket = 'астеройд2.png'
    if random == 3:
        image_rocket = 'пришельцы.png'
    meteor = Enemy_left(image_rocket, randint(1, 3), -50, randint(0, 420), 40, 40)
    meteor.add(meteors_left)

for i in range(4):
    random = randint(1,3)
    image_rocket = 0
    if random == 1:
        image_rocket = 'астеройд.png'
    if random == 2:
        image_rocket = 'астеройд2.png'
    if random == 3:
        image_rocket = 'пришельцы.png'
    meteor = Enemy_right(image_rocket, randint(1, 3), 750, randint(0, 420), 40, 40)
    meteor.add(meteors_right)


for i in range(4):
    random = randint(1,3)
    image_rocket = 0
    if random == 1:
        image_rocket = 'астеройд.png'
    if random == 2:
        image_rocket = 'астеройд2.png'
    if random == 3:
        image_rocket = 'пришельцы.png'
    meteor = Enemy_down(image_rocket, randint(1, 3), randint(0, 620),550, 40, 40)
    meteor.add(meteors_down)



game = True
gameplay = True
question_game = True
hp = main_win.right + 1
clock = time.Clock()

lose = Text('Вы проиграли', 250, 200, 115, 132, 148)
win = Text('Вы победили', 250, 200, 115, 132, 148)
restart = Text('Закрыть игру', 250, 300, 166, 225, 223)
hp_text = Text(str(hp), 10, 10, 255, 0, 0)

second = 0


while game:

    for i in event.get():
            if i.type == QUIT:
                game = False
                pause = False


    

    if second >= 1200:
        gameplay = False

    if gameplay:

        

        second += 1 

        bg_y +=1
        if bg_y == 500:
            bg_y = 0

        if sprite.spritecollide(player, meteors_up, True):
            hp -= 1
            random = randint(1,3)
            image_rocket = 0
            if random == 1:
                image_rocket = 'астеройд.png'
            if random == 2:
                image_rocket = 'астеройд2.png'
            if random == 3:
                image_rocket = 'пришельцы.png'
            meteor = Enemy_up(image_rocket, randint(1, 3), randint(0, 620),-50, 40, 40)
            meteor.add(meteors_up)       
        if sprite.spritecollide(player, meteors_left, True):
            hp -= 1
            random = randint(1,3)
            image_rocket = 0
            if random == 1:
                image_rocket = 'астеройд.png'
            if random == 2:
                image_rocket = 'астеройд2.png'
            if random == 3:
                image_rocket = 'пришельцы.png'
            meteor = Enemy_left(image_rocket, randint(1, 3), -50, randint(0, 420), 40, 40)
            meteor.add(meteors_left)
        if sprite.spritecollide(player, meteors_right, True):
            hp -= 1
            random = randint(1,3)
            image_rocket = 0
            if random == 1:
                image_rocket = 'астеройд.png'
            if random == 2:
                image_rocket = 'астеройд2.png'
            if random == 3:
                image_rocket = 'пришельцы.png'
            meteor = Enemy_right(image_rocket, randint(1, 3), 750, randint(0, 420), 40, 40)
            meteor.add(meteors_right)
        if sprite.spritecollide(player, meteors_down, True):
            hp -= 1
            random = randint(1,3)
            image_rocket = 0
            if random == 1:
                image_rocket = 'астеройд.png'
            if random == 2:
                image_rocket = 'астеройд2.png'
            if random == 3:
                image_rocket = 'пришельцы.png'
            meteor = Enemy_down(image_rocket, randint(1, 3), randint(0, 620),550, 40, 40)
            meteor.add(meteors_down)

        
        
        if hp == 0:
            gameplay = False
        
                
        window.blit(background,(0,bg_y))
        window.blit(background,(0,bg_y - 500))
        player.update()
        meteors_up.update()
        meteors_left.update()
        meteors_right.update()
        meteors_down.update()
        player.reset()
        meteors_up.draw(window)
        meteors_left.draw(window)
        meteors_right.draw(window)
        meteors_down.draw(window)
        hp_text.label = hp_text.font_.render('hp:' + str(hp), True, (hp_text.colour1,hp_text.colour2,hp_text.colour3))
        hp_text.reset()

    else:
        mixer.music.stop()
        window.fill((87, 88, 89))
        if hp <= 0:
            lose.reset()
        else:
            win.reset()
        restart.reset()
        
        mouse_ = mouse.get_pos()
        if restart.rect.collidepoint(mouse_) and mouse.get_pressed()[0]:
            game = False
            


            



        

    clock.tick(60)
    display.update()