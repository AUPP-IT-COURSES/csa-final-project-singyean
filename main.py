import pygame
import sys
import os
import random
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1400, 800))
pygame.display.set_caption("Beat Buddy")

songs_folder = "songs"
song_files = [file for file in os.listdir(songs_folder) if file.endswith((".mp3", ".wav"))]

BG = pygame.image.load("assets/background.webp")

def get_font(size):
    return pygame.font.Font("assets/MinecraftTen-VGORe.ttf", size)

def show_popup(text, color):
    popup_font = get_font(60)
    popup_text = popup_font.render(text, True, color)
    popup_rect = popup_text.get_rect(center=(1400 // 2, 500 // 2))
    SCREEN.blit(popup_text, popup_rect)
    pygame.display.update()

    pygame.time.wait(1500)  # Display the popup for 1.5 seconds

def play():
    # Initialize game variables
    score = 0
    round_count = 0
    correct_song = None
    buttons = []
    time_limit = 15
    timer = pygame.time.get_ticks() + (time_limit * 1000)
    played_songs = []

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        if correct_song is None:
            # Start a new round
            round_count += 1
            if round_count > 4:
                # Game over, display final score
                end_game(score)
                pygame.mixer.music.stop()  # Stop the song
                return

            # Generate a list of songs that have not been played yet
            available_songs = [song for song in song_files if song[:-4] not in played_songs]

            if len(available_songs) == 0:
                # All songs have been played, end the game
                end_game(score)
                pygame.mixer.music.stop()  # Stop the song
                return

            # Randomly select a song and set it as the correct song
            correct_song = random.choice(available_songs)
            played_songs.append(correct_song[:-4])

            correct_song = random.choice(available_songs)

            available_songs.remove(correct_song)

            random.shuffle(available_songs)

            button_songs = available_songs[:3]

            button_songs.append(correct_song)

            random.shuffle(button_songs)

            buttons = []
            for i, song in enumerate(button_songs):
                x_offset = 300 + (i % 2) * 800
                y_offset = 450 + (i // 2) * 150
                if song == "songs":
                    button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(x_offset, y_offset), text_input=song[:-4], font=get_font(40),
                                    base_color="#dda52c", hovering_color="White", background_color="#000000")
                else:
                    button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(x_offset, y_offset), text_input=song[:-4], font=get_font(40),
                                    base_color="#dda52c", hovering_color="White")
                buttons.append(button)

            start_time = random.randint(0, 55)  # Generate a random start time between 0 and 55 seconds
            pygame.mixer.music.load(os.path.join(songs_folder, correct_song))
            pygame.mixer.music.play(start=start_time)

            timer = pygame.time.get_ticks() + (time_limit * 1000)  # Reset the timer for each round

        # Display round information
        ROUND_TEXT = get_font(75).render(f"Round {round_count}", True, "#dda52c")
        ROUND_RECT = ROUND_TEXT.get_rect(center=(183, 53))
        SCREEN.blit(ROUND_TEXT, ROUND_RECT)

        ROUND_TEXT_S = get_font(75).render(f"Round {round_count}", True, "White")
        ROUND_RECT_S = ROUND_TEXT_S.get_rect(center=(180, 50))
        SCREEN.blit(ROUND_TEXT_S, ROUND_RECT_S)

        SCORE_TEXT = get_font(75).render(f"Score: {score}", True, "#dda52c")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(183, 153))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        SCORE_TEXT_S = get_font(75).render(f"Score: {score}", True, "White")
        SCORE_RECT_S = SCORE_TEXT_S.get_rect(center=(180, 150))
        SCREEN.blit(SCORE_TEXT_S, SCORE_RECT_S)

        # Display remaining time
        time_remaining = max(0, (timer - pygame.time.get_ticks()) // 1000)
        TIME_TEXT = get_font(75).render(f"Time: {time_remaining}", True, "#dda52c")
        TIME_RECT = TIME_TEXT.get_rect(center=(703, 153))
        SCREEN.blit(TIME_TEXT, TIME_RECT)

        TIME_TEXT_S = get_font(75).render(f"Time: {time_remaining}", True, "#ffffff")
        TIME_RECT_S = TIME_TEXT_S.get_rect(center=(703, 150))
        SCREEN.blit(TIME_TEXT_S, TIME_RECT_S)

        # Display buttons
        for button in buttons:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.checkForInput(PLAY_MOUSE_POS):
                        if button.text_input == correct_song[:-4]:
                            score += 1
                            show_popup("Correct!", "green")  # Show correct pop-up
                        else:
                            show_popup("Incorrect!", "red")  # Show incorrect pop-up
                        correct_song = None
                        break

        if pygame.time.get_ticks() >= timer:
            show_popup("Out of time!", "red")  # Show out of time pop-up
            correct_song = None 

        pygame.display.update()

def end_game(score):
    while True:
        SCREEN.blit(BG, (0, 0))

        END_TEXT = get_font(100).render("Game Over", True, "#dda52c")
        END_RECT = END_TEXT.get_rect(center=(703, 103))
        SCREEN.blit(END_TEXT, END_RECT)

        END_TEXT_S = get_font(100).render("Game Over", True, "White")
        END_RECT_S = END_TEXT_S.get_rect(center=(700, 100))
        SCREEN.blit(END_TEXT_S, END_RECT_S)

        SCORE_TEXT = get_font(75).render(f"Score: {score}", True, "Red")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(703, 303))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        SCORE_TEXT_S = get_font(75).render(f"Score: {score}", True, "Green")
        SCORE_RECT_S = SCORE_TEXT.get_rect(center=(700, 300))
        SCREEN.blit(SCORE_TEXT_S, SCORE_RECT_S)

        PLAY_AGAIN = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(700, 550), text_input="Play Again", font=get_font(75),
                            base_color="#dda52c", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(700, 700),
                            text_input="QUIT", font=get_font(75), base_color="#dda52c", hovering_color="White")

        MOUSE_POS = pygame.mouse.get_pos()
        PLAY_AGAIN.changeColor(MOUSE_POS)
        PLAY_AGAIN.update(SCREEN)

        QUIT_BUTTON.changeColor(MOUSE_POS)
        QUIT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_AGAIN.checkForInput(MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Beat Buddy", True, "#dda52c")
        MENU_RECT = MENU_TEXT.get_rect(center=(703, 103))

        MENU_TEXT_SHADOW = get_font(100).render("BeatBuddy", True, "#ffffff")
        MENU_RECT_SHADOW = MENU_TEXT_SHADOW.get_rect(center=(700, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(700, 375),
                            text_input="PLAY", font=get_font(75), base_color="#dda52c", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(700, 550),
                            text_input="QUIT", font=get_font(75), base_color="#dda52c", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT.topleft)
        SCREEN.blit(MENU_TEXT_SHADOW, MENU_RECT_SHADOW.topleft)

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

main_menu()