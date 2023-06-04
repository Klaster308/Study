import socket

from threading import Thread
from pygame import mouse, draw
from tkinter import messagebox


class VisualField:
    def __init__(self, screen, client: socket.socket, n, player_number):
        self.n = n
        self.field = [[0 for _ in range(n)] for __ in range(n)]
        self.move_of_player = 1
        self.player_number = player_number

        self.screen = screen
        self.client = client
        self.buttons = []

        self.mouse_is_pressed = False
        self.mouse_cords = (0, 0)
        self.screen_w, self.screen_h = screen.get_width(), screen.get_height()
        self.ratio_w, self.ratio_h = self.screen_w // self.n, self.screen_h // self.n

        for i in range(1, n):
            draw.line(screen, (0, 0, 0), (i * self.ratio_w, 0), (i * self.ratio_w, self.screen_w), 3)
            draw.line(screen, (0, 0, 0), (0, i * self.ratio_h), (self.screen_h, i * self.ratio_w), 3)

        self.controlling = Thread(target=self.control)
        self.controlling.start()

    def __del__(self):
        self.controlling.join()
        del self.field

    def control(self):
        while True:
            if self.move_of_player == self.player_number:
                if mouse.get_pressed()[0]:
                    mouse_x, mouse_y = mouse.get_pos()
                    x, y = mouse_x // self.ratio_w, mouse_y // self.ratio_h
                    if not self.field[x][y]:
                        self.add_my_chip(x, y)
                        self.client.send(f"{x} {y}".encode())
                        print("send", f"{x} {y}")
            else:
                move = self.client.recv(128).decode()
                print("get move", move)
                try:
                    x, y = map(int, move.split())
                except ValueError:
                    print(move)
                    if move == "!draw":
                        messagebox.showinfo("", "Ничья!")
                        return
                    winner = int(move[5])
                    if winner == self.player_number:
                        messagebox.showinfo("", "Вы победили!")
                    else:
                        messagebox.showinfo("", "Вы проиграли!")
                    return
                else:
                    self.add_another_chip(x, y)

    def add_my_chip(self, x, y):
        self.field[x][y] = self.move_of_player

        print("draw_blue_circle")
        draw.circle(
            self.screen,
            "blue" if self.move_of_player == self.player_number else "red",
            ((x + 0.5) * self.ratio_w, (y + 0.5) * self.ratio_h),
            20
        )
        self.move_of_player *= -1

    def add_another_chip(self, x, y):
        self.field[x][y] = self.move_of_player
        self.move_of_player *= -1

        print("draw_red_circle")
        draw.circle(
            self.screen,
            "red",
            ((x + 0.5) * self.ratio_w, (y + 0.5) * self.ratio_h),
            20
        )
