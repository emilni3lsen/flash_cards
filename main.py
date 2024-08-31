from tkinter import *
import random
import pandas
import os.path


FLIP_TIME = 3   # How long it waits before card flips (in seconds)
LANGUAGE1 = "French"
LANGUAGE2 = "English"
FILE_NAME = "french_words.csv" 
FLIP_FONT = ("Arial", 10, "bold")

BACKGROUND_COLOR = "#B1DDC6"
ENCODING = "utf-8"

if os.path.exists("data/words_to_learn.csv"):
    data_file = "data/words_to_learn.csv"
else:
    data_file = fr"data\{FILE_NAME}"
data = pandas.read_csv(data_file, encoding=ENCODING)
words_to_learn = data.to_dict(orient="records")


card_flip = None
current_word = None


### FUNCTIONS ###

def next_card():
    global card_flip, current_word
    canvas.itemconfig(card_image, image=front_image)
    
    if card_flip:
        window.after_cancel(card_flip)
    
    if not words_to_learn:
        canvas.itemconfig(word_text, text="NO MORE WORDS", fill="black", font=("Arial", 60, "bold"))
        canvas.itemconfig(language_text, text="")
        return
        
    current_word = random.choice(words_to_learn)
    canvas.itemconfig(language_text, text=LANGUAGE1, fill="black")
    canvas.itemconfig(word_text, text=current_word[LANGUAGE1], fill="black", font=font_size(current_word[LANGUAGE1]))
    card_flip = window.after(FLIP_TIME*1000, flip_card)
    

def flip_card():
    definition = current_word[LANGUAGE2]
    canvas.itemconfig(word_text, font=font_size(definition))
    definition = split_lines(definition)
    
    canvas.itemconfig(card_image, image=back_image)
    canvas.itemconfig(language_text, text=LANGUAGE2, fill="white")
    canvas.itemconfig(word_text, text=definition, fill="white")
    

def word_is_known():
    if current_word and not len(words_to_learn) == 0:
        words_to_learn.remove(current_word)
        data = pandas.DataFrame(words_to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
    

def font_size(line):
    if len(line) > 60:
        return ("Arial", 11, "bold")
    if len(line) > 30:
        return ("Arial", 18, "bold")
    if len(line) > 15:
        return ("Arial", 30, "bold")
    else:
        return ("Arial", 60, "bold")
    

def split_lines(text):
    lines = []
    current_line = ""
    for word in text.split():
        if len(current_line + word) <= 100:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    return "\n".join(lines)
    
    

### UI SETUP ###

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=front_image)
language_text = canvas.create_text(400, 130, text="Click a button to", font=("Arial", 25, "italic"))
word_text = canvas.create_text(400, 263, text="START", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


green_button_image = PhotoImage(file="images/right.png")
green_button = Button(image=green_button_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=word_is_known)
green_button.grid(row=1, column=0)

red_button_image = PhotoImage(file="images/wrong.png")
red_button = Button(image=red_button_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
red_button.grid(row=1, column=1)


window.mainloop()