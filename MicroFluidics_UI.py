import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, \
     QPushButton, QWidget, QTabWidget, QMenuBar, QMenu, QAction, QGridLayout,\
     QSplitter, QSizePolicy, QFileDialog
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import pickle

from electrode import *
from store import *
from cmd_prompt import *
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.store = store()
        self.initUI()

    def initUI(self):
        # Create a central widget
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        self.layout = QGridLayout(central_widget)


        self.elect = Electrode_Widget(self.store)
        self.layout.addWidget(self.elect,0,0,1,1,alignment=Qt.AlignCenter)


        
        #self.elec.setFixedSize(830,320)
        #ELEC_layout.addWidget(self.elec,0,0,1,1,alignment=Qt.AlignTop)
        
        #self.layout.addLayout(ELEC_layout, 0,0,1,1,alignment=Qt.AlignTop)
        #self.layout.addWidget(ELEC_WIDGET)

        self.tab_widget = QTabWidget(self)
        initial_text_edit = QTextEdit(self)
        self.tab_widget.addTab(initial_text_edit, "Untitled")

        self.cmd = CMD()
        self.tab_widget.addTab(self.cmd, "Command")

        
        self.layout.addWidget(self.tab_widget, 1,0)


        self.splitter = QSplitter(self)
        self.splitter.setOrientation(Qt.Vertical)
        
        self.splitter.addWidget(self.elect)
        self.splitter.addWidget(self.tab_widget)
        #splitter.setSizes([100, 200])  # Set initial sizes for the widgets

        self.layout.addWidget(self.splitter)
        

        #collapsible_layout.addWidget(self.layout)
        
        # Create a menu bar
        menubar = self.menuBar()

        # Create a File menu
        file_menu = menubar.addMenu('File')

        # Create a New action
        new_action = QAction('New', self)
        new_action.triggered.connect(self.onNew)
        file_menu.addAction(new_action)

        # Load template file
        template_file_load = QAction('Open', self)
        template_file_load.triggered.connect(self.showFileDialog)
        file_menu.addAction(template_file_load)

        # Load template file
        template_file_save = QAction('Save', self)
        template_file_save.triggered.connect(self.showSaveFileDialog)
        file_menu.addAction(template_file_save)
        

        # Create an Exit action
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.onExit)
        file_menu.addAction(exit_action)

        self.setWindowTitle('PyQt Window with Menu and Button')
        self.setGeometry(100, 100, 400, 300)

    def showSaveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "SDU Files (*.sdu)", options=options)

        if file_name:
            print("Saving the file as", file_name)
            print(self.store.button_states)
            try:
                with open(file_name+".sdu", "wb") as F:
                    pickle.dump(self.store.button_states, F)
            except Exception as e:
                # everything else, possibly fatal
                print(e)
                return
            

    def showFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Use the built-in file dialog

        # Get selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'SDU Files (*.sdu)', options=options)

        print('Selected file:', file_path)
        
        if file_path:
            with open(file_path, "rb") as F:
                button_states = pickle.load(F)
            self.store.button_states = button_states

            self.layout.removeWidget(self.elect)
            self.layout.removeItem(self.layout.itemAt(0))


            self.elect = Electrode_Widget(self.store)
            
            self.layout.addWidget(self.elect, 0, 0, 1, 1, alignment=Qt.AlignCenter)

            
            self.splitter = QSplitter(self)
            self.splitter.setOrientation(Qt.Vertical)
            
            self.splitter.addWidget(self.elect)
            self.splitter.addWidget(self.tab_widget)
            

            self.layout.addWidget(self.splitter)

            
            print(button_states)
            

    def onButtonClick(self):
        print('Button clicked!')

    def onNew(self):
        print('New action triggered!')

    def onExit(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
