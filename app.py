import pygame as pg
import sys
import socket

from app_components import VisualField


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 1063))
    client.send("!ready".encode())
    role = client.recv(128).decode()
    print(f"{role=}")

    pg.init()
    screen = pg.display.set_mode((900, 900))
    pg.display.set_caption(role)
    screen.fill((255, 255, 255))

    if role == "!start1":
        field = VisualField(screen, client, 15, 1)
        print("start1")
    else:
        field = VisualField(screen, client, 15, -1)
        print("start2")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if pg.key.get_pressed()[pg.K_SPACE]:
            pg.display.quit()
            return
        pg.display.flip()


if __name__ == '__main__':
    while True:
        main()
