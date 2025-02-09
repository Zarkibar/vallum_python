import threading
import pygame
from ollama import chat
from ollama import create


create(
    model='mark',
    from_='deepseek-r1:1.5b',
    system=""""""
)


# SECTION - WINDOW

pygame.init()

WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Val")

BACKGROUND_COLOR = (2, 2, 10)
INPUT_COLOR = (20, 20, 40)
TEXT_COLOR = (0, 255, 0)

font = pygame.font.Font("fonts/1995.ttf", 18)
chat_history = []
input_text = ">> "


def recv_msg(text):
    stream = chat(
        model='mark',
        messages=[{'role': 'user', 'content': text}],
        stream=True,
    )
    chat_history.append("-->> ")
    for chunk in stream:
        chat_history[-1] += chunk['message']['content']


def update_chat(msg):
    chat_history.append(msg)


def wrap_text(text, font, max_width):
    """Splits text into multiple lines so it fits inside max_width."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_chat():
    screen.fill(BACKGROUND_COLOR)

    y_offset = 10
    max_width = WIDTH - 20  # Space padding
    for chat in chat_history[-15:]:  # Show only last 15 messages
        wrapped_lines = wrap_text(chat, font, max_width)
        for line in wrapped_lines:
            chat_surface = font.render(line, True, TEXT_COLOR)
            screen.blit(chat_surface, (10, y_offset))
            y_offset += 35  # Move down for the next line

    # Draw input box
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

                    if input_text == ">> !quit_":
                        run = False
                    else:
                        update_chat(input_text)
                        threading.Thread(target=recv_msg, daemon=True, args=(input_text,)).start()

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
