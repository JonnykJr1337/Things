import sys, sqlite3

from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QListWidgetItem


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = sqlite3.connect('database.db')
        self.cur = self.db.cursor()
        uic.loadUi('untitled.ui', self)
        self.pages.setCurrentIndex(0)
        self.okbutton.clicked.connect(self.checkuser)
        self.okok.clicked.connect(self.registeruser)
        self.nono.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.back.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.cancelbutton.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.loginbutton.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.regbutton.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.booksbutton.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        self.booksbutton.clicked.connect(self.searchingbooks)
        self.exitbutton.clicked.connect(self.exit)
        self.back_2.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        self.addbook.clicked.connect(self.addbookk)
        self.userbooks.itemDoubleClicked.connect(self.monitorim)
        self.currentuser = (self.cur.execute("""select username from last_user""").fetchall())[0][0]

    def monitorim(self):
        self.pages.setCurrentIndex(5)
        self.showbook.setHtml((
                                  self.cur.execute("""select html from books where title = ?""",
                                                   (self.userbooks.selectedItems()[0].text(),)).fetchall())[0][0])

    def addbookk(self):
        check = False
        self.pages.setCurrentIndex(4)
        self.booklist.itemDoubleClicked.connect(self.addbooktouser)
        self.cancelforbooks.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        self.okforbooks.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        self.okforbooks.clicked.connect(self.searchingbooks)
        books = self.cur.execute("""select title from books""")
        for elem in books:
            for elem1 in self.booklist.selectedItems():
                if elem[0] == elem1.text():
                    check = True
            if not check:
                self.booklist.addItem(elem[0])
            else:
                check = False

    def addbooktouser(self):
        self.cur.execute("""insert into has_book (id_user, id_book) values ((select id from users where login = ?), 
        (select id from books where title = ?))""", (self.currentuser, self.booklist.selectedItems()[0].text()))
        self.db.commit()

    def exit(self):
        self.currentuser = '0'
        self.cur.execute("""update last_user set username='0'""").fetchall()
        self.db.commit()
        self.close()

    def checkuser(self):
        log = self.login.text()
        pas = self.password.text()
        password = self.cur.execute("""select password from users where login = ?""", (log,)).fetchall()
        if len(password) == 0:
            self.answer.setText('Несуществующий логин')
        elif self.currentuser == log:
            self.answer.setText('Вы уже вошли')
        else:
            if pas == password[0][0]:
                self.currentuser = log
                self.cur.execute("""update last_user set username=?""", (log,)).fetchall()
                self.pages.setCurrentIndex(0)
            else:
                self.answer.setText('Неправильный пароль')
        self.db.commit()

    def registeruser(self):
        log = self.reglogin.text()
        pas = self.regpassword.text()
        em = self.regemail.text()
        i = (self.cur.execute("""select id from users where id=(select max(id) from users)""").fetchall())[0][0]
        login = self.cur.execute("""select login from users where login = ?""", (log,)).fetchall()
        email = self.cur.execute("""select login from users where login = ?""", (em,)).fetchall()
        self.cur.execute("""update last_user set username=?""", (log,)).fetchall()
        if len(email) == 0:
            if len(login) == 0:
                if len(log) >= 8:
                    self.cur.execute("""insert into users (id, email, login, password) values (?, ?, ?, ?)""",
                                     ((i + 1), em, log, pas)).fetchall()
                    self.cur.execute("""update last_user set username=?""", (log,)).fetchall()
                    self.currentuser = log
                    self.pages.setCurrentIndex(0)
                else:
                    self.answer.setText('Логин должен быть больше 7 символов')
            else:
                self.answer.setText('Придумайте другой логин')
        else:
            self.answer.setText('Эта почта зарегистрирована')
        self.db.commit()

    def searchingbooks(self):
        if self.currentuser == '0':
            self.hellolabel.setText('')
            self.messagelabel.setText('Войдите в аккаунт чтобы получить книжки')
        else:
            self.hellolabel.setText(f'Привет, {self.currentuser}, вот твои книжки')
            self.messagelabel.setText('')
            books = self.cur.execute("""select title from books where id=
                                        (select id_book from has_book where id_user=
                                        (select id from users where login=?))""", (self.currentuser,)).fetchall()
            if len(books) == 0:
                self.messagelabel.setText('К сожалению, у вас нет ни одной книжки :(')
            else:
                check = False
                for elem in books:
                    for elem1 in self.userbooks.selectedItems():
                        if elem[0] == elem1.text():
                            check = True
                    if not check:
                        self.userbooks.addItem(elem[0])
                    else:
                        check = False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
