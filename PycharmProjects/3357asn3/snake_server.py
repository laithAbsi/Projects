import numpy as np
import socket
from _thread import *
import pickle
from snake import SnakeGame
import uuid
import time

# server = "10.11.250.207"
server = "localhost"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

counter = 0
rows = 20

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
# s.settimeout(0.5)
print("Waiting for a connection, Server Started")

game = SnakeGame(rows)
game_state = ""
last_move_timestamp = time.time()
interval = 0.2
moves_queue = set()


def game_thread():
    global game, moves_queue, game_state
    while True:
        last_move_timestamp = time.time()
        game.move(moves_queue)
        moves_queue = set()
        game_state = game.get_state()
        while time.time() - last_move_timestamp < interval:
            time.sleep(0.1)


rgb_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
}
rgb_colors_list = list(rgb_colors.values())


# ... [rest of the imports and initial setup]

def client_thread(conn, addr):
    global game, moves_queue, game_state
    unique_id = str(uuid.uuid4())
    color = rgb_colors_list[np.random.randint(0, len(rgb_colors_list))]
    game.add_player(unique_id, color=color)

    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print(f"Disconnected from {addr}")
                break
            elif data == "quit":
                game.remove_player(unique_id)
                break
            elif data == "reset":
                game.reset_player(unique_id)
            elif data in ["up", "down", "left", "right"]:
                moves_queue.add((unique_id, data))

            conn.sendall(pickle.dumps(game.get_state()))
        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break

    print(f"Connection closed with {addr}")
    conn.close()

def main():
    global counter, game
    start_new_thread(game_thread, ())

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)
        start_new_thread(client_thread, (conn, addr))

if __name__ == "__main__":
    main()