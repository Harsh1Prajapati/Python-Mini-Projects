from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt
import sys
import random

class TicTacToe(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(300, 300))    
        self.setWindowTitle("Tic Tac Toe") 
        self.setWindowIcon(QIcon('icon.png'))  # Set the path to your icon file
        self.current_player = 'X'
        self.board = [' ']*9
        self.buttons = []
        self.ai = False
        self.difficulty = 'easy'
        self.theme = 'light'

        central_widget = QWidget(self)          
        self.setCentralWidget(central_widget)   

        layout = QGridLayout(central_widget)    

        for i in range(9):
            button = QPushButton(' ', self)
            button.setFont(QFont('Arial', 24))
            button.setStyleSheet("background-color: lightblue")
            button.clicked.connect(lambda _, i=i: self.click(i))
            layout.addWidget(button, i//3, i%3)
            self.buttons.append(button)

        self.label = QLabel("Player X's turn", self)
        self.label.setFont(QFont('Arial', 24))
        layout.addWidget(self.label, 3, 0, 1, 3)

        self.player_selection()
        self.theme_selection()

    def player_selection(self):
        items = ("Player vs Player", "Player vs Computer")
        item, ok = QInputDialog.getItem(self, "Select game mode", "Choose a game mode:", items, 0, False)
        if ok and item:
            self.ai = (item == "Player vs Computer")
            if self.ai:
                self.difficulty_selection()

    def difficulty_selection(self):
        items = ("Easy", "Hard")
        item, ok = QInputDialog.getItem(self, "Select difficulty", "Choose a difficulty level:", items, 0, False)
        if ok and item:
            self.difficulty = item.lower()

    def theme_selection(self):
        items = ("Light", "Dark")
        item, ok = QInputDialog.getItem(self, "Select theme", "Choose a theme:", items, 0, False)
        if ok and item:
            self.theme = item.lower()
            self.update_theme()

    def update_theme(self):
        if self.theme == 'dark':
            self.setStyleSheet("background-color: black; color: white;")
            for button in self.buttons:
                button.setStyleSheet("background-color: grey; color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")
            for button in self.buttons:
                button.setStyleSheet("background-color: lightblue; color: black;")

    def click(self, i):
        if self.board[i] == ' ':
            self.board[i] = self.current_player
            self.buttons[i].setText(self.current_player)
            self.buttons[i].setStyleSheet("background-color: lightgreen" if self.current_player == 'X' else "background-color: lightyellow")
            if self.check_win():
                QMessageBox.information(self, "Game Over", f"Player {self.current_player} wins!")
                self.reset()
            elif ' ' not in self.board:
                QMessageBox.information(self, "Game Over", "It's a draw!")
                self.reset()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.label.setText(f"Player {self.current_player}'s turn")
                if self.ai and self.current_player == 'O':
                    self.ai_move()

    def ai_move(self):
        possible_moves = [i for i, x in enumerate(self.board) if x == ' ']
        if self.difficulty == 'hard':
            # AI strategy: win > block > random
            for move in possible_moves:
                self.board[move] = 'O'
                if self.check_win():
                    self.board[move] = ' '
                    break
                self.board[move] = 'X'
                if self.check_win():
                    self.board[move] = ' '
                    break
                self.board[move] = ' '
            else:
                move = random.choice(possible_moves)
        else:
            move = random.choice(possible_moves)
        self.click(move)

    def check_win(self):
        win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        return any(self.board[i]==self.board[j]==self.board[k]==self.current_player for i,j,k in win_conditions)

    def reset(self):
        self.board = [' ']*9
        for button in self.buttons:
            button.setText(' ')
            button.setStyleSheet("background-color: lightblue")
        self.current_player = 'X'
        self.label.setText("Player X's turn")
        self.player_selection()
        self.theme_selection()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = TicTacToe()
    mainWin.show()
    sys.exit(app.exec_())
