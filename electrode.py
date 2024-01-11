from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QVBoxLayout, QPushButton, QWidget, QMenuBar, QMenu, QAction, QGridLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import pdb
from reservoirs import *

class Cell(QPushButton):
    def __init__(self, row, col, store):
        super().__init__()
        self.row = row
        self.col = col
        self.store = store
        self.setCheckable(True)  # Make the button checkable

        #  I need to add logic to color the cell based on its value
        # cells with sensors, defective cells, 
        #if(self.store.button_states[row][col] )

        self.setStyleSheet("QPushButton { background-color: %s }"%(self.store.cell_colors["Free-cell"]))
        self.disable_context_menu = False
        
    def contextMenuEvent(self, event):
        print(self.row, self.col)
        menu = QMenu(self)
        
        action1 = menu.addAction("Move Here")
        action_mix = menu.addAction("Move Here + Mix")
        action2 = menu.addAction("Sensor-cell")
        action3 = menu.addAction("Dead-cell")
        action4 = menu.addAction("Free-cell")

        selected_action = menu.exec_(self.mapToGlobal(event.pos()))

        if selected_action == action1:
            if(self.store.selected_cell):
                if(self.store.button_states[self.row][self.col] != 9):
                    from_row = self.store.selected_cell[0]
                    from_col = self.store.selected_cell[1]

     
                    clr = self.store.button_colors[from_row][from_col]
                    self.store.add_movement(self.store.selected_cell, (self.row, self.col), clr, "Move")
                    self.store.selected_cell = None
                    print("Move Here")
            
        elif selected_action == action_mix:
            if(self.store.selected_cell):
                if(self.store.button_states[self.row][self.col] == 9):
                    print(" Move and Mix ")
                    from_row = self.store.selected_cell[0]
                    from_col = self.store.selected_cell[1]


                    clr = self.store.button_colors[from_row][from_col]
                    self.store.add_movement(self.store.selected_cell, (self.row, self.col), clr, "Move_and_Mix")
                    self.store.selected_cell = None

                
            
        elif selected_action == action2:
            print("Sensor-cell")
            self.setCheckable(False)
            self.setChecked(False)
            self.setStyleSheet("QPushButton { background-color: %s }"%(self.store.cell_colors["Sensor-cell"]))
            self.store.button_colors[self.row][self.col] = self.store.cell_colors["Sensor-cell"]
            self.store.sensor_cells[self.row][self.col] = 1

            print(self.store.sensor_cells[0:5, 0:5])



                
        elif selected_action == action3:
            print("Dead-cell")
            self.setCheckable(False)
            self.setChecked(False)
            self.setStyleSheet("QPushButton { background-color: %s }"%(self.store.cell_colors["Dead-cell"]))

            self.store.button_states[self.row][self.col] = 5
            
        elif selected_action == action4:
            print("Free-cell")
            self.setStyleSheet("QPushButton { background-color: %s }"%(self.store.cell_colors["Free-cell"]))
            self.store.button_states[self.row][self.col] = 0
            self.store.sensor_cells[self.row][self.col] = 0
            print(self.store.button_states)

    def mousePressEvent(self, event):
        if(event.button() == Qt.LeftButton):
            if(self.store.button_states[self.row][self.col] == 9):
                print("Droplet Selected", self.row, self.col)
                self.store.selected_cell = (self.row, self.col)
        # Override mouse press event to prevent state change
        pass

    def mouseReleaseEvent(self, event):
        
        # Override mouse release event to prevent state change
        pass
        
            
class ButtonGrid(QWidget):
    def __init__(self, store):
        super().__init__()
        self.store = store
        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        #self.setFixedSize(300, 500)
        
        # Create a 2D list to store button states
        #self.button_states = np.zeros((self.rows, self.columns))
        
        print(self.store.all_buttons)
        # Create a grid of buttons
        for row in range(self.store.rows):
            for col in range(self.store.cols):
                button = Cell(row,col, self.store)
                button.setCheckable(True)
                button.setChecked(self.store.button_states[row][col])
                button.clicked.connect(lambda state, r=row, c=col: self.buttonClicked(r, c))
                self.store.all_buttons[row][col] = button
                self.grid_layout.addWidget(button, row, col)

        self.setWindowTitle('Button Grid')
        #self.setGeometry(300, 300, 300, 200)

        """
        # Create a QTimer to trigger the changeState function every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.store.changeState)
        self.timer.start(50)  # 5000 milliseconds = 5 seconds
        """


    def buttonClicked(self, row, col):
        # Update the corresponding element in the array based on the button's state
        #self.store.button_states[row][col] = not self.store.button_states[row][col]
        print(self.store.button_states)
        print("Button clicked", row, col)

    def resizeEvent(self, event):
        # Override resizeEvent to enforce fixed size
        print("Resizing ButtonGrid")
        
    

class Electrode(QWidget):
    def __init__(self, store):
        super().__init__()
        self.store = store
        self.initUI()

    def initUI(self):
        # Create a grid layout
        grid_layout = QGridLayout(self)
        #self.setFixedSize(830,320)

        rsr1 = Left_Reservoir(w = 30, h = 30, row = 1, col = 0, store=self.store, color = QColor(0,255,0))
        rsr1.setFixedSize(90, 90)
        grid_layout.addWidget(rsr1,0,0,1,1, alignment=Qt.AlignTop)

        rsr2 = Left_Reservoir(w = 30, h = 30, row = 8, col = 0, store=self.store, color = QColor(255,0,0) )
        rsr2.setFixedSize(90, 90)
        grid_layout.addWidget(rsr2,2,0,1,1, alignment=Qt.AlignTop)
        

        btgrid = ButtonGrid(self.store)
        btgrid.setFixedSize(600, 300)
        #btgrid.setGeometry(200, 100, 100, 300)
        grid_layout.addWidget(btgrid,0,1,0,1,alignment=Qt.AlignTop)


        rsr3 = Right_Reservoir(w = 30, h = 30, row = 1, col = 19, store=self.store, color = QColor(255,180,0))
        rsr3.setFixedSize(90, 90)
        grid_layout.addWidget(rsr3,0,3,1,1, alignment=Qt.AlignTop)

        rsr4 = Right_Reservoir(w = 30, h = 30, row = 8, col = 19, store=self.store, color = QColor(150, 150, 150))
        rsr4.setFixedSize(90, 90)
        grid_layout.addWidget(rsr4,2,3,1,1, alignment=Qt.AlignTop)

        
        # Set size policy to prevent the layout from resizing
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        self.setWindowTitle('Fixed Size QGridLayout')
        self.setGeometry(100, 100, 300, 300)
    def resizeEvent(self, event):
        # Override resizeEvent to enforce fixed size
        print("Resizing it")

        """
        screen_geometry = QDesktopWidget().screenGeometry()
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2

        # Move the widget to the calculated center position
        self.move(center_x, center_y)
        """
        
        #self.resize(830, 320)

class Electrode_Widget(QWidget):
    def __init__(self, store):
        super().__init__()
        self.store = store
        self.initUI()
        
    def initUI(self):
        self.elec = Electrode(self.store)
        layout = QGridLayout(self)
        layout.addWidget(self.elec, 0, 0, 1, 1, alignment=Qt.AlignCenter)
