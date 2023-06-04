import socket

from threading import Thread
from time import sleep

from server_components import Game


ready_for_game = []
games = []


def try_to_start_game():
    while True:
        sleep(1)
        if len(ready_for_game) >= 2:
            print("start game")
            user1 = ready_for_game.pop()
            user2 = ready_for_game.pop()

            games.append(Game(15, user1, user2))


def wait_for_game(user):
    message = user.recv(128)
    if message.decode() == "!ready":
        ready_for_game.append(user)
        print("new user")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 1063))
    server.listen()
    users = []
    print("server is listening")

    Thread(target=try_to_start_game).start()

    while True:
        user_socket, address = server.accept()
        users.append(user_socket)
        Thread(target=wait_for_game, args=(user_socket,)).start()


if __name__ == '__main__':
    main()
