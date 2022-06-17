from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QTextEdit, QVBoxLayout, QAction, QFileDialog
from PyQt5.QtWidgets import QFontDialog
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSettings
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.settings = QSettings('Text Editor', 'PyQt5 Text Editor')
        self.filename = None
        self.file_open = False
        self.te_main = QTextEdit(self)
        self.setWindowTitle("PyQt5 Text Editor")
        self.setGeometry(100, 100, 800, 500)
        self.setMinimumSize(200, 200)

        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window location'))
            font = QFont()
            font.setFamily(self.settings.value('font family'))
            font.setPointSize(int(self.settings.value('font size')))
            font.setBold(eval(self.settings.value('bold')))
            font.setItalic(eval(self.settings.value('italics')))
            font.setUnderline(eval(self.settings.value('underline')))
            self.te_main.setFont(font)
        except:
            pass
        self.build_ui()

    def build_ui(self):

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        new_menu = QAction('New', self)
        new_menu.setShortcut('Ctrl+N')
        new_menu.triggered.connect(self.new)
        file_menu.addAction(new_menu)

        open_menu = QAction('Open', self)
        open_menu.setShortcut('Ctrl+O')
        open_menu.triggered.connect(self.open)
        file_menu.addAction(open_menu)

        save_menu = QAction('Save', self)
        save_menu.setShortcut('Ctrl+S')
        save_menu.triggered.connect(self.save)
        file_menu.addAction(save_menu)

        print_menu = QAction('Print', self)
        print_menu.setShortcut('Ctrl+P')
        print_menu.triggered.connect(self.print_file)
        file_menu.addAction(print_menu)

        edit_menu = menu_bar.addMenu("Edit")

        undo_menu = QAction('Undo', self)
        undo_menu.setShortcut('Ctrl+Z')
        undo_menu.triggered.connect(self.undo)
        edit_menu.addAction(undo_menu)

        redo_menu = QAction('Redo', self)
        redo_menu.setShortcut('Ctrl+Y')
        redo_menu.triggered.connect(self.redo)
        edit_menu.addAction(redo_menu)

        copy_menu = QAction('Copy', self)
        copy_menu.setShortcut('Ctrl+C')
        copy_menu.triggered.connect(self.copy)
        edit_menu.addAction(copy_menu)

        cut_menu = QAction('Cut', self)
        cut_menu.setShortcut('Ctrl+X')
        cut_menu.triggered.connect(self.cut)
        edit_menu.addAction(cut_menu)

        paste_menu = QAction('Paste', self)
        paste_menu.setShortcut('Ctrl+V')
        paste_menu.triggered.connect(self.paste)
        edit_menu.addAction(paste_menu)

        font_menu = QAction('Font', self)
        font_menu.triggered.connect(self.set_font)
        edit_menu.addAction(font_menu)

        vertical_box = QVBoxLayout()
        vertical_box.addWidget(self.te_main)
        vertical_box.setStretchFactor(self.te_main, 1)
        vertical_box.setContentsMargins(0, 0, 0, 0)

        central_widget = QWidget()
        central_widget.setLayout(vertical_box)
        self.setCentralWidget(central_widget)

    def copy(self):
        self.te_main.copy()

    def cut(self):
        self.te_main.cut()

    def paste(self):
        self.te_main.paste()

    def undo(self):
        self.te_main.undo()

    def redo(self):
        self.te_main.redo()

    def set_font(self):
        font, valid = QFontDialog().getFont()
        if valid:
            self.te_main.setFont(QFont(font))

    def new(self):
        self.filename = None
        self.file_open = False
        self.te_main.clear()

    def open(self):
        self.te_main.setPlainText("")
        open_file = QFileDialog.getOpenFileName(self, 'Open')
        self.file_open = True
        self.filename = open_file[0]
        try:
            o = open(self.filename, "r")
            content = o.read()
            self.te_main.setPlainText(content)
            o.close()
        except IOError:
            print()
        self.post_save()

    def save(self):
        save_file = QFileDialog.getSaveFileName(self, 'Save')
        self.filename = save_file[0]
        self.file_open = True
        text_to_save = self.te_main.toPlainText()

        try:
            f = open(self.filename, "w")
            f.write(text_to_save)
            f.close()
        except IOError:
            pass
        self.post_save()

    def post_save(self):
        window_title = "PyQt5 Text Editor - " + self.filename
        self.setWindowTitle(window_title)

    def print_file(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_():
            self.te_main.print_(printer)

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window location', self.pos())
        self.settings.setValue('font family', str(self.te_main.font().family()))
        self.settings.setValue('font size', str(self.te_main.font().pointSize()))
        self.settings.setValue('bold', str(self.te_main.font().bold()))
        self.settings.setValue('italics', str(self.te_main.font().italic()))
        self.settings.setValue('underline', str(self.te_main.font().underline()))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())