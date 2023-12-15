from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import random
import shutil

FONT_NAME = "Ariel"
BACKGROUND_COLOR = "#B1DDC6"
CARD_FRONT = 'images/card_front.png'
CARD_BACK = 'images/card_back.png'
WRONG_IMAGE = 'images/wrong.png'
RIGHT_IMAGE = 'images/right.png'
FRENCH = 'French'
ENGLISH = 'English'
original = 'data/french_words.csv'
target = 'data/french_words_to_learn.csv'
answer = ''
word = ''
random_numer = 0

# Read source file
data = pd.read_csv(original)
count_row = data.shape[0]

# Duplicate the file, but each new running project adds all words again
shutil.copyfile(original, target)
words_to_learn = pd.read_csv(target)
# print(words_to_learn)

# --------------- Read Data ---------------


def next_card():
    global answer, word, random_numer, flip_timer
    random_number = random.randint(0, count_row+1)
    window.after_cancel(flip_timer)
    word = words_to_learn[FRENCH][random_number]
    answer = words_to_learn[ENGLISH][random_number]
    print(word, answer)
    # card_front_image = PhotoImage(file=CARD_FRONT)
    canvas.itemconfig(card_image, image=card_front_image)
    canvas.itemconfig(language, text=FRENCH, fill='black')
    canvas.itemconfig(card_word, text=word, fill='black')
    flip_timer = window.after(3000, func=flip_card)

# ----------------


def flip_card():

    # card_back_image = PhotoImage(file=CARD_BACK)
    canvas.itemconfig(card_image, image=card_back_image)
    # canvas.imgref = card_back_image
    canvas.itemconfig(language, text=ENGLISH, fill='white')
    canvas.itemconfig(card_word, text=answer, fill='white')




def wrong():

    flip_card()
    window.after(3000, func=next_card)

def right():
    global flip_timer
    window.after_cancel(flip_timer)
    next_card()
    words_to_learn.drop(words_to_learn.index[(words_to_learn[FRENCH] == word)], axis=0, inplace=True)
    words_to_learn.to_csv(target, index=False)



    print('to learn: ', len(words_to_learn))


# #  --------------- Display ----------

window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Image background
canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file=CARD_FRONT)
card_back_image = PhotoImage(file=CARD_BACK)
card_image = canvas.create_image(400, 263, image=card_front_image)
language = canvas.create_text(400, 150, text='Title', font=(FONT_NAME, 40, 'italic'), fill='black')
card_word = canvas.create_text(400, 263, text='Word', font=(FONT_NAME, 60, 'bold'), fill='black')
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


#  Buttons
wrong_png = ImageTk.PhotoImage(Image.open(WRONG_IMAGE))
wrong_button = Button(image=wrong_png, highlightthickness=0, command=wrong)
wrong_button.grid(row=1, column=0)

right_png = ImageTk.PhotoImage(Image.open(RIGHT_IMAGE))
right_button = Button(image=right_png, highlightthickness=0, command=right)
right_button.grid(row=1, column=1)


next_card()

window.mainloop()
