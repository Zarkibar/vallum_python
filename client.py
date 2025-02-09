import sys
from ciphering import Cipher
import pygame
import socket
import threading


# q1 = str(sys.argv[3])
# q2 = str(sys.argv[4])
# q3 = str(sys.argv[5])
# q4 = str(sys.argv[6])
# q5 = str(sys.argv[7])
# q6 = str(sys.argv[8])
# q7 = str(sys.argv[9])
# q8 = str(sys.argv[10])

# USER_INFO = "#-" + q1+"\n- "+q2+"\n- "+q3+"\n- "+q4+"\n- "+q5+"\n- "+q6+"\n- "+q7+"\n- "+q8+"\n"
USER_INFO = "#-EMPTY INFO"


# SECTION - WINDOW

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Client")

BACKGROUND_COLOR = (2, 2, 10)
INPUT_COLOR = (20, 20, 40)
TEXT_COLOR = (0, 255, 0)

font = pygame.font.Font("fonts/1995.ttf", 17)
chat_history = []
input_text = ">> !start_client_"

# SECTION - NETWORK

SERVER = "localhost" # str(sys.argv[1])
USERNAME = "USER" # str(sys.argv[2])
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = ">> !disconnect_"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SECTION - Cipher

KEY = 1234567890123456789012345678901234567890
cipher = Cipher(key=KEY)


def recv_broadcast():
    try:
        while True:
            msg = client_socket.recv(1024).decode(FORMAT)
            # msg = cipher.decrypt(msg)
            chat_history.append(msg)
    except:
        print("[ERROR] Can't receive messages")


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
                try:
                    client_socket.send(DISCONNECT_MESSAGE.encode(FORMAT))
                    client_socket.close()
                except:
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

                if event.key == pygame.K_RETURN:
                    if input_text == ">> " or input_text == "":
                        break

                    if input_text == ">> !start_client_":
                        chat_history.clear()
                        try:
                            client_socket.connect(ADDR)
                            client_socket.send(USER_INFO.encode(FORMAT))
                            threading.Thread(target=recv_broadcast, daemon=True).start()
                        except ConnectionRefusedError:
                            chat_history.append("[ERROR] Connection refused")
                        except Exception as e:
                            chat_history.append(f"[ERROR] Unexpected error: {e}")
                    else:
                        try:
                            # input_text = cipher.encrypt(input_text)
                            client_socket.send(input_text.encode(FORMAT))
                        except:
                            chat_history.append(f"[NOTE] You can't send messages while disconnected to a server")

                    input_text = ">> "
                elif event.key == pygame.K_BACKSPACE:
                    if input_text == ">> " or input_text == "":
                        break
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    pygame.quit()


if __name__ == "__main__":
    main()

