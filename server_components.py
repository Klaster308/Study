import socket

from threading import Thread
from time import sleep


class Game:
    def control(self):
        # self.users[0].send("!wait_for_move".encode())
        while True:
            move = self.users[0].recv(128)
            print(f"user1: {move.decode()}")
            self.users[1].send(move)
            x, y = map(int, move.decode().split())
            self.add_chip(x, y)

            if self.check_win():
                print("user1 win")
                self.users[0].send("!user1_win".encode())
                self.users[1].send("!user1_win".encode())
                return

            move = self.users[1].recv(128)
            print(f"user2:{move.decode()}")
            self.users[0].send(move)
            x, y = map(int, move.decode().split())
            self.add_chip(x, y)

            print(self.chips_count)
            if self.check_win():
                print("user2 win")
                self.users[0].send("!user2_win".encode())
                self.users[1].send("!user2_win".encode())
                return
            elif self.chips_count == self.n ** 2:
                print("It\'s draw")
                self.users[0].send("!draw".encode())
                self.users[1].send("!draw".encode())
                return

    # 0 - пустая клетка, 1 и -1 - игроки
    def __init__(self, n, user1: socket.socket, user2: socket.socket):
        self.n = n
        self.field = [[0 for _ in range(n)] for __ in range(n)]
        self.chips_count = 0
        self.player_number = 1
        self.users = (user1, user2)
        self.users[0].send("!start1".encode())  # start1 значит, что юзер 1 ходдит первым
        sleep(0.1)
        self.users[1].send("!start2".encode())
        Thread(target=self.control).start()

    def add_chip(self, x, y):
        if not self.field[x][y]:
            self.field[x][y] = self.player_number
            self.player_number *= -1
            self.chips_count += 1
            return True
        return False

    def check_win(self):
        n = self.n
        # Проверка горизонтальных комбинаций
        for i in range(n):
            for j in range(n - 4):
                if self.field[i][j] != 0 and self.field[i][j] == self.field[i][j + 1] == self.field[i][j + 2] == \
                        self.field[i][j + 3] == self.field[i][j + 4]:
                    return self.field[i][j]  # Возвращаем номер выигравшего игрока

        # Проверка вертикальных комбинаций
        for i in range(n - 4):
            for j in range(n):
                if self.field[i][j] != 0 and self.field[i][j] == self.field[i + 1][j] == self.field[i + 2][j] == \
                        self.field[i + 3][j] == self.field[i + 4][j]:
                    return self.field[i][j]  # Возвращаем номер выигравшего игрока

        # Проверка диагоналей, идущих слева направо (\)
        for i in range(n - 4):
            for j in range(n - 4):
                if self.field[i][j] != 0 and self.field[i][j] == self.field[i + 1][j + 1] == self.field[i + 2][j + 2] \
                        == self.field[i + 3][j + 3] == self.field[i + 4][j + 4]:
                    return self.field[i][j]  # Возвращаем номер выигравшего игрока

        # Проверка диагоналей, идущих справа налево (/)
        for i in range(n - 4):
            for j in range(4, n):
                if self.field[i][j] != 0 and self.field[i][j] == self.field[i + 1][j - 1] == self.field[i + 2][j - 2] \
                        == self.field[i + 3][j - 3] == self.field[i + 4][j - 4]:
                    return self.field[i][j]  # Возвращаем номер выигравшего игрока

        return False  # Никто не выиграл
