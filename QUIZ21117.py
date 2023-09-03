# Main Menu, Version 1
# The user selects an option, which successfully takes them to the appropriately-titled Quiz window

# import statements
from tkinter import *
from functools import partial
import re


# Main window
class Menu:
    def __init__(self):
        self.menu_frame = Frame()
        self.menu_frame.grid()

        # Heading

        self.main_menu_label = Label(text="Main Maths Menu")
        self.main_menu_label.grid()

        # Select operation heading

        self.selection_label = Label(text="Select Quiz:")
        self.selection_label.grid()

        # Addition button

        self.addition_button = Button(text="+", command=lambda: self.quiz("Addition"))
        self.addition_button.grid()

        # Subtraction button

        self.subtraction_button = Button(text="-", command=lambda: self.quiz("Subtraction"))
        self.subtraction_button.grid()

        # Multiplication button

        self.multiplication_button = Button(text="x", command=lambda: self.quiz("Multiplication"))
        self.multiplication_button.grid()

        # Division button

        self.division_button = Button(text="/", command=lambda: self.quiz("Division"))
        self.division_button.grid()

    # Opens the Quiz window once operation has been selected, passing the operation into the Quiz class

    def quiz(self, operation):
        # print(operation)
        Quiz(self, operation)


class Quiz:
    def __init__(self, partner, operation):
        # Operation buttons disabled
        partner.addition_button.config(state=DISABLED)
        partner.subtraction_button.config(state=DISABLED)
        partner.multiplication_button.config(state=DISABLED)
        partner.division_button.config(state=DISABLED)

        self.quiz_box = Toplevel()
        self.quiz_box.protocol('WM_DELETE_WINDOW', partial(self.close_quiz, partner))

        self.quiz_frame = Frame(self.quiz_box)
        self.quiz_frame.grid()

        # Shows which quiz it is

        self.operation_label = Label(self.quiz_frame, text="{}".format(operation))
        self.operation_label.grid()

        self.quit_button = Button(self.quiz_frame, text="Quit", command=partial(self.close_quiz, partner))
        self.quit_button.grid()

    # The close_quiz function closes the Quiz window when "dismissed".

    def close_quiz(self, partner):
        partner.addition_button.config(state=NORMAL)
        partner.subtraction_button.config(state=NORMAL)
        partner.multiplication_button.config(state=NORMAL)
        partner.division_button.config(state=NORMAL)
        self.quiz_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Maths Quiz")
    something = Menu()
    root.mainloop()