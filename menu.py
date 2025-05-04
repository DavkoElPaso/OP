import pygame
import sys
from button import Button


def get_font(size):
    return pygame.font.Font("imgs/ahmed/font.ttf", size)


def play():
    from game import main
    main()


def main_menu():
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 600))
    pygame.display.set_caption("Pivko SKS Main Menu")

    BG = pygame.image.load("imgs/ahmed/menubg.jpg")

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("Pivko SKS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # skore
        try:
            with open('highscores.txt', 'r') as f:
                high_scores = eval(f.read())
            with open('currentscores.txt', 'r') as f:
                current_scores = eval(f.read())

            y_pos = 180
            for level in range(1, 4):
                score_text = f"Level {level} - Last game: {current_scores[level]} | High Score: {high_scores[level]}"
                SCORE_TEXT = get_font(25).render(score_text, True, "#b68f40")
                SCORE_RECT = SCORE_TEXT.get_rect(center=(640, y_pos))
                SCREEN.blit(SCORE_TEXT, SCORE_RECT)
                y_pos += 40
        except:
            pass

        PLAY_BUTTON = Button(image=pygame.image.load("imgs/ahmed/play.png"), pos=(640, 350),
                             text_input="PLAY", font=get_font(55), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("imgs/ahmed/quit.png"), pos=(640, 460),
                             text_input="QUIT", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()