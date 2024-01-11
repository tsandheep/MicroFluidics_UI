from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QMenuBar, QMenu, QAction, QGridLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer
from AStarAlgo  import *
import numpy as np
import time
import pdb

class store(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = 10
        self.cols = 20
        
        self.button_states = np.zeros((self.rows, self.cols), dtype=np.int32)
        self.sensor_cells = np.zeros((self.rows, self.cols), dtype=np.int32)

        #print(self.button_states)
        self.all_buttons = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.cell_states = {
            0 : "Free Cell",
            1 : "Blocked",
            2 : "Blocked",
            3 : "Blocked",
            4 : "Blocked",
            5 : "Dead Cell",
            9 : "Droplet"
        }

        self.cell_colors = {
            "Free-cell" : "#FFFFFF",
            "Dead-cell" : "#BBBBBB",
            "Sensor-cell" : "#FFFF00",
            "Mixed-droplet" : "#964B00"
        }
                        
        self.button_colors = np.array([[self.cell_colors["Free-cell"] for _ in range(self.cols)] for _ in range(self.rows)])
        self.selected_cell = None

        
        self.movement_list = {}
        # the movement_list dictionary: key = from_cell, value = to_cell
        
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.changeState)
        self.timer.start(1000)  # 5000 milliseconds = 5 seconds
        
    def block_kernel(self, t):
        if(t[0] == 0 and t[1] == 0):
            idx = np.where(self.button_states[t[0]:t[0]+2, t[1]: t[1]+2] < 9)
            self.button_states[t[0]:t[0]+2, t[1]: t[1]+2][idx] += 1
        elif(t[0] == 0):
            idx = np.where(self.button_states[t[0]:t[0]+2, t[1]-1: t[1]+2] < 9)
            self.button_states[t[0]:t[0]+2, t[1]-1: t[1]+2][idx] += 1
            
        elif(t[1] == 0):
            print("Cheliya Cheliya", t[0]-1, t[0]+2, t[1],  t[1]+2)
            idx = np.where(self.button_states[t[0]-1:t[0]+2, t[1]: t[1]+2] < 9)
            self.button_states[t[0]-1:t[0]+2, t[1]: t[1]+2][idx] += 1
        else:
            idx = np.where(self.button_states[t[0]-1:t[0]+2, t[1]-1: t[1]+2] < 9)
            self.button_states[t[0]-1:t[0]+2, t[1]-1: t[1]+2][idx] += 1

        print("blocked")



    def un_block_kernel(self, t):
        if(t[0] == 0 and t[1] == 0):
            idx = np.where(self.button_states[t[0]:t[0]+2, t[1]: t[1]+2] < 9)
            self.button_states[t[0]:t[0]+2, t[1]: t[1]+2][idx] -= 1
            
        elif(t[0] == 0):
            idx = np.where(self.button_states[t[0]:t[0]+2, t[1]-1: t[1]+2] < 9)
            self.button_states[t[0]:t[0]+2, t[1]-1: t[1]+2][idx] -= 1
        elif(t[1] == 0):
            idx = np.where(self.button_states[t[0]-1:t[0]+2, t[1]: t[1]+2] < 9)
            self.button_states[t[0]-1:t[0]+2, t[1]: t[1]+2][idx] -= 1
        else:
            idx = np.where(self.button_states[t[0]-1:t[0]+2, t[1]-1: t[1]+2] < 9)
            self.button_states[t[0]-1:t[0]+2, t[1]-1: t[1]+2][idx] -= 1
        print("unblocked")
            
            
    def changeState(self):
        # Change the state of each button randomly
        new_movement_list = {}
        if( len(self.movement_list) ):
            print(self.movement_list)
        for i in self.movement_list:

            from_cell = i
            to_cell = self.movement_list[i]["to"]
            print(from_cell, to_cell)
            print(self.button_states)
            time.sleep(0.1)
                
            if(self.movement_list[i]["movement_type"] == "Move"):
                from_cell = i
                to_cell = self.movement_list[i]["to"]
                clr = self.movement_list[i]["color"]

                self.un_block_kernel(from_cell)
                
                this_path = astar(from_cell, to_cell, self.button_states)
                if this_path:
                    print(self.button_states[this_path[0][0]][this_path[0][1]], self.sensor_cells[this_path[0][0]][this_path[0][1]])
                    if(self.sensor_cells[this_path[0][0]][this_path[0][1]]):
                        print("Source - Sensor Cell")
                        self.all_buttons[this_path[0][0]][this_path[0][1]].setStyleSheet("QPushButton { background-color: %s }"%(self.cell_colors["Sensor-cell"]))
                        
                        pass
                    else:

                        print("Source - Free Cell")
                        
                        self.all_buttons[this_path[0][0]][this_path[0][1]].setStyleSheet("QPushButton { background-color: %s }"%(self.cell_colors["Free-cell"]))


                    self.button_colors[this_path[0][0]][this_path[0][1]] = self.cell_colors["Free-cell"]
                    
                                        
                    self.button_states[this_path[0][0]][this_path[0][1]] = 0
                        
                    
                    self.all_buttons[this_path[0][0]][this_path[0][1]].setChecked(False)
                    self.all_buttons[this_path[0][0]][this_path[0][1]].setCheckable(False)
                    
                    self.all_buttons[this_path[1][0]][this_path[1][1]].setCheckable(True)
                    self.all_buttons[this_path[1][0]][this_path[1][1]].setChecked(True)
                    self.button_states[this_path[1][0]][this_path[1][1]] = 9


                    self.button_colors[this_path[1][0]][this_path[1][1]] = clr
                        
                    self.all_buttons[this_path[1][0]][this_path[1][1]].setStyleSheet("QPushButton { background-color: %s }"%clr)
                    if(this_path[1] != to_cell):
                        new_movement_list[this_path[1]] = {"to": to_cell, "color" : self.movement_list[i]["color"], "movement_type" : self.movement_list[i]["movement_type"]} 
                    self.block_kernel(this_path[1])
                    
                else:
                    new_movement_list[from_cell] = {"to": to_cell, "color" : self.movement_list[i]["color"], "movement_type" : self.movement_list[i]["movement_type"]} 
                    self.block_kernel(from_cell)
                    
            elif(self.movement_list[i]["movement_type"] == "Move_and_Mix"):
                print("Move and Mix", self.movement_list[i]["movement_type"])
                from_cell = i
                to_cell = self.movement_list[i]["to"]
                clr = self.movement_list[i]["color"]

                self.un_block_kernel(to_cell)
                self.un_block_kernel(from_cell)
                
                to_cell_value = self.button_states[to_cell[0]][to_cell[1]]
                self.button_states[to_cell[0]][to_cell[1]] = 0
                
                
                
                this_path = astar(from_cell, to_cell, self.button_states)
                print(this_path)
                if this_path:
                    print(self.button_states[this_path[0][0]][this_path[0][1]], self.sensor_cells[this_path[0][0]][this_path[0][1]])
                    if(self.sensor_cells[this_path[0][0]][this_path[0][1]]):
                        print("Source - Sensor Cell")
                        self.all_buttons[this_path[0][0]][this_path[0][1]].setStyleSheet("QPushButton { background-color: %s }"%(self.cell_colors["Sensor-cell"]))
                        
                        pass
                    else:
                        print("Source - Free Cell")
                        
                        self.all_buttons[this_path[0][0]][this_path[0][1]].setStyleSheet("QPushButton { background-color: %s }"%(self.cell_colors["Free-cell"]))

                    
                    self.button_colors[this_path[0][0]][this_path[0][1]] = self.cell_colors["Free-cell"]
                    
                                        
                    self.button_states[this_path[0][0]][this_path[0][1]] = 0
                        
                    
                    self.all_buttons[this_path[0][0]][this_path[0][1]].setChecked(False)
                    self.all_buttons[this_path[0][0]][this_path[0][1]].setCheckable(False)
                    
                    self.all_buttons[this_path[1][0]][this_path[1][1]].setCheckable(True)
                    self.all_buttons[this_path[1][0]][this_path[1][1]].setChecked(True)
                    self.button_states[this_path[1][0]][this_path[1][1]] = 9


                    self.button_colors[this_path[1][0]][this_path[1][1]] = clr
                        
                    self.all_buttons[this_path[1][0]][this_path[1][1]].setStyleSheet("QPushButton { background-color: %s }"%clr)
                    if(this_path[1] != to_cell):
                        new_movement_list[this_path[1]] = {"to": to_cell, "color" : self.movement_list[i]["color"], "movement_type" : self.movement_list[i]["movement_type"]}
                        self.block_kernel(this_path[1])
                        self.button_states[to_cell[0]][to_cell[1]] = to_cell_value
                        self.block_kernel(to_cell)
                    
                    else:
                        self.all_buttons[to_cell[0]][to_cell[1]].setStyleSheet("QPushButton { background-color: %s }"%(self.cell_colors["Mixed-droplet"]))
                        self.button_colors[to_cell[0]][to_cell[1]] = self.cell_colors["Mixed-droplet"]
                        self.block_kernel(this_path[1])
                        self.button_states[to_cell[0]][to_cell[1]] = to_cell_value
                    
                    
                else:
                    new_movement_list[from_cell] = {"to": to_cell, "color" : self.movement_list[i]["color"], "movement_type" : self.movement_list[i]["movement_type"]} 
                    self.block_kernel(from_cell)
                    self.block_kernel(to_cell)
            

        self.movement_list = {}
        self.movement_list = new_movement_list
        
        """
        temp = np.random.choice([0,1],(self.rows,self.cols),p=[0.5,0.5])
        mask = self.button_states != temp
        ix = np.where(mask)

        for i in zip(*ix):
            st = temp[i[0]][i[1]]
            self.all_buttons[i[0]][i[1]].setChecked(st)
        self.button_states = temp
        """

    def add_movement(self, move_from, move_to, color, movement_type):
        self.movement_list[move_from] = {"to": move_to, "color" : color, "movement_type" : movement_type}
        print("movement list")
        print(self.movement_list)
        pass
