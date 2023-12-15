from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import random

FONT_NAME = "Ariel"
BACKGROUND_COLOR = "#B1DDC6"
CARD_FRONT = 'images/card_front.png'
CARD_BACK = 'images/card_back.png'
WRONG_IMAGE = 'images/wrong.png'
RIGHT_IMAGE = 'images/right.png'
FRENCH = 'French'
ENGLISH = 'English'
current_card = {}
to_learn = {}

# --------------- Read Data ---------------

try:
    data = pd.read_csv('data/french_words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    print(current_card)
    canvas.itemconfig(card_title, text=FRENCH, fill='black')
    canvas.itemconfig(card_word, text=current_card[FRENCH], fill='black')
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text=ENGLISH)
    canvas.itemconfig(card_word, text=current_card[ENGLISH])

#
#
def wrong():
    next_card()

def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)
    next_card()


# #  --------------- Display ----------
window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Image background
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file=CARD_FRONT)
card_back_img = PhotoImage(file=CARD_BACK)
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text=FRENCH, font=(FONT_NAME, 40, 'italic'), fill='black')
card_word = canvas.create_text(400, 263, text='word', font=(FONT_NAME, 60, 'bold'), fill='black')
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


#  Buttons
wrong_png = ImageTk.PhotoImage(Image.open(WRONG_IMAGE))
wrong_button = Button(image=wrong_png, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

right_png = ImageTk.PhotoImage(Image.open(RIGHT_IMAGE))
right_button = Button(image=right_png, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
