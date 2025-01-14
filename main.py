import sys

import os

from ui_scoopgui import *

from PySide6.QtGui import *

import subprocess

import re

from PySide6 import QtCore, QtWidgets, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

POWERSHELL_PATH = "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QWidget, QMessageBox, QComboBox)

from state_tooltip import StateTooltip

from threading import Thread

import time
from os.path import exists

from py_toggle import *

from Second_PushButton import *

from BlurWindow.blurWindow import blur

from BlurWindow.blurWindow import GlobalBlur
import resource_file_qt_rc

import plyer

from plyer import *

import webbrowser

from plyer import notification

import subprocess

from os.path import exists

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None , *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs, parent=parent)
        self.setupUi(self)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(1150, 700)

        GlobalBlur(self.winId(),Dark=True,QWidget=self)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")


        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.resize(1050, 700)
        #
        # hWnd = self.winId()
        # print(hWnd)
        # blur(hWnd)

        # self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")

        # loading splashscreen
        # self.stackedWidget.setCurrentWidget(self.splashscreen)


        # making widget and adding to layout
        self.go_recommended_apps_page_button = custompushbutton('Starred', parent=self)
        self.go_recommended_apps_page_button.setMinimumHeight(91)
        self.go_recommended_apps_page_button.setFixedWidth(251)

        self.enter_recommended_apps_frame.addWidget(self.go_recommended_apps_page_button, Qt.AlignCenter, Qt.AlignCenter)

        # attaching to function
        self.go_recommended_apps_page_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_1))

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # UPDATING SCOOP REPO WHEN LAUNCHING                    #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        def do_update_and_show_status():
            #update scoop repo
            powershell_do_update = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', "scoop update"]
            powershell_do_update_1 = subprocess.run(powershell_do_update, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                     universal_newlines=True, shell="False")

            powershell_do_update2 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', "scoop status"]
            powershell_do_update_2 = subprocess.run(powershell_do_update2, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                     universal_newlines=True, shell="False")
            status_output = powershell_do_update_2.stdout

            # check number of updates
            # does scoop status, counts lines and minuses 6 (non app lines)
            number = len(status_output.splitlines())
            number = number - 6

            if number == 0:
                notification.notify(
                    title='Scoop is up to date',
                    message="All apps up to date, no need to update",
                    app_icon="fluorite.ico",
                    timeout=10,
                )
            else:
                number = str(number)
                message = (number+" out of date apps found, please update")
                message = str(message)
                notification.notify(
                    title='Out of date apps',
                    message=message,
                    app_icon="fluorite.ico",
                    timeout=10,
                )

        t = Thread(target=do_update_and_show_status)
        t.daemon = True
        t.start()

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # INSTALL SCOOP-SEARCH IF NOT ALREADY                 #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        def check_if_scoop_search_installed():
            if exists('fluorite_store_config.txt') == False:

                notification.notify(
                    title='Installing one dependency please wait',
                    message='getting the scoop-search package from scoop',
                    app_icon="fluorite.ico",
                    timeout=10,
                )
                install_scoop_search_command = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', "scoop install scoop-search"]
                install_scoop_search = subprocess.run(install_scoop_search_command, stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE,
                                                        universal_newlines=True, shell="False")
                with open("fluorite_store_config", 'w') as file:
                    file.write("")
                    file.close()

                notification.notify(
                    title='Finished',
                    message='installed scoop-search dependency',
                    app_icon="fluorite.ico",
                    timeout=10,
                )

        t2 = Thread(target=check_if_scoop_search_installed)
        t2.daemon = True
        t2.start()

        def do_search():

            def clear_previous_description():
                self.app_desc_1_lbl.setText(" ")
                self.app_desc_2_lbl.setText(" ")
                self.app_desc_3_lbl.setText(" ")
                self.app_desc_4_lbl.setText(" ")
                self.app_desc_5_lbl.setText(" ")
                self.app_label_1.setText(" ")
                self.app_label_2.setText(" ")
                self.app_label_3.setText(" ")
                self.app_label_4.setText(" ")
                self.app_label_5.setText(" ")
                self.install_search_app_btn_1.setText(" ")
                self.install_search_app_btn_2.setText(" ")
                self.install_search_app_btn_3.setText(" ")
                self.install_search_app_btn_4.setText(" ")
                self.install_search_app_btn_5.setText(" ")

            t = Thread(target=clear_previous_description)
            t.daemon = True
            t.start()

            # as this part is rather slow, there'll be one function for each app

            def app_desc_1_function():
                try:
                    # making scoop cat commands
                    scoop_cat_command_1 = ("scoop cat "+final_app_one)
                    powershell_cat_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_cat_command_1)]
                    powershell_do_cat_1 = subprocess.run(powershell_cat_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                     universal_newlines=True, shell="False")
                except:
                    pass

                try:
                    # getting app description from the scoop cat commands
                    getting_stdout_1 = powershell_do_cat_1.stdout
                    splitting_stdout_1 = getting_stdout_1.split('\n')
                    app_desc_1 = splitting_stdout_1[2]

                    # since desc is sometimes 3 instead of 2, so this check is done
                    if 'version":' in app_desc_1:
                        app_desc_1 = splitting_stdout_1[3]

                    app_desc_1 = app_desc_1.strip(" ")
                    app_desc_1 = app_desc_1.strip('",')
                    app_desc_1 = app_desc_1.strip('description": ')

                except:
                    pass

                if successful_1:
                    self.install_search_app_btn_1.setText("install")

                # putting app description onto qt description box
                try:
                    self.app_desc_1_lbl.setText(str(app_desc_1))
                    self.app_label_1.setText(str(final_app_one))
                except:
                    pass

            def app_desc_2_function():
                try:
                    scoop_cat_command_2 = ("scoop cat "+final_app_two)
                    powershell_cat_2 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_cat_command_2)]
                    powershell_do_cat_2 = subprocess.run(powershell_cat_2, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                         universal_newlines=True, shell="False")
                except:
                    pass

                try:
                    getting_stdout_2 = powershell_do_cat_2.stdout
                    splitting_stdout_2 = getting_stdout_2.split('\n')
                    app_desc_2 = splitting_stdout_2[2]

                    if 'version":' in app_desc_2:
                        app_desc_2 = splitting_stdout_2[3]

                    app_desc_2 = app_desc_2.strip(" ")
                    app_desc_2 = app_desc_2.strip('",')
                    app_desc_2 = app_desc_2.strip('description": ')

                except:
                    pass

                if successful_2:
                    self.install_search_app_btn_2.setText("install")

                try:
                    self.app_desc_2_lbl.setText(str(app_desc_2))
                    self.app_label_2.setText(str(final_app_two))
                except:
                    pass


            def app_desc_3_function():
                try:
                    scoop_cat_command_3 = ("scoop cat "+final_app_three)
                    powershell_cat_3 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_cat_command_3)]
                    powershell_do_cat_3 = subprocess.run(powershell_cat_3, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                     universal_newlines=True, shell="False")
                except:
                    pass

                try:
                    getting_stdout_3 = powershell_do_cat_3.stdout
                    splitting_stdout_3 = getting_stdout_3.split('\n')
                    app_desc_3 = splitting_stdout_3[2]

                    if 'version":' in app_desc_3:
                        app_desc_3 = splitting_stdout_3[3]

                    app_desc_3 = app_desc_3.strip(" ")
                    app_desc_3 = app_desc_3.strip('",')
                    app_desc_3 = app_desc_3.strip('description": ')

                except:
                    pass

                if successful_3:
                    self.install_search_app_btn_3.setText("install")

                try:
                    self.app_desc_3_lbl.setText(str(app_desc_3))
                    self.app_label_3.setText(str(final_app_three))
                except:
                    pass


            def app_desc_4_function():
                try:
                    scoop_cat_command_4 = ("scoop cat "+final_app_four)
                    powershell_cat_4 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_cat_command_4)]
                    powershell_do_cat_4 = subprocess.run(powershell_cat_4, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                     universal_newlines=True, shell="False")
                except:
                    pass

                try:
                    getting_stdout_4 = powershell_do_cat_4.stdout
                    splitting_stdout_4 = getting_stdout_4.split('\n')
                    app_desc_4 = splitting_stdout_4[2]

                    if 'version":' in app_desc_4:
                        app_desc_4 = splitting_stdout_4[3]

                    app_desc_4 = app_desc_4.strip(" ")
                    app_desc_4 = app_desc_4.strip('",')
                    app_desc_4 = app_desc_4.strip('description": ')

                except:
                    pass

                if successful_4:
                    self.install_search_app_btn_4.setText("install")

                try:
                    self.app_desc_4_lbl.setText(str(app_desc_4))
                    self.app_label_4.setText(str(final_app_four))
                except:
                    pass


            def app_desc_5_function():
                try:
                    scoop_cat_command_5 = ("scoop cat "+final_app_five)
                    powershell_cat_5 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_cat_command_5)]
                    powershell_do_cat_5 = subprocess.run(powershell_cat_5, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                     universal_newlines=True, shell="False")
                except:
                    pass

                try:
                    getting_stdout_5 = powershell_do_cat_5.stdout
                    splitting_stdout_5 = getting_stdout_5.split('\n')
                    app_desc_5 = splitting_stdout_5[2]

                    if 'version":' in app_desc_5:
                        app_desc_5 = splitting_stdout_5[3]

                    app_desc_5 = app_desc_5.strip(" ")
                    app_desc_5 = app_desc_5.strip('",')
                    app_desc_5 = app_desc_5.strip('description": ')

                except:
                    pass

                if successful_5:
                    self.install_search_app_btn_5.setText("install")

                try:
                    self.app_desc_5_lbl.setText(str(app_desc_5))
                    self.app_label_5.setText(str(final_app_five))
                except:
                    pass

            # setting previous app names to blank, so if the user searches again, it'll remove previous searches
            global final_app_one, final_app_two, final_app_three, final_app_four, final_app_five
            final_app_one = " "
            final_app_two = " "
            final_app_three = " "
            final_app_four = " "
            final_app_five = " "

            # getting search bar text
            search_bar_text = self.search_bar_input.text()

            # making scoop search command
            scoop_search_command = ("scoop-search " + str(search_bar_text))
            # notification.notify(
            #     title='Searching...',
            #     message='please wait',
            #     app_icon="fluorite.ico",
            #     timeout=10,)

            powershell_scoop_search_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_search_command)]
            powershell_scoop_search_2 = subprocess.run(powershell_scoop_search_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

            powershell_scoop_search_2 = str(powershell_scoop_search_2)
            split_result = powershell_scoop_search_2.split('\\n')

            split_result = str(split_result).split(',')

            del split_result[0]
            del split_result[0]
            del split_result[0]
            del split_result[0]
            del split_result[0]
            del split_result[0]

            # removing all items which don't contain a bracket
            # because apps have a bracket with the version beside em, so this'll remove all non-apps

            stringVal = '('
            simplified = [x for x in split_result if stringVal in x]

            # only keeping the left of the bracket, which is the appname
            try:
                final_app_one = (simplified[0].split("(")[0]).strip()
                final_app_one = final_app_one.strip("'")
                final_app_one = final_app_one.strip('"')
                final_app_one = final_app_one.strip(" ")
                successful_1 = True
            except:
                # if the try for finding the first app fails, then no apps were found, hence notifying the user
                self.app_desc_1_lbl.setText("no apps found")
                # then skipping the rest of the function
                return None

            try:
                final_app_two = (simplified[1].split("(")[0]).strip()
                final_app_two = final_app_two.strip("'")
                final_app_two = final_app_two.strip('"')
                final_app_two = final_app_two.strip(" ")
                # then adding text to install buttons if app exists for that row
                successful_2 = True
            except:
                successful_2 = False

            try:
                final_app_three = (simplified[2].split("(")[0]).strip()
                final_app_three = final_app_three.strip("'")
                final_app_three = final_app_three.strip('"')
                final_app_three = final_app_three.strip(" ")
                successful_3 = True
            except:
                successful_3 = False

            try:
                final_app_four = (simplified[3].split("(")[0]).strip()
                final_app_four = final_app_four.strip("'")
                final_app_four = final_app_four.strip('"')
                final_app_four = final_app_four.strip(" ")
                successful_4 = True
            except:
                successful_4 = False

            try:
                final_app_five = (simplified[4].split("(")[0]).strip()
                final_app_five = final_app_five.strip("'")
                final_app_five = final_app_five.strip('"')
                final_app_five = final_app_five.strip(" ")
                successful_5 = True
            except:
                successful_5 = False

            try:
                # making scoop install commands
                scoop_install_command_1 =  ("scoop install "+final_app_one)
                scoop_install_command_2 =  ("scoop install "+final_app_two)
                scoop_install_command_3 =  ("scoop install "+final_app_three)
                scoop_install_command_4 =  ("scoop install "+final_app_four)
                scoop_install_command_5 =  ("scoop install "+final_app_five)
            except:
                pass

            # getting app descriptions - to speed this part up as its quite slow, there'll be 5 threads, 1 for getting each app description
            t = Thread(target=app_desc_1_function)
            t.daemon = True
            t.start()

            z = Thread(target=app_desc_2_function)
            z.daemon = True
            z.start()

            x = Thread(target=app_desc_3_function)
            x.daemon = True
            x.start()

            y = Thread(target=app_desc_4_function)
            y.daemon = True
            y.start()

            c = Thread(target=app_desc_5_function)
            c.daemon = True
            c.start()

            def installed_app_notif_1():
                notification.notify(
                    title='Finished',
                    message='Installed app',
                    app_icon="fluorite.ico",
                    timeout=10,
                )

            # installing corresponding apps when install button is pressed
            def install_search_app_one():
                powershell_install_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_install_command_1)]
                powershell_do_install_1 = subprocess.run(powershell_install_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                universal_newlines=True, shell="False")
                installed_app_notif_1()

            def install_search_app_two():
                powershell_install_2 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_install_command_2)]
                powershell_do_install_2 = subprocess.run(powershell_install_2, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                universal_newlines=True, shell="False")
                installed_app_notif_1()

            def install_search_app_three():
                powershell_install_3 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_install_command_3)]
                powershell_do_install_3 = subprocess.run(powershell_install_3, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                universal_newlines=True, shell="False")
                installed_app_notif_1()

            def install_search_app_four():
                powershell_install_4 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_install_command_4)]
                powershell_do_install_4 = subprocess.run(powershell_install_4, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                universal_newlines=True, shell="False")
                installed_app_notif_1()

            def install_search_app_five():
                powershell_install_5 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_install_command_5)]
                powershell_do_install_5 = subprocess.run(powershell_install_5, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                universal_newlines=True, shell="False")
                installed_app_notif_1()

            def install_search_app_one_thread():
                t = Thread(target=install_search_app_one)
                t.daemon = True
                t.start()

            def install_search_app_two_thread():
                t = Thread(target=install_search_app_two)
                t.daemon = True
                t.start()

            def install_search_app_three_thread():
                t = Thread(target=install_search_app_three)
                t.daemon = True
                t.start()

            def install_search_app_four_thread():
                t = Thread(target=install_search_app_four)
                t.daemon = True
                t.start()

            def install_search_app_five_thread():
                t = Thread(target=install_search_app_five)
                t.daemon = True
                t.start()

            # connecting search page install buttons to install function
            self.install_search_app_btn_1.clicked.connect(lambda: install_search_app_one_thread())
            self.install_search_app_btn_2.clicked.connect(lambda: install_search_app_two_thread())
            self.install_search_app_btn_3.clicked.connect(lambda: install_search_app_three_thread())
            self.install_search_app_btn_4.clicked.connect(lambda: install_search_app_four_thread())
            self.install_search_app_btn_5.clicked.connect(lambda: install_search_app_five_thread())

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # VIRUS TOTAL APP CHECKING                            #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        def app_is_safe_notif():
            notification.notify(
                title='App is Safe',
                message='no malware detections found from 58 sources - VirusTotal',
                app_icon="fluorite.ico",
                timeout=10,
            )


        def vt_function_1():
            vt_command_1 = ("scoop virustotal "+final_app_one)
            vt_ps_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (vt_command_1)]
            vt_do_ps_1 = subprocess.run(vt_ps_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

            vt_output = vt_do_ps_1.stdout
            vt_output = vt_output.split(" ")

            # checking for WARN word, if it exists then vt returned at least 1 detection and the virustotal link is opened in a browser for the user to check
            # else its safe
            if vt_output[0] == "WARN":
                vt_output_url = vt_output[5]
                webbrowser.open(vt_output_url)
            else:
                app_is_safe_notif()


        def vt_function_2():
            vt_command_1 = ("scoop virustotal "+final_app_two)
            vt_ps_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (vt_command_1)]
            vt_do_ps_1 = subprocess.run(vt_ps_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

            vt_output = vt_do_ps_1.stdout
            vt_output = vt_output.split(" ")

            # checking for WARN word, if it exists then vt returned at least 1 detection and the virustotal link is opened in a browser for the user to check
            # else its safe
            if vt_output[0] == "WARN":
                vt_output_url = vt_output[5]
                webbrowser.open(vt_output_url)
            else:
                app_is_safe_notif()

        def vt_function_3():
            vt_command_1 = ("scoop virustotal "+final_app_three)
            vt_ps_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (vt_command_1)]
            vt_do_ps_1 = subprocess.run(vt_ps_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

            vt_output = vt_do_ps_1.stdout
            vt_output = vt_output.split(" ")

            # checking for WARN word, if it exists then vt returned at least 1 detection and the virustotal link is opened in a browser for the user to check
            # else its safe
            if vt_output[0] == "WARN":
                vt_output_url = vt_output[5]
                webbrowser.open(vt_output_url)
            else:
                app_is_safe_notif()

        def vt_function_4():
            vt_command_1 = ("scoop virustotal "+final_app_four)
            vt_ps_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (vt_command_1)]
            vt_do_ps_1 = subprocess.run(vt_ps_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

            vt_output = vt_do_ps_1.stdout
            vt_output = vt_output.split(" ")

            # checking for WARN word, if it exists then vt returned at least 1 detection and the virustotal link is opened in a browser for the user to check
            # else its safe
            if vt_output[0] == "WARN":
                vt_output_url = vt_output[5]
                webbrowser.open(vt_output_url)
            else:
                app_is_safe_notif()

        def vt_function_5():
            vt_command_1 = ("scoop virustotal "+final_app_five)
            vt_ps_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (vt_command_1)]
            vt_do_ps_1 = subprocess.run(vt_ps_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

            vt_output = vt_do_ps_1.stdout
            vt_output = vt_output.split(" ")

            # checking for WARN word, if it exists then vt returned at least 1 detection and the virustotal link is opened in a browser for the user to check
            # else its safe
            if vt_output[0] == "WARN":
                vt_output_url = vt_output[5]
                webbrowser.open(vt_output_url)
            else:
                app_is_safe_notif()


        def remove_app_function():
            remove_app_input_text = self.apps_list.currentText()

            # making scoop remove command
            scoop_remove_command = ("scoop uninstall " + str(remove_app_input_text))

            powershell_scoop_remove_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', (scoop_remove_command)]
            powershell_scoop_remove_2 = subprocess.run(powershell_scoop_remove_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

            notification.notify(
                title='Finished',
                message='uninstalled app',
                app_icon="fluorite.ico",
                timeout=10,
            )

        def remove_app_function_thread():
            t = Thread(target=remove_app_function)
            t.daemon = True
            t.start()

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # INSTALL BUTTONS ON SEARCH PAGE                         #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        # making search page install buttons and adding to layout
        self.install_search_app_btn_1 = custompushbutton('install', parent=self)
        self.install_search_app_btn_1.setMinimumHeight(51)
        self.install_search_app_btn_1.setFixedWidth(101)

        self.install_search_app_btn_2 = custompushbutton('install', parent=self)
        self.install_search_app_btn_2.setMinimumHeight(51)
        self.install_search_app_btn_2.setFixedWidth(101)

        self.install_search_app_btn_3 = custompushbutton('install', parent=self)
        self.install_search_app_btn_3.setMinimumHeight(51)
        self.install_search_app_btn_3.setFixedWidth(101)

        self.install_search_app_btn_4 = custompushbutton('install', parent=self)
        self.install_search_app_btn_4.setMinimumHeight(51)
        self.install_search_app_btn_4.setFixedWidth(101)

        self.install_search_app_btn_5 = custompushbutton('install', parent=self)
        self.install_search_app_btn_5.setMinimumHeight(51)
        self.install_search_app_btn_5.setFixedWidth(101)

        self.app_install_1_layout.addWidget(self.install_search_app_btn_1, Qt.AlignCenter, Qt.AlignCenter)
        self.app_install_2_layout.addWidget(self.install_search_app_btn_2, Qt.AlignCenter, Qt.AlignCenter)
        self.app_install_3_layout.addWidget(self.install_search_app_btn_3, Qt.AlignCenter, Qt.AlignCenter)
        self.app_install_4_layout.addWidget(self.install_search_app_btn_4, Qt.AlignCenter, Qt.AlignCenter)
        self.app_install_5_layout.addWidget(self.install_search_app_btn_5, Qt.AlignCenter, Qt.AlignCenter)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # REMOVE APP AND INPUT BOX                            #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.remove_app_button = custompushbutton('Remove App (click)', parent=self)
        self.remove_app_button.setMinimumHeight(61)
        self.remove_app_button.setFixedWidth(131)

        self.remove_app_button_layout.addWidget(self.remove_app_button, Qt.AlignCenter, Qt.AlignCenter)
        self.remove_app_button.clicked.connect(lambda: remove_app_function_thread())



        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # SEARCH BAR & SEARCH BUTTON                          #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.enter_search_term_button = custompushbutton('Enter', parent=self)
        self.enter_search_term_button.setMinimumHeight(51)
        self.enter_search_term_button.setFixedWidth(91)

        self.enter_search_term_layout.addWidget(self.enter_search_term_button, Qt.AlignCenter, Qt.AlignCenter)
        self.enter_search_term_button.clicked.connect(lambda: threaded_do_search())
        self.search_bar_input.returnPressed.connect(lambda: threaded_do_search())

        def threaded_do_search():
            t = Thread(target=do_search)
            t.daemon = True
            t.start()

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # STATUS INDICATOR                                    #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        self.status_indicator_1 = QLabel("", parent=self)
        self.status_indicator_2 = QLabel("", parent=self)
        self.status_indicator_3 = QLabel("", parent=self)
        self.status_indicator_4 = QLabel("", parent=self)
        self.status_indicator_5 = QLabel("", parent=self)
        self.status_indicator_6 = QLabel("", parent=self)

        # bucket add or remove status indicator
        self.status_indicator_bucket= QLabel("", parent=self)

        self.status_indicator_layout_1.addWidget(self.status_indicator_1, Qt.AlignCenter, Qt.AlignCenter)
        self.status_indicator_layout_2.addWidget(self.status_indicator_2, Qt.AlignCenter, Qt.AlignCenter)
        self.status_indicator_layout_3.addWidget(self.status_indicator_3, Qt.AlignCenter, Qt.AlignCenter)
        self.status_indicator_layout_4.addWidget(self.status_indicator_4, Qt.AlignCenter, Qt.AlignCenter)
        self.status_indicator_layout_5.addWidget(self.status_indicator_5, Qt.AlignCenter, Qt.AlignCenter)
        self.status_indicator_layout_6.addWidget(self.status_indicator_6, Qt.AlignCenter, Qt.AlignCenter)

        self.status_indicator_layout_buckets.addWidget(self.status_indicator_bucket, Qt.AlignCenter, Qt.AlignCenter)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # NEXT PAGE BUTTON - STARRED/RECOMMENDED APPS PAGE    #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        # defining the button
        self.starred_next_page_1 = custompushbutton('N\ne\nx\nt\n\nP\na\ng\ne', parent=self)
        self.starred_next_page_1.setMinimumHeight(241)
        self.starred_next_page_1.setFixedWidth(51)

        self.starred_next_page_2 = custompushbutton('N\ne\nx\nt\n\nP\na\ng\ne', parent=self)
        self.starred_next_page_2.setMinimumHeight(241)
        self.starred_next_page_2.setFixedWidth(51)

        self.starred_next_page_3 = custompushbutton('N\ne\nx\nt\n\nP\na\ng\ne', parent=self)
        self.starred_next_page_3.setMinimumHeight(241)
        self.starred_next_page_3.setFixedWidth(51)

        self.starred_next_page_4 = custompushbutton('N\ne\nx\nt\n\nP\na\ng\ne', parent=self)
        self.starred_next_page_4.setMinimumHeight(241)
        self.starred_next_page_4.setFixedWidth(51)

        self.starred_next_page_5 = custompushbutton('N\ne\nx\nt\n\nP\na\ng\ne', parent=self)
        self.starred_next_page_5.setMinimumHeight(241)
        self.starred_next_page_5.setFixedWidth(51)

        # Adding back button to layout
        self.recc_next_page_layout_1.addWidget(self.starred_next_page_1, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_next_page_layout_two.addWidget(self.starred_next_page_2, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_next_page_layout_3.addWidget(self.starred_next_page_3, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_next_page_layout_4.addWidget(self.starred_next_page_4, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_next_page_layout_5.addWidget(self.starred_next_page_5, Qt.AlignCenter, Qt.AlignCenter)

        # connecting back button to function
        self.starred_next_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_2))
        self.starred_next_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_3))
        self.starred_next_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_4))
        self.starred_next_page_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_5))
        self.starred_next_page_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_6))


        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # BACK BUTTON - RETURNING TO HOMEPAGE                 #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        # defining the button
        self.return_home = custompushbutton('Back', parent=self)
        self.return_home.setMinimumHeight(61)
        self.return_home.setFixedWidth(261)

        self.return_home_1 = custompushbutton('H\no\nm\ne', parent=self)
        self.return_home_1.setMinimumHeight(181)
        self.return_home_1.setFixedWidth(51)

        self.return_home_2 = custompushbutton('B\na\nc\nk', parent=self)
        self.return_home_2.setMinimumHeight(181)
        self.return_home_2.setFixedWidth(51)

        self.return_home_3 = custompushbutton('B\na\nc\nk', parent=self)
        self.return_home_3.setMinimumHeight(181)
        self.return_home_3.setFixedWidth(51)

        self.return_home_4 = custompushbutton('B\na\nc\nk', parent=self)
        self.return_home_4.setMinimumHeight(181)
        self.return_home_4.setFixedWidth(51)

        self.return_home_5 = custompushbutton('B\na\nc\nk', parent=self)
        self.return_home_5.setMinimumHeight(181)
        self.return_home_5.setFixedWidth(51)

        self.return_home_6 = custompushbutton('B\na\nc\nk', parent=self)
        self.return_home_6.setMinimumHeight(181)
        self.return_home_6.setFixedWidth(51)

        self.return_home_7 = custompushbutton('Back', parent=self)
        self.return_home_7.setMinimumHeight(61)
        self.return_home_7.setFixedWidth(261)

        # return home page button on search page#
        self.back_search_page = custompushbutton('Home', parent=self)
        self.back_search_page.setMinimumHeight(51)
        self.back_search_page.setFixedWidth(131)

        # Adding back button to layout
        self.bucket_back_layout.addWidget(self.return_home, Qt.AlignCenter, Qt.AlignCenter)

        self.return_home_layout_settings.addWidget(self.return_home, Qt.AlignCenter, Qt.AlignCenter)

        self.back_search_page_layout.addWidget(self.back_search_page, Qt.AlignCenter, Qt.AlignCenter)

        self.return_home_layout_1.addWidget(self.return_home_1, Qt.AlignCenter, Qt.AlignCenter)
        self.return_home_layout_two.addWidget(self.return_home_2, Qt.AlignCenter, Qt.AlignCenter)
        self.return_home_layout_3.addWidget(self.return_home_3, Qt.AlignCenter, Qt.AlignCenter)
        self.return_home_layout_4.addWidget(self.return_home_4, Qt.AlignCenter, Qt.AlignCenter)
        self.return_home_layout_5.addWidget(self.return_home_5, Qt.AlignCenter, Qt.AlignCenter)
        self.return_home_layout_6.addWidget(self.return_home_6, Qt.AlignCenter, Qt.AlignCenter)

        self.bucket_back_layout.addWidget(self.return_home_7, Qt.AlignCenter, Qt.AlignCenter)

        # connecting back button to function
        self.return_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home))

        self.back_search_page.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home))

        self.return_home_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home))
        self.return_home_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_1))
        self.return_home_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_2))
        self.return_home_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_3))
        self.return_home_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_4))
        self.return_home_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.recommended_apps_page_5))

        self.return_home_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home))

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # DESCRIPTION LABELS ON SEARCH APPS PAGE             #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        self.app_desc_1_lbl = QLabel("", parent=self)
        self.app_desc_2_lbl = QLabel("", parent=self)
        self.app_desc_3_lbl = QLabel("", parent=self)
        self.app_desc_4_lbl = QLabel("", parent=self)
        self.app_desc_5_lbl = QLabel("", parent=self)

        self.app_desc_1_layout.addWidget(self.app_desc_1_lbl, Qt.AlignCenter, Qt.AlignCenter)
        self.app_desc_2_layout.addWidget(self.app_desc_2_lbl, Qt.AlignCenter, Qt.AlignCenter)
        self.app_desc_3_layout.addWidget(self.app_desc_3_lbl, Qt.AlignCenter, Qt.AlignCenter)
        self.app_desc_4_layout.addWidget(self.app_desc_4_lbl, Qt.AlignCenter, Qt.AlignCenter)
        self.app_desc_5_layout.addWidget(self.app_desc_5_lbl, Qt.AlignCenter, Qt.AlignCenter)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # INSTALL BUTTONS PAGE  1  - STARRED APPS             #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.recc_app_install_button_1 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_1.setMinimumHeight(71)
        self.recc_app_install_button_1.setFixedWidth(131)

        self.recc_app_install_button_2 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_2.setMinimumHeight(71)
        self.recc_app_install_button_2.setFixedWidth(131)

        self.recc_app_install_button_3 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_3.setMinimumHeight(71)
        self.recc_app_install_button_3.setFixedWidth(131)

        self.recc_app_install_button_4 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_4.setMinimumHeight(71)
        self.recc_app_install_button_4.setFixedWidth(131)

        self.recc_app_install_button_5 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_5.setMinimumHeight(71)
        self.recc_app_install_button_5.setFixedWidth(131)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # INSTALL BUTTONS PAGE  2  - STARRED APPS             #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.recc_app_install_button_6 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_6.setMinimumHeight(71)
        self.recc_app_install_button_6.setFixedWidth(131)

        self.recc_app_install_button_7 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_7.setMinimumHeight(71)
        self.recc_app_install_button_7.setFixedWidth(131)

        self.recc_app_install_button_8 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_8.setMinimumHeight(71)
        self.recc_app_install_button_8.setFixedWidth(131)

        self.recc_app_install_button_9 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_9.setMinimumHeight(71)
        self.recc_app_install_button_9.setFixedWidth(131)

        self.recc_app_install_button_10 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_10.setMinimumHeight(71)
        self.recc_app_install_button_10.setFixedWidth(131)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # INSTALL BUTTONS PAGE  3  - STARRED APPS             #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.recc_app_install_button_11 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_11.setMinimumHeight(71)
        self.recc_app_install_button_11.setFixedWidth(131)

        self.recc_app_install_button_12 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_12.setMinimumHeight(71)
        self.recc_app_install_button_12.setFixedWidth(131)

        self.recc_app_install_button_13 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_13.setMinimumHeight(71)
        self.recc_app_install_button_13.setFixedWidth(131)

        self.recc_app_install_button_14 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_14.setMinimumHeight(71)
        self.recc_app_install_button_14.setFixedWidth(131)

        self.recc_app_install_button_15 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_15.setMinimumHeight(71)
        self.recc_app_install_button_15.setFixedWidth(131)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # INSTALL BUTTONS PAGE  4  - STARRED APPS             #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.recc_app_install_button_16 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_16.setMinimumHeight(71)
        self.recc_app_install_button_16.setFixedWidth(131)

        self.recc_app_install_button_17 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_17.setMinimumHeight(71)
        self.recc_app_install_button_17.setFixedWidth(131)

        self.recc_app_install_button_18 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_18.setMinimumHeight(71)
        self.recc_app_install_button_18.setFixedWidth(131)

        self.recc_app_install_button_19 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_19.setMinimumHeight(71)
        self.recc_app_install_button_19.setFixedWidth(131)

        self.recc_app_install_button_20 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_20.setMinimumHeight(71)
        self.recc_app_install_button_20.setFixedWidth(131)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # INSTALL BUTTONS PAGE  5  - STARRED APPS             #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.recc_app_install_button_21 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_21.setMinimumHeight(71)
        self.recc_app_install_button_21.setFixedWidth(131)

        self.recc_app_install_button_22 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_22.setMinimumHeight(71)
        self.recc_app_install_button_22.setFixedWidth(131)

        self.recc_app_install_button_23 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_23.setMinimumHeight(71)
        self.recc_app_install_button_23.setFixedWidth(131)

        self.recc_app_install_button_24 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_24.setMinimumHeight(71)
        self.recc_app_install_button_24.setFixedWidth(131)

        self.recc_app_install_button_25 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_25.setMinimumHeight(71)
        self.recc_app_install_button_25.setFixedWidth(131)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # INSTALL BUTTONS PAGE  6  - STARRED APPS             #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.recc_app_install_button_26 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_26.setMinimumHeight(71)
        self.recc_app_install_button_26.setFixedWidth(131)

        self.recc_app_install_button_27 = custompushbutton('Install', parent=self)
        self.recc_app_install_button_27.setMinimumHeight(71)
        self.recc_app_install_button_27.setFixedWidth(131)

        # self.recc_app_install_button_28 = custompushbutton('Install', parent=self)
        # self.recc_app_install_button_28.setMinimumHeight(71)
        # self.recc_app_install_button_28.setFixedWidth(131)
        #
        # self.recc_app_install_button_29 = custompushbutton('Install', parent=self)
        # self.recc_app_install_button_29.setMinimumHeight(71)
        # self.recc_app_install_button_29.setFixedWidth(131)
        #
        # self.recc_app_install_button_30 = custompushbutton('Install', parent=self)
        # self.recc_app_install_button_30.setMinimumHeight(71)
        # self.recc_app_install_button_30.setFixedWidth(131)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # VIRUS TOTAL BUTTON NEXT TO EACH APP                #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        self.vt_btn_1 = custompushbutton('check', parent=self)
        self.vt_btn_1.setMinimumHeight(71)
        self.vt_btn_1.setFixedWidth(91)

        self.vt_btn_2 = custompushbutton('check', parent=self)
        self.vt_btn_2.setMinimumHeight(71)
        self.vt_btn_2.setFixedWidth(91)

        self.vt_btn_3 = custompushbutton('check', parent=self)
        self.vt_btn_3.setMinimumHeight(71)
        self.vt_btn_3.setFixedWidth(91)

        self.vt_btn_4 = custompushbutton('check', parent=self)
        self.vt_btn_4.setMinimumHeight(71)
        self.vt_btn_4.setFixedWidth(91)

        self.vt_btn_5 = custompushbutton('check', parent=self)
        self.vt_btn_5.setMinimumHeight(71)
        self.vt_btn_5.setFixedWidth(91)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # ATTACHING VIRUS TOTAL BUTTONS TO LAYOUT             #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        self.vt_button_1_layout.addWidget(self.vt_btn_1, Qt.AlignCenter, Qt.AlignCenter)
        self.vt_button_2_layout.addWidget(self.vt_btn_2, Qt.AlignCenter, Qt.AlignCenter)
        self.vt_button_3_layout.addWidget(self.vt_btn_3, Qt.AlignCenter, Qt.AlignCenter)
        self.vt_button_4_layout.addWidget(self.vt_btn_4, Qt.AlignCenter, Qt.AlignCenter)
        self.vt_button_5_layout.addWidget(self.vt_btn_5, Qt.AlignCenter, Qt.AlignCenter)

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # CONNECTING VIRUS TOTAL BUTTONS TO THEIR FUNCTIONS   #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        self.vt_btn_1.clicked.connect(lambda: vt_function_1())
        self.vt_btn_2.clicked.connect(lambda: vt_function_2())
        self.vt_btn_3.clicked.connect(lambda: vt_function_3())
        self.vt_btn_4.clicked.connect(lambda: vt_function_4())
        self.vt_btn_5.clicked.connect(lambda: vt_function_5())

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        # ATTACHING STARRED INSTALL BUTTONS TO LAYOUT         #
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        # attaching page 1 buttons to layouts
        self.recc_app_install_layout_1.addWidget(self.recc_app_install_button_1, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_2.addWidget(self.recc_app_install_button_2, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_3.addWidget(self.recc_app_install_button_3, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_4.addWidget(self.recc_app_install_button_4, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_5.addWidget(self.recc_app_install_button_5, Qt.AlignCenter, Qt.AlignCenter)

        # attaching page 2 buttons to layouts
        self.recc_app_install_layout_6.addWidget(self.recc_app_install_button_6, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_7.addWidget(self.recc_app_install_button_7, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_8.addWidget(self.recc_app_install_button_8, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_9.addWidget(self.recc_app_install_button_9, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_10.addWidget(self.recc_app_install_button_10, Qt.AlignCenter, Qt.AlignCenter)

        # attaching page 3 buttons to layouts
        self.recc_app_install_layout_11.addWidget(self.recc_app_install_button_11, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_12.addWidget(self.recc_app_install_button_12, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_13.addWidget(self.recc_app_install_button_13, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_14.addWidget(self.recc_app_install_button_14, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_15.addWidget(self.recc_app_install_button_15, Qt.AlignCenter, Qt.AlignCenter)

        # attaching page 4 buttons to layouts
        self.recc_app_install_layout_16.addWidget(self.recc_app_install_button_16, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_17.addWidget(self.recc_app_install_button_17, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_18.addWidget(self.recc_app_install_button_18, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_19.addWidget(self.recc_app_install_button_19, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_20.addWidget(self.recc_app_install_button_20, Qt.AlignCenter, Qt.AlignCenter)

        # attaching page 5 buttons to layouts
        self.recc_app_install_layout_1_21.addWidget(self.recc_app_install_button_21, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_1_22.addWidget(self.recc_app_install_button_22, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_1_23.addWidget(self.recc_app_install_button_23, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_1_24.addWidget(self.recc_app_install_button_24, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_1_25.addWidget(self.recc_app_install_button_25, Qt.AlignCenter, Qt.AlignCenter)

        # attaching page 6 buttons to layouts
        self.recc_app_install_layout_1_26.addWidget(self.recc_app_install_button_26, Qt.AlignCenter, Qt.AlignCenter)
        self.recc_app_install_layout_1_27.addWidget(self.recc_app_install_button_27, Qt.AlignCenter, Qt.AlignCenter)

        # functions for installing recommended apps on button click

        def installed_app_notif():
            notification.notify(
                title='Finished',
                message='Installed app',
                app_icon="fluorite.ico",
                timeout=10,
            )

        def install_recc_app_1():
            # toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install hwinfo']
            # process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            #                                 universal_newlines=True, shell="False")
            print ("unfortunately portmaster isn't on scoop yet, so i'll have to find some other way to install this later. Coming soon..")
            installed_app_notif()

        def install_recc_app_2():
            self.status_indicator_1.setText("Installing... fluent-reader")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install fluent-reader']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_1.setText("Installed")
            installed_app_notif()

        def install_recc_app_3():
            self.status_indicator_1.setText("Installing... flameshot")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install flameshot']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_1.setText("Installed")
            installed_app_notif()

        def install_recc_app_4():
            self.status_indicator_1.setText("Installing... ludusavi")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install ludusavi']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_1.setText("Installed")
            installed_app_notif()

        def install_recc_app_5():
            self.status_indicator_1.setText("Installing... compactgui")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install compactgui']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_1.setText("Installed")
            installed_app_notif()

        def install_recc_app_6():
            self.status_indicator_2.setText("Installing... peazip")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install peazip']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_2.setText("Installed")
            installed_app_notif()

        def install_recc_app_7():
            self.status_indicator_2.setText("Installing... librewolf")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install librewolf']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_2.setText("Installed")
            installed_app_notif()

        def install_recc_app_8():
            self.status_indicator_2.setText("Installing... freetube")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install freetube']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_2.setText("Installed")
            installed_app_notif()

        def install_recc_app_9():
            self.status_indicator_2.setText("Installing... geekuninstaller")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install geekuninstaller']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_2.setText("Installed")
            installed_app_notif()

        def install_recc_app_10():
            self.status_indicator_2.setText("Installing... simplewall")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install simplewall']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_2.setText("Installed")
            installed_app_notif()

        def install_recc_app_11():
            self.status_indicator_3.setText("Installing... sandboxie-plus-np")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install sandboxie-plus-np']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_3.setText("Installed")
            installed_app_notif()

        def install_recc_app_12():
            self.status_indicator_3.setText("Installing... playnite")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install playnite']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_3.setText("Installed")
            installed_app_notif()

        def install_recc_app_13():
            self.status_indicator_3.setText("Installing... crystaldiskinfo")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install crystaldiskinfo']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_3.setText("Installed")
            installed_app_notif()

        def install_recc_app_14():
            self.status_indicator_3.setText("Installing... hwinfo")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install hwinfo']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_3.setText("Installed")
            installed_app_notif()

        def install_recc_app_15():
            # toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install hwinfo']
            # process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            #                                 universal_newlines=True, shell="False")
            self.status_indicator_3.setText("OOCT is unavaliable")
            print(
                "unfortunately OCCT isn't on scoop yet, so i'll have to find some other way to install this later. Coming soon..")
            installed_app_notif()

        def install_recc_app_16():
            self.status_indicator_4.setText("Installing... shutup10")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install shutup10']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_4.setText("Installed")
            installed_app_notif()

        def install_recc_app_17():
            self.status_indicator_4.setText("Installing... mpv")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install mpv']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_4.setText("Installed")
            installed_app_notif()

        def install_recc_app_18():
            self.status_indicator_4.setText("Installing... tabby")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install tabby']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_4.setText("Installed")
            installed_app_notif()

        def install_recc_app_19():
            self.status_indicator_4.setText("Installing... eartrumpet")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install eartrumpet']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_4.setText("Installed")
            installed_app_notif()

        def install_recc_app_20():
            self.status_indicator_4.setText("Installing... ryujinx")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install ryujinx']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_4.setText("Installed")
            installed_app_notif()

        def install_recc_app_21():
            self.status_indicator_5.setText("Installing... modernflouts")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install modernflyouts']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_5.setText("Installed")
            installed_app_notif()

        def install_recc_app_22():
            self.status_indicator_5.setText("Installing... espanso-pre")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install espanso-pre']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_5.setText("Installed")
            installed_app_notif()

        def install_recc_app_23():
            self.status_indicator_5.setText("Installing... lively-wallpaper")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop bucket add HUMORCE_nuke https://github.com/HUMORCE/nuke; scoop install lively-wallpaper']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_5.setText("Installed")
            installed_app_notif()

        def install_recc_app_24():
            self.status_indicator_5.setText("Installing... obsidian")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install obsidian']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_5.setText("Installed")
            installed_app_notif()

        def install_recc_app_25():
            self.status_indicator_5.setText("Installing... snappy-driver-installer-origin")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install snappy-driver-installer-origin']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_5.setText("Installed")
            installed_app_notif()

        def install_recc_app_26():
            self.status_indicator_6.setText("Installing... Fancontrol-Portable")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', "scoop bucket add ACooper81_scoop-apps https://github.com/ACooper81/scoop-apps; scoop install FanControl-Portable"]
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_6.setText("Installed")
            installed_app_notif()

        def install_recc_app_27():
            self.status_indicator_6.setText("Installing... openrgb")
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install openrgb']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            self.status_indicator_6.setText("Installed")
            installed_app_notif()


        # launching install functions in seperate thread = no gui hang
        def thread_install_recc_app_1():
            t = Thread(target=install_recc_app_1)
            t.daemon = True
            t.start()

        def thread_install_recc_app_2():
            t = Thread(target=install_recc_app_2)
            t.daemon = True
            t.start()

        def thread_install_recc_app_3():
            t = Thread(target=install_recc_app_3)
            t.daemon = True
            t.start()

        def thread_install_recc_app_4():
            t = Thread(target=install_recc_app_4)
            t.daemon = True
            t.start()

        def thread_install_recc_app_5():
            t = Thread(target=install_recc_app_5)
            t.daemon = True
            t.start()

        def thread_install_recc_app_6():
            t = Thread(target=install_recc_app_6)
            t.daemon = True
            t.start()

        def thread_install_recc_app_7():
            t = Thread(target=install_recc_app_7)
            t.daemon = True
            t.start()

        def thread_install_recc_app_8():
            t = Thread(target=install_recc_app_8)
            t.daemon = True
            t.start()

        def thread_install_recc_app_9():
            t = Thread(target=install_recc_app_9)
            t.daemon = True
            t.start()

        def thread_install_recc_app_10():
            t = Thread(target=install_recc_app_10)
            t.daemon = True
            t.start()

        def thread_install_recc_app_11():
            t = Thread(target=install_recc_app_11)
            t.daemon = True
            t.start()

        def thread_install_recc_app_12():
            t = Thread(target=install_recc_app_12)
            t.daemon = True
            t.start()

        def thread_install_recc_app_13():
            t = Thread(target=install_recc_app_13)
            t.daemon = True
            t.start()

        def thread_install_recc_app_14():
            t = Thread(target=install_recc_app_14)
            t.daemon = True
            t.start()

        def thread_install_recc_app_15():
            t = Thread(target=install_recc_app_15)
            t.daemon = True
            t.start()

        def thread_install_recc_app_16():
            t = Thread(target=install_recc_app_16)
            t.daemon = True
            t.start()

        def thread_install_recc_app_17():
            t = Thread(target=install_recc_app_17)
            t.daemon = True
            t.start()

        def thread_install_recc_app_18():
            t = Thread(target=install_recc_app_18)
            t.daemon = True
            t.start()

        def thread_install_recc_app_19():
            t = Thread(target=install_recc_app_19)
            t.daemon = True
            t.start()

        def thread_install_recc_app_20():
            t = Thread(target=install_recc_app_20)
            t.daemon = True
            t.start()

        def thread_install_recc_app_21():
            t = Thread(target=install_recc_app_21)
            t.daemon = True
            t.start()

        def thread_install_recc_app_22():
            t = Thread(target=install_recc_app_22)
            t.daemon = True
            t.start()

        def thread_install_recc_app_23():
            t = Thread(target=install_recc_app_23)
            t.daemon = True
            t.start()

        def thread_install_recc_app_24():
            t = Thread(target=install_recc_app_24)
            t.daemon = True
            t.start()

        def thread_install_recc_app_25():
            t = Thread(target=install_recc_app_25)
            t.daemon = True
            t.start()

        def thread_install_recc_app_26():
            t = Thread(target=install_recc_app_26)
            t.daemon = True
            t.start()

        def thread_install_recc_app_27():
            t = Thread(target=install_recc_app_27)
            t.daemon = True
            t.start()


        def do_nothing():
            print ("coming soon")

        # attaching all 20 to functions
        # currently do nothing
        self.recc_app_install_button_1.clicked.connect(lambda: thread_install_recc_app_1())
        self.recc_app_install_button_2.clicked.connect(lambda: thread_install_recc_app_2())
        self.recc_app_install_button_3.clicked.connect(lambda: thread_install_recc_app_3())
        self.recc_app_install_button_4.clicked.connect(lambda: thread_install_recc_app_4())
        self.recc_app_install_button_5.clicked.connect(lambda: thread_install_recc_app_5())
        self.recc_app_install_button_6.clicked.connect(lambda: thread_install_recc_app_6())
        self.recc_app_install_button_7.clicked.connect(lambda: thread_install_recc_app_7())
        self.recc_app_install_button_8.clicked.connect(lambda: thread_install_recc_app_8())
        self.recc_app_install_button_9.clicked.connect(lambda: thread_install_recc_app_9())
        self.recc_app_install_button_10.clicked.connect(lambda: thread_install_recc_app_10())
        self.recc_app_install_button_11.clicked.connect(lambda: thread_install_recc_app_11())
        self.recc_app_install_button_12.clicked.connect(lambda: thread_install_recc_app_12())
        self.recc_app_install_button_13.clicked.connect(lambda: thread_install_recc_app_13())
        self.recc_app_install_button_14.clicked.connect(lambda: thread_install_recc_app_14())
        self.recc_app_install_button_15.clicked.connect(lambda: thread_install_recc_app_15())
        self.recc_app_install_button_16.clicked.connect(lambda: thread_install_recc_app_16())
        self.recc_app_install_button_17.clicked.connect(lambda: thread_install_recc_app_17())
        self.recc_app_install_button_18.clicked.connect(lambda: thread_install_recc_app_18())
        self.recc_app_install_button_19.clicked.connect(lambda: thread_install_recc_app_19())
        self.recc_app_install_button_20.clicked.connect(lambda: thread_install_recc_app_20())
        self.recc_app_install_button_21.clicked.connect(lambda: thread_install_recc_app_21())
        self.recc_app_install_button_22.clicked.connect(lambda: thread_install_recc_app_22())
        self.recc_app_install_button_23.clicked.connect(lambda: thread_install_recc_app_23())
        self.recc_app_install_button_24.clicked.connect(lambda: thread_install_recc_app_24())
        self.recc_app_install_button_25.clicked.connect(lambda: thread_install_recc_app_25())
        self.recc_app_install_button_26.clicked.connect(lambda: thread_install_recc_app_26())
        self.recc_app_install_button_27.clicked.connect(lambda: thread_install_recc_app_27())

        ###################################################################################################################
        # BUCKETS AND APPS PAGE
        ###################################################################################################################
        self.update_all_apps_button = QtWidgets.QPushButton('update', parent=self)
        self.update_all_apps_button.setMinimumHeight(61)
        self.update_all_apps_button.setFixedWidth(251)
        self.cleanup_old_app_versions_button = QtWidgets.QPushButton('cleanup', parent=self)
        self.cleanup_old_app_versions_button.setMinimumHeight(61)
        self.cleanup_old_app_versions_button.setFixedWidth(251)

        # adding widgets to layout
        self.update_all_apps_layout.addWidget(self.update_all_apps_button, Qt.AlignCenter, Qt.AlignCenter)
        self.cleanup_old_app_versions_layout.addWidget(self.cleanup_old_app_versions_button, Qt.AlignCenter, Qt.AlignCenter)

        # updating all apps function
        self.update_all_apps_button.clicked.connect(self.update_all_apps_thread)
        self.cleanup_old_app_versions_button.clicked.connect(self.cleanup_old_app_versions_thread)

        # settings page
        self.settings_page_button = custompushbutton('Settings', parent=self)
        self.settings_page_button.setMinimumHeight(91)
        self.settings_page_button.setFixedWidth(251)
        self.settings_page_layout.addWidget(self.settings_page_button, Qt.AlignCenter, Qt.AlignCenter)
        self.settings_page_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.settings_page) )

        # manage buckets button on home page
        self.manage_buckets_button = custompushbutton('Manage', parent=self)
        self.manage_buckets_button.setMinimumHeight(91)
        self.manage_buckets_button.setFixedWidth(251)
        self.enter_manage_buckets_layout.addWidget(self.manage_buckets_button, Qt.AlignCenter, Qt.AlignCenter)

        # search page button on home page
        self.search_page_button = custompushbutton('Search', parent=self)
        self.search_page_button.setMinimumHeight(91)
        self.search_page_button.setFixedWidth(251)
        self.enter_search_layout.addWidget(self.search_page_button, Qt.AlignCenter, Qt.AlignCenter)

        self.search_page_button.clicked.connect(self.goSearch)
        self.manage_buckets_button.clicked.connect(self.goBuckets)

        # Back button on Search page
        self.search_back_button = custompushbutton('B\na\nc\nk', parent=self)
        self.search_back_button.setMinimumHeight(121)
        self.search_back_button.setFixedWidth(61)
        self.back_button_search_layout.addWidget(self.search_back_button, Qt.AlignCenter, Qt.AlignCenter)

        self.search_back_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home))

        ###################################################################################################################
        # SETTINGS PAGE
        ###################################################################################################################

        self.other_toggle = PyToggle(
            width=50
        )

        # the other 2 toggles don't do anything, yet, placeholders.
        self.download_manager_toggle = PyToggle(
            width=50
        )

        self.a_thing = PyToggle(
            width=50
        )

        with open('downloadmanager.txt', 'r') as file:
            dmToggled = file.read()
            dmToggled = str(dmToggled)
            if dmToggled == str(1):
                self.download_manager_toggle.setChecked(True)
            else:
                self.download_manager_toggle.setChecked(False)

        # adding widgets to layout
        self.settings_toggle_1_layout.addWidget(self.other_toggle, Qt.AlignCenter, Qt.AlignCenter)
        self.settings_toggle_2_layout.addWidget(self.download_manager_toggle, Qt.AlignCenter, Qt.AlignCenter)
        self.settings_toggle_3_layout.addWidget(self.a_thing, Qt.AlignCenter, Qt.AlignCenter)

        def install_aria2c():
            toggle_command_1 = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop install aria2']
            process_result = subprocess.run(toggle_command_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

        # checking if toggle has been toggled, looped on thread
        # loop ends if ticked, only runs if never ran before

        # time.sleep is necessary otherwise the 3 checks running concurrently hogs system resources,
        # set to 1 check per sec for each of the 3

        def continuous_checking_downloadmanager_toggle_status():
            while True:
                time.sleep(1)
                if self.download_manager_toggle.isChecked() == True:
                    with open('downloadmanager.txt', 'w') as file:
                        file.truncate(0)
                        file.write(str(1))
                    # checking if has_ran_before_one exists, if not runs and creates
                    check_installed = subprocess.run(['scoop list'], stdout=subprocess.PIPE)
                    # check_manager_command = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop list']
                    # process_result = subprocess.run(check_manager_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    #                                 universal_newlines=True, shell="False")
                    check_installed = check_installed.stdout
                    word = ("aria2")
                    if word not in check_installed:
                        # install aria2c in a seperate thread
                        t = Thread(target=install_aria2c)
                        t.daemon = True
                        t.start()
                if self.download_manager_toggle.isChecked() == False:
                    with open('downloadmanager.txt', 'w') as file:
                        file.truncate(0)
                        file.write(str(0))

        # concurrently run 3 toggle checks when opening settings
        t = Thread(target=continuous_checking_downloadmanager_toggle_status)
        t.daemon = True
        t.start()

        # self.stateTooltip = None
        with open('resource/pushbutton/push_button.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


    # update all apps
    def update_all_apps_function(self):
        update_all_apps_powershell = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop update *']
        update_all_apps_powershell2 = subprocess.run(update_all_apps_powershell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True, shell="False")


        notification.notify(
            title='Finished',
            message='Updated Apps',
            app_icon="fluorite.ico",
            timeout=10,
        )

    def update_all_apps_thread(self):
        t = Thread(target=self.update_all_apps_function)
        t.daemon = True
        t.start()

    # update all apps
    def cleanup_old_app_versions_function(self):
        update_all_apps_powershell = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop cleanup *']
        update_all_apps_powershell2 = subprocess.run(update_all_apps_powershell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True, shell="False")
        notification.notify(
            title='Finished',
            message='Cleaned up old app versions',
            app_icon="fluorite.ico",
            timeout=10,
        )

    def cleanup_old_app_versions_thread(self):
        t = Thread(target=self.cleanup_old_app_versions_function)
        t.daemon = True
        t.start()

    def goSearch(self):
        self.stackedWidget.setCurrentWidget(self.search)

    def goBuckets(self):
        self.stackedWidget.setCurrentWidget(self.buckets)


        def function():
            commandline_options = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop bucket list']
            process_result = subprocess.run(commandline_options, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")
            res = process_result.stdout.split()

            # Manipulate list
            ################################################################################################################

            res = [x for x in res if not (x.isdigit()
                                                     or x[0] == '-' and x[1:].isdigit())]

            for idx, ele in enumerate(res):
               res[idx] = ele.replace('-', '')

            while ("" in res):
                res.remove("")

            res = list(filter(
                lambda ThisWord: not re.match('^(?:(?:[0-9]{2}[:\/,]){2}[0-9]{2,4}|am|pm)$', ThisWord),
                res))

            stopwords = ['Name', 'Source', 'Manifests', 'main', 'Updated']
            for word in list(res):
                if word in stopwords:
                    res.remove(word)

            res = [elements for elements in res if '/Main' not in elements]

            i = int(0)
            while True:
                try:
                    i = i + 1
                    del res[i]
                except:
                    break

            endres = ""
            for ele in res:
                endres += ele + "\n"

            self.cb.addItems(res)

        ################################################################################################################

        def function2():
            commandline_options = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', 'scoop list']
            process_result = subprocess.run(commandline_options, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            universal_newlines=True, shell="False")

            res2 = process_result.stdout
            res2 = str(res2)
            res2 = res2.split("\n")

            # Manipulate list
            ################################################################################################################


            del res2[0]
            del res2[0]
            del res2[0]
            del res2[0]

            simplified = ""

            # converting list to str
            for x in res2:
                simplified += x

            simplified = simplified.split(' ')

            # remove blank spaces
            while ("" in simplified):
                simplified.remove("")

            counter = int(0)
            newlist = []

            # as every app is the 5th item in the list
            for x in simplified:
                try:
                    counter = counter + 5
                    newlist.append(simplified[counter])
                except:
                    pass

            # adding app names to dropdown
            self.apps_list.addItems(newlist)
            ################################################################################################################

            # self.apps_list.addItems(res2)

        # thread fixes hanging, daemon keep alive until finished
        t = Thread(target=function)
        t.daemon = True
        t.start()

        # thread fixes hanging, daemon keep alive until finished
        t = Thread(target=function2)
        t.daemon = True
        t.start()

    def addBucket(self):
        bucketname = self.bucket_input_add.text()
        self.status_indicator_bucket.setText("Adding bucket: " + str(bucketname))
        # self.stackedWidget.setCurrentWidget(self.buckets)
        command = 'scoop bucket add ' + str(bucketname)
        commandline_options = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', command]
        process_result = subprocess.run(commandline_options, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True, shell="False")
        self.status_indicator_bucket.setText("Added: " + str(bucketname))

        notification.notify(
            title='Finished',
            message='Added Bucket',
            app_icon="fluorite.ico",
            timeout=10,
        )

    def thread_add_bucket(self):
        t = Thread(target=self.addBucket)
        t.daemon = True
        t.start()
        # choice = QtWidgets.QMessageBox.question(self, 'Finished',
        #                                         "We're not sure if the process was successful \nReload Buckets?",
        #                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        # if choice == QtWidgets.QMessageBox.Yes:
        #     self.list_buckets_layout.removeWidget(self.list_buckets_label)
        #     self.stackedWidget.setCurrentWidget(self.home)
        #     self.stackedWidget.setCurrentWidget(self.buckets)
        # else:
        #     self.list_buckets_layout.removeWidget(self.list_buckets_label)
        #     self.stackedWidget.setCurrentWidget(self.home)

    def removeBucket(self):
        bucketname = self.cb.currentText()
        command = 'scoop bucket rm ' + str(bucketname)
        commandline_options = [POWERSHELL_PATH, '-ExecutionPolicy', 'Unrestricted', command]
        process_result = subprocess.run(commandline_options, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True, shell="False")
        # choice = QtWidgets.QMessageBox.question(self, 'Finished',
        #                                         "We're not sure if the process was successful \nReload Buckets?",
        #                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        # if choice == QtWidgets.QMessageBox.Yes:
        #     self.list_buckets_layout.removeWidget(self.list_buckets_label)
        #     self.stackedWidget.setCurrentWidget(self.home)
        #     self.stackedWidget.setCurrentWidget(self.buckets)
        # else:
        #     self.list_buckets_layout.removeWidget(self.list_buckets_label)
        #     self.stackedWidget.setCurrentWidget(self.home)

if exists('downloadmanager.txt'):
    pass
else:
    file = open('downloadmanager.txt', 'w+')
    file.write('0')
    file.close()



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle('  ')
my_pixmap = QPixmap("fluorite.ico")
my_icon = QIcon(my_pixmap)
window.setWindowIcon(my_icon)
window.show()
app.exec()
