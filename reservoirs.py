from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QMenuBar, QMenu, QAction, QGridLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer
import numpy as np

class Left_Reservoir(QWidget):
    def __init__(self, w, h, row, col, store, color):
        super().__init__()
        
        button_width = w
        button_height = h
        self.row = row
        self.col = col
        self.store = store
        self.color = color
        print(button_width, button_height)

        self.rectangles = np.array([
            {'onclickedcolor': QColor(0, 255, 0),'color': self.color, 'rect': (button_width+int(button_width/2), 0, button_width, button_height)},
            {'onclickedcolor': QColor(255, 0, 0),'color': self.color, 'rect': (2*button_width, button_height, button_width, button_height)},
            {'onclickedcolor': QColor(0, 0, 255),'color': QColor(0, 0, 255), 'rect': (button_width, 0, int(button_width/2), button_height)},
            {'onclickedcolor': QColor(0, 0, 255),'color': QColor(0, 0, 255), 'rect': (button_width, 2*button_height, int(button_width/2), button_height)},
            {'onclickedcolor': QColor(0, 0, 255),'color': QColor(0, 0, 255), 'rect': (0, 0, button_width, 3*button_height)},
            {'onclickedcolor': QColor(0, 255, 0),'color': self.color, 'rect': (button_width+int(button_width/2), 2*button_height, button_width, button_height)},
            {'onclickedcolor': QColor(0, 0, 0),  'color': QColor(0, 0, 0),   'rect': (1*button_width, button_height, button_width, button_height)}
        ])


    def paintEvent(self, event):
        painter = QPainter(self)
        for rectangle in self.rectangles:
            painter.fillRect(*rectangle['rect'], rectangle['color'])

        

    def mousePressEvent(self, event):
        for idx in [4,6]:
            print(idx)
            rect = self.rectangles[idx]['rect']
            print(rect)
            print(rect[0] < event.x() < rect[0] + rect[2] and rect[1] < event.y() < rect[1] + rect[3])

            if rect[0] < event.x() < rect[0] + rect[2] and rect[1] < event.y() < rect[1] + rect[3]:
                # Change the color when clicked
                self.rectangles[idx]['color'] = QColor(0, 255, 255)  # Cyan
                self.update()  # Trigger a repaint

                if(idx == 4):
                    if(not self.store.button_states[self.row][self.col]):
                        self.store.button_states[self.row][self.col] = 9
                        self.store.block_kernel((self.row, self.col))
                        
                        self.store.button_colors[self.row][self.col] = self.color.name()
                        
                        self.store.all_buttons[self.row][self.col].setCheckable(True)
                        self.store.all_buttons[self.row][self.col].setChecked(True)
                        self.store.all_buttons[self.row][self.col].setStyleSheet("""QPushButton { background-color: %s }
                                            QPushButton:checked {background-color: %s}
                                           QPushButton:pressed { background-color: %s }"""%(self.color.name(), self.color.name(), self.color.name()))
                    print(self.store.button_states)
                    
                elif(idx == 6):
                    # unblock_kernel is makint it to -1.
                    # so making this value to 1

                    if(self.store.button_states[self.row][self.col]):
                        self.store.button_states[self.row][self.col] = 1
                        self.store.un_block_kernel((self.row, self.col))
                        self.store.button_colors[self.row][self.col] = '#FFFFFF'
                        
                        #self.store.all_buttons[self.row][self.col].setCheckable(True)
                        self.store.all_buttons[self.row][self.col].setChecked(False)
                        self.store.all_buttons[self.row][self.col].setStyleSheet("""QPushButton { background-color: white }
                                QPushButton:checked {background-color: white}
                               QPushButton:pressed { background-color: white }""")
                        print(self.store.button_states)
                    

    def mouseReleaseEvent(self, event):
        for rectangle in self.rectangles[[4,6]]:
            print("Mouse Release")
            rect = rectangle['rect']
            if rect[0] < event.x() < rect[0] + rect[2] and rect[1] < event.y() < rect[1] + rect[3]:
                # Change the color when the mouse is released
                rectangle['color'] = rectangle['onclickedcolor']
                self.update()  # Trigger a repaint
                
class Right_Reservoir(QWidget):
    def __init__(self,  w, h, row, col, store, color):
        super().__init__()
        

        button_width = w
        button_height = h
        self.row = row
        self.col = col
        self.store = store
        self.color = color
        print(button_width, button_height)
        
        
        self.rectangles = np.array([
            {'onclickedcolor': QColor(0, 255, 0),'color': self.color, 'rect': (int(button_width/2), 0, button_width, button_height)},
            {'onclickedcolor': QColor(255, 0, 0),'color': self.color, 'rect': (0, button_height, button_width, button_height)},
            {'onclickedcolor': QColor(0, 0, 255),'color': QColor(0, 0, 255), 'rect': (button_width+int(button_width/2), 0, button_width, button_height)},
            {'onclickedcolor': QColor(0, 0, 255),'color': QColor(0, 0, 255), 'rect': (button_width+int(button_width/2), 2*button_height, button_width, button_height)},
            {'onclickedcolor': QColor(0, 0, 255),'color': QColor(0, 0, 255), 'rect': (2 * button_width, 0, button_width, 3*button_height)},
            {'onclickedcolor': QColor(0, 255, 0),'color': self.color, 'rect': (int(button_width/2), 2*button_height, button_width, button_height)},
            {'onclickedcolor': QColor(0, 0, 0),  'color': QColor(0, 0, 0),   'rect': (1*button_width, button_height, button_width, button_height)}
        ])

    def paintEvent(self, event):
        painter = QPainter(self)
        for rectangle in self.rectangles:
            painter.fillRect(*rectangle['rect'], rectangle['color'])

        painter.rotate(90)
        

    def mousePressEvent(self, event):
        for idx in [4,6]:
            rect = self.rectangles[idx]['rect']
            if rect[0] < event.x() < rect[0] + rect[2] and rect[1] < event.y() < rect[1] + rect[3]:
                # Change the color when clicked
                self.rectangles[idx]['color'] = QColor(0, 255, 255)  # Cyan
                self.update()  # Trigger a repaint
                if(idx == 4):
                    if(not self.store.button_states[self.row][self.col]):
                        self.store.button_states[self.row][self.col] = 9
                        self.store.block_kernel((self.row, self.col))
                        
                        self.store.button_colors[self.row][self.col] = self.color.name()

                        
                        self.store.all_buttons[self.row][self.col].setCheckable(True)
                        self.store.all_buttons[self.row][self.col].setChecked(True)
                        self.store.all_buttons[self.row][self.col].setStyleSheet("""QPushButton { background-color: %s }
                                            QPushButton:checked {background-color: %s}
                                           QPushButton:pressed { background-color: %s }"""%(self.color.name(), self.color.name(), self.color.name()))

                    print(self.store.button_states)
                    
                elif(idx == 6):
                    # unblock_kernel is makint it to -1.
                    # so making this value to 1

                    if(self.store.button_states[self.row][self.col]):
                        self.store.button_states[self.row][self.col] = 1
                        self.store.un_block_kernel((self.row, self.col))
                        self.store.button_colors[self.row][self.col] = '#FFFFFF'
                        
                        #self.store.all_buttons[self.row][self.col].setCheckable(True)
                        self.store.all_buttons[self.row][self.col].setChecked(False)
                        self.store.all_buttons[self.row][self.col].setStyleSheet("""QPushButton { background-color: white }
                                QPushButton:checked {background-color: white}
                               QPushButton:pressed { background-color: white }""")
                    print(self.store.button_states)
        

    def mouseReleaseEvent(self, event):
        for rectangle in self.rectangles[[4,6]]:
            print("Mouse Release Event")
            rect = rectangle['rect']
            if rect[0] < event.x() < rect[0] + rect[2] and rect[1] < event.y() < rect[1] + rect[3]:
                # Change the color when the mouse is released
                rectangle['color'] = rectangle['onclickedcolor']  # Cyan
                self.update()  # Trigger a repaint
                
