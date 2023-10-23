# JM 1/10/23
import pygame
import requests
import random
from collections import Counter

# Get the word list from the internet -----
r = requests.Session()

try:  # Try to go on the interent and get the word list
    resp = r.get('https://raw.githubusercontent.com/tabatkins/wordle-list/main/words').text
    wordList = resp.split('\n')
    answer = random.choice(wordList)

except requests.exceptions.ConnectionError:  # If no internet exit the program
    print('You need internet')
    exit()

# Pygame Setup
pygame.init()

black = (0, 0, 0)  # Colors
white = (255, 255, 255)
green = (0, 255, 0)
yellow = (255, 200, 0)
gray = (220, 220, 220)

display_surface = pygame.display.set_mode((400, 600))  # screen size
pygame.display.set_caption('Wordle')  # Title

font = pygame.font.Font('freesansbold.ttf', 40)  # Normal Font
small_font = pygame.font.Font('freesansbold.ttf', 20)  # Smaller Font

display_surface.fill(white)  # White Background

# Create the Wordle Boxes
for y in range(0, 6):
    for x in range(0, 5):
        pygame.draw.rect(display_surface, gray, pygame.Rect(30 + (x * 70), 30 + (y * 70), 60, 60))

# Starting variables
word = []
attempts = 0
remaining_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# ----- Functions -------
def wordle_checker(word):  # Does the heavy lifting
    answer_split = [x for x in answer]
    response = [None, None, None, None, None]  # Color order

    res = dict(Counter(answer_split))  # Make a dictionary with all word frequency

    # Make a list of all the colors in the proper order
    for x in range(0,5):
        if word[x] == answer_split[x]:
            response[x] = '🟩'
            res[word[x]] -= 1

    for x in range(0,5):
        if word[x] in answer_split and res[word[x]] > 0 and response[x] != '🟩':
            response[x] = '🟨'
            res[word[x]] -= 1
    for x in range(0, 5):
        if word[x] not in answer_split:
            if word[x] in remaining_letters:
                remaining_letters.remove(word[x])

    x = 0
    for item in response:  # Put everything on the screen (in order)
        if item == '🟩':
            pygame.draw.rect(display_surface, green, pygame.Rect((x * 70) + 30, 30 + (attempts * 70), 60, 60))
            # Put the letter back in
            display_surface.blit(font.render(word[x].upper(), True, white), ((45 + (70 * x)), 40 + (attempts * 70)))
        elif item == '🟨':
            pygame.draw.rect(display_surface, yellow, pygame.Rect((x * 70) + 30, 30 + (attempts * 70), 60, 60))
            display_surface.blit(font.render(word[x].upper(), True, white), ((45 + (70 * x)), 40 + (attempts * 70)))
        x += 1

    draw_remaining_letters(remaining_letters)

    if response == ['🟩', '🟩', '🟩', '🟩', '🟩']:
        return True


def draw_remaining_letters(remaining_letters):  # Draw the remaining letters below
    i = 0
    pygame.draw.rect(display_surface, white, pygame.Rect(0, 500, 600, 30))
    for letter in remaining_letters:
        display_surface.blit(small_font.render(letter, True, black), (30 + (15 * i), 500))
        i += 1


def restart_game():  # Reset all the variables when you want to play again
    global answer, word, attempts, remaining_letters  # get in the global scope
    pygame.draw.rect(display_surface, white, pygame.Rect(0, 450, 600, 600))
    answer = random.choice(wordList)  # Generate a new word
    for y in range(0, 6):  # Draw new grey boxes
        for x in range(0, 5):
            pygame.draw.rect(display_surface, gray, pygame.Rect(30 + (x * 70), 30 + (y * 70), 60, 60))
    word = []
    attempts = 0
    remaining_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                         'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


while True:
    for event in pygame.event.get():  # main loop
        if attempts == 6: # If you have reached max tries, show the word and end the game
            display_surface.blit(font.render(answer, True, black), (30, 540)) # Draw the word
            pygame.display.update()  # Put it on the screen
            pygame.time.wait(5000)  # Let player take it in
            restart_game()  # Restart

        if event.type == pygame.KEYDOWN: # If any key is pressed
            if pygame.key.name(event.key) == 'return' and len(word) == 5:  # If you press enter (submit a word)
                if "".join(word) in wordList:
                    if wordle_checker(word):  # If the wordle checker shows 5 green, you win!
                        display_surface.blit(font.render('WIN!', True, black), (30, 540))
                        pygame.display.update()
                        pygame.time.wait(5000)
                        restart_game()
                    else:  # Else, keep playing
                        attempts += 1
                        word = []
                else:  # That's not a real word
                    pass # Useless maybe add something here

            elif pygame.key.name(event.key) == 'backspace' and len(word) != 0:  # Deleting letters
                word.pop()
                pygame.draw.rect(display_surface, gray, pygame.Rect((len(word) * 70) + 30, 30 + (attempts * 70), 60, 60))

            if len(pygame.key.name(event.key)) == 1 and attempts < 6:  # If you type a letter
                if len(word) < 5: # If there is room
                    word.append(pygame.key.name(event.key))
                    display_surface.blit(font.render(pygame.key.name(event.key).upper(), True, white), ((45 + (70 * (len(word) - 1))), 40 + (attempts * 70)))

        if event.type == pygame.QUIT:  # if you press the exit button
             pygame.quit()
             quit()

        pygame.display.update()  # Update the screen
