import sys, sqlite3


from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow, QLayout, QPushButton, QDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QTransform, QFont


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect('database.db')
        self.cur = self.db.cursor()
        uic.loadUi('untitled.ui', self)
        self.loginbutton.clicked.connect(self.login)
        self.regbutton.clicked.connect(self.registration)
        self.menubutton.clicked.connect(self.openmenu)
        self.booksbutton.clicked.connect(self.books)
        self.exitbutton.clicked.connect(self.exit)
        self.exitbutton.hide()
        self.regbutton.hide()
        self.loginbutton.hide()
        self.booksbutton.hide()
        self.currentuser = (self.cur.execute("""select username from last_user where id = 1""").fetchall())[0][0]
        self.message = QLabel('', self)


    def login(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Вход")
        self.dialog.resize(220, 220)
        self.logtext = QLabel('Логин:', self.dialog)
        self.pastext = QLabel('Пароль:', self.dialog)
        self.answer = QLabel('', self.dialog)
        self.login = QLineEdit(self.dialog)
        self.password = QLineEdit(self.dialog)
        okbtn = QPushButton('OK', self.dialog)
        cancbtn = QPushButton('Cancel', self.dialog)
        self.logtext.move(10, 55)
        self.pastext.move(10, 85)
        self.answer.resize(200, 20)
        self.answer.move(10, 160)
        self.login.resize(150, 20)
        self.login.move(60, 50)
        self.password.resize(150, 20)
        self.password.move(60, 80)
        okbtn.resize(90, 20)
        okbtn.move(5, 190)
        cancbtn.resize(90, 20)
        cancbtn.move(125, 190)
        okbtn.clicked.connect(self.checkuser)
        cancbtn.clicked.connect(self.closething)
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def registration(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Регистрация")
        self.dialog.resize(220, 220)
        self.logtext = QLabel('Логин:', self.dialog)
        self.pastext = QLabel('Пароль:', self.dialog)
        self.emailtext = QLabel('Почта:', self.dialog)
        self.answer = QLabel('', self.dialog)
        self.email = QLineEdit(self.dialog)
        self.login = QLineEdit(self.dialog)
        self.password = QLineEdit(self.dialog)
        okbtn = QPushButton('OK', self.dialog)
        cancbtn = QPushButton('Cancel', self.dialog)
        self.emailtext.move(10, 25)
        self.logtext.move(10, 55)
        self.pastext.move(10, 85)
        self.answer.resize(200, 20)
        self.answer.move(10, 160)
        self.email.resize(150, 20)
        self.email.move(60, 20)
        self.login.resize(150, 20)
        self.login.move(60, 50)
        self.password.resize(150, 20)
        self.password.move(60, 80)
        okbtn.resize(90, 20)
        okbtn.move(5, 190)
        cancbtn.resize(90, 20)
        cancbtn.move(125, 190)
        okbtn.clicked.connect(self.registeruser)
        cancbtn.clicked.connect(self.closething)
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def exit(self):
        self.currentuser = '0'
        self.cur.execute("""update last_user set username='0' where id=1""").fetchall()
        self.db.commit()

    def checkuser(self):
        log = self.login.text()
        pas = self.password.text()
        password = self.cur.execute("""select password from users where login = ?""", (log, )).fetchall()
        if len(password) == 0:
            self.answer.setText('Несуществующий логин')
        elif self.currentuser == log:
            self.answer.setText('Вы уже вошли')
        else:
            if pas == password[0][0]:
                self.currentuser = log
                self.dialog.setVisible(False)
                self.cur.execute("""update last_user set username=? where id=1""", (log, )).fetchall()
                self.message.hide()
                self.hellolabel.hide()
            else:
                self.answer.setText('Неправильный пароль')
        self.db.commit()

    def registeruser(self):
        log = self.login.text()
        pas = self.password.text()
        em = self.email.text()
        i = (self.cur.execute("""select id from users where id=(select max(id) from users)""").fetchall())[0][0]
        login = self.cur.execute("""select login from users where login = ?""", (log, )).fetchall()
        email = self.cur.execute("""select login from users where login = ?""", (em, )).fetchall()
        self.cur.execute("""update last_user set username=? where id=1""", (log, )).fetchall()
        if len(email) == 0:
            if len(login) == 0:
                if len(log) >= 8:
                    self.message.hide()
                    self.hellolabel.hide()
                    self.cur.execute("""insert into users (id, email, login, password) values (?, ?, ?, ?)""", ((i + 1), em, log, pas)).fetchall()
                    self.cur.execute("""update last_user set username=? where id=1""", (log, )).fetchall()
                    self.currentuser = log
                    self.dialog.setVisible(False)
                else:
                    self.answer.setText('Логин должен быть больше 7 символов')
            else:
                self.answer.setText('Придумайте другой логин')
        else:
            self.answer.setText('Эта почта зарегестрирована')
        self.db.commit()

    def closething(self):
        self.dialog.setVisible(False)

    def openmenu(self):
        self.loginbutton.show()
        self.regbutton.show()
        self.booksbutton.show()
        self.exitbutton.show()
        self.menubutton.hide()

    def books(self):
        self.message.hide()
        self.regbutton.hide()
        self.loginbutton.hide()
        self.booksbutton.hide()
        self.exitbutton.hide()
        self.menubutton.show()
        if self.currentuser == '0':
            self.hellolabel.setText('')
            self.message = QLabel('Войдите в аккаунт чтобы получить книжки', self)
            self.message.setFont(QFont('MS Shell Dlg 2', 12))
            self.message.resize(320, 31)
            self.message.move(140, 61)
            self.message.show()
        else:
            self.hellolabel.setText(f'Привет, {self.currentuser}, вот твои книжки')
            books = self.cur.execute("""select title from books where id=
                                        (select id_book from has_book where id_user=
                                        (select id from users where login=?))""", (self.currentuser, )).fetchall()
            if len(books) == 0:
                self.message = QLabel('К сожалению, у вас нет ни одной книжки :(', self)
                self.message.setFont(QFont('MS Shell Dlg 2', 10))
                self.message.resize(260, 31)
                self.message.move(170, 61)
                self.message.show()
            else:
                pass

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())