import pygame
import socket
import threading

# SECTION - WINDOW

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Server")

BACKGROUND_COLOR = (2, 2, 10)
INPUT_COLOR = (20, 20, 40)
TEXT_COLOR = (0, 255, 0)

font = pygame.font.Font("fonts/1995.ttf", 17)
chat_history = []
input_text = ">> !start_server_"

# SECTION - NETWORK

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ">> !disconnect_"

clients = []
lock = threading.Lock()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)


def handle_client(conn, addr):
    try:
        update_chat(f"[NEW CONNECTION] {addr} has joined the chat")

        with lock:
            clients.append(conn)

        connected = True
        while connected:
            try:
                msg = conn.recv(1024).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    update_chat(f"[CONNECTION LEFT] {addr} has left the chat")
                    connected = False
                elif "#" in msg:
                    print(msg)
                elif msg:
                    update_chat(msg)
            except ConnectionResetError:
                update_chat(f"[CONNECTION ERROR] {addr} disconnected abruptly")
                break
    except:
        update_chat(f"[ERROR] Connection with {addr} lost")
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()


def start_server():
    try:
        chat_history.append(f"[STARTING] Server is starting...")
        server_socket.listen()
        chat_history.append(f"[LISTENING] Server is listening on {ADDR}")
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, daemon=True, args=(conn, addr))
            thread.start()
            update_chat(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
    except Exception as e:
        update_chat(f"[ERROR] e")
    finally:
        for client in clients:
            client.close()
        server_socket.close()


def update_chat(msg):
    chat_history.append(msg)
    for client in clients:
        try:
            client.send(msg.encode(FORMAT))
        except:
            clients.remove(client)


def draw_chat():
    screen.fill(BACKGROUND_COLOR)

    y_offset = 10
    for chat in chat_history[-15:]:
        chat_surface = font.render(chat, True, TEXT_COLOR)
        screen.blit(chat_surface, (10, y_offset))
        y_offset += 35

    pygame.draw.rect(screen, INPUT_COLOR, (10, HEIGHT - 50, WIDTH - 20, 40), 0)
    input_surface = font.render(input_text, True, TEXT_COLOR)
    screen.blit(input_surface, (15, HEIGHT - 45))

    pygame.display.flip()


def main():
    global screen, input_text

    run = True
    while run:
        draw_chat()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

                if event.key == pygame.K_RETURN:
                    if input_text == ">> " or input_text == "":
                        break

                    if input_text == ">> !start_server_":
                        threading.Thread(target=start_server, daemon=True).start()
                    else:
                        update_chat(input_text)

                    input_text = ">> "
                elif event.key == pygame.K_BACKSPACE:
                    if input_text == ">> " or input_text == "":
                        break
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    server_socket.close()
    pygame.quit()


if __name__ == "__main__":
    main()
