# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pyperclip
import sys

from init import *

class window(QMainWindow):
    def __init__(self):
        app = QApplication(sys.argv)
        super(window, self).__init__()
        self.loadConfig()
        initIcons(config)

        self.openedfile=""

        self.mainUi = uic.loadUi('main.ui')
        self.mainUi.setWindowTitle(config['title'])
        self.mainUi.setWindowIcon(QIcon(config['icons']['icon']))

        self.preferencesUi = uic.loadUi('preferences.ui')
        self.preferencesUi.setWindowIcon(QIcon(config['icons']['preferences']))
        self.preferencesUi.setParent(self.mainUi)
        self.preferencesUi.setWindowFlags(Qt.WindowFlags(Qt.Dialog))

        self.functionality()

        self.mainUi.show()
        sys.exit(app.exec_())

    def loadConfig(self):
        initConfig()
        #print(config)

    def saveConfig(self):
        with open("./config.json", "w") as jsonfile:
            json.dump(config, jsonfile, indent='\t')

    def functionality(self):
        ## Icons
        self.new_icon = QIcon()
        self.new_icon.addPixmap(QPixmap(config['icons']['new']), QIcon.Normal, QIcon.Off)
        self.open_icon = QIcon()
        self.open_icon.addPixmap(QPixmap(config['icons']['open']), QIcon.Normal, QIcon.Off)
        self.save_icon = QIcon()
        self.save_icon.addPixmap(QPixmap(config['icons']['save']), QIcon.Normal, QIcon.Off)
        self.exit_icon = QIcon()
        self.exit_icon.addPixmap(QPixmap(config['icons']['exit']), QIcon.Normal, QIcon.Off)
        self.preferences_icon = QIcon()
        self.preferences_icon.addPixmap(QPixmap(config['icons']['preferences']), QIcon.Normal, QIcon.Off)

        self.mainUi.actionSave.setIcon(self.save_icon)
        self.mainUi.actionSave_As.setIcon(self.save_icon)
        self.mainUi.actionNew.setIcon(self.new_icon)
        self.mainUi.actionOpen.setIcon(self.open_icon)
        self.mainUi.actionPreferences.setIcon(self.preferences_icon)
        self.mainUi.actionClose.setIcon(self.exit_icon)

        ## Plain Text Edit
        self.mainUi.plainTextEdit.setPlaceholderText(f"Welcome to UNotes! (v.{config['version']})\nFont {config['font']} {config['font-size']}")
        self.mainUi.plainTextEdit.setFont(QFont(config['font'], config['font-size']))

        ## Actions
        self.mainUi.actionNew.triggered.connect(lambda: self.file_new())
        self.mainUi.actionSave.triggered.connect(lambda: self.file_save())
        self.mainUi.actionSave_As.triggered.connect(lambda: self.file_save_as())
        self.mainUi.actionOpen.triggered.connect(lambda: self.file_open())
        self.mainUi.actionClose.triggered.connect(lambda: self.mainUi.close())
        self.mainUi.actionPaste.triggered.connect(lambda: self.mainUi.plainTextEdit.appendPlainText(pyperclip.paste()))
        self.mainUi.actionPreferences.triggered.connect(lambda: self.preferences())

        ################
        ### PREFERENCES 
        self.preferencesUi.fontFamily.setCurrentFont(QFont(config['font']))
        self.preferencesUi.fontSize.setCurrentIndex(config['font-size-index'])

        themes = ['Dark', 'Light']

        theme = config['theme']
        if theme == "Dark":
            self.mainUi.plainTextEdit.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(25, 25, 25); border-color: rgb(25, 25, 25);")

        self.preferencesUi.appTheme.clear()
        self.preferencesUi.appTheme.addItems(themes)
        self.preferencesUi.appTheme.setCurrentIndex(self.preferencesUi.appTheme.findText(config['theme']))

        self.preferencesUi.fontSize.currentTextChanged.connect(lambda: self.preferencesUpdate())
        self.preferencesUi.fontFamily.currentTextChanged.connect(lambda: self.preferencesUpdate())
        self.preferencesUi.appTheme.currentTextChanged.connect(lambda: self.preferencesUpdate())


    def file_new(self):
        if self.mainUi.plainTextEdit.toPlainText() != "":
            if self.confirmationDialog("Unsaved File", f"Do you want to save changes?"):
                self.file_save()
        self.mainUi.plainTextEdit.clear()
        self.mainUi.openedfile = ""


    def file_save(self):
        if self.openedfile != "":
            file = open(self.openedfile, "w", encoding="utf-8")
            file.write(self.mainUi.plainTextEdit.toPlainText())
            file.close()
        else:
            self.file_save_as()


    def file_save_as(self):
        data = QFileDialog.getSaveFileName(self.mainUi,"Save File","untitled.txt","*.txt",options=QFileDialog.Options())
        if data[0]!="":
            fileopen=open(data[0], "w", encoding="utf-8")
            self.openedfile = data[0]
            fileopen.write(self.mainUi.plainTextEdit.toPlainText())
            fileopen.close()
    

    def file_open(self):
        if self.mainUi.plainTextEdit.toPlainText() != "":
            if self.confirmationDialog("Unsaved File", f"Do you want to save changes?"):
                self.file_save()

        data=QFileDialog.getOpenFileName(self.mainUi, "Select File","","*.txt",options=QFileDialog.Options())
        if data[0]!="":
            fileopen=open(data[0], "r")
            self.openedfile = data[0]
            self.mainUi.plainTextEdit.setPlainText(fileopen.read())
            fileopen.close()


    def preferences(self):
        if self.preferencesUi.exec():
            config["font"] = self.preferencesUi.fontFamily.currentText()
            config["font-size"] = int(self.preferencesUi.fontSize.currentText())
            config["theme"] = self.preferencesUi.appTheme.currentText()
            self.saveConfig()
        else:
            self.preferencesUi.fontFamily.setCurrentFont(QFont(config['font']))
            self.preferencesUi.fontSize.setCurrentIndex(config['font-size-index'])
        
        self.mainUi.plainTextEdit.setFont(QFont(config['font'], config['font-size']))
        self.mainUi.plainTextEdit.setPlaceholderText(f"Welcome to UNotes! (v.{config['version']})\nFont {config['font']} {config['font-size']}")
    
    def preferencesUpdate(self):
        font = self.preferencesUi.fontFamily.currentText()
        fontSize = int(self.preferencesUi.fontSize.currentText())
        self.mainUi.plainTextEdit.setFont(QFont(font, fontSize))

        theme = self.preferencesUi.appTheme.currentText()
        if theme == "Dark":
            css = "color: rgb(255, 255, 255); background-color: rgb(25, 25, 25); border-color: rgb(25, 25, 25);"
        elif theme == "Light":
            css = ""
        self.mainUi.plainTextEdit.setStyleSheet(css)

    def confirmationDialog(self, title, text):
        msg = QMessageBox(self.mainUi)
        reply = msg.question(self, title, text, msg.Yes | msg.No)
        msg.setParent(self.mainUi)
        msg.setWindowFlags(Qt.WindowFlags(Qt.Dialog))

        if reply == msg.Yes:
            return True
        if reply == msg.No:
            return False



window()

