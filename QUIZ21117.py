# import statements
from tkinter import *
from functools import partial
import re
import random


# Quiz main class, with control buttons, quiz, menu of operations
class Quiz:
    def __init__(self):

        self.menu_frame = Frame(width=300, pady=10, height=600)
        self.menu_frame.grid()

        self.main_menu_label = Label(self.menu_frame, text="Main Maths Menu", justify=CENTER, font="Helvetica 18",
                                     padx=10, pady=10)
        self.main_menu_label.grid(row=0)

        # The number of questions asked, initially zero

        self.question_number = 0

        # The number of a quiz completed at any instant, initially zero

        self.quiz_number = 0

        # The string that contains the entire history of quizzes completed in the session, initially empty

        self.quiz_history = ""

        # The string that contains the data of each quiz, intially empty

        self.quiz_string = ""

        # The number of questions answered correctly

        self.correct_number = 0

        # The list of questions, initially empty

        self.question_list = []

        # The list of correspondnig correct answers, intially empty

        self.correct_answers = []

        # The list of user's answers, intially empty

        self.answers = []

        # The score for each quiz, intially zero

        self.score = 0

        # The constant for maximum number of quizzes, 4 at the moment

        self.max_quiz_number = 4

        # The constant for the number of questions per quiz, 2 at the moment

        self.no_questions = 2

        # The lowest number in the range of numbers randomly generated

        self.lowest_number = 1

        # The highest number in the range of numbers randomly generated

        self.highest_number = 10

        # Selection label

        self.selection_label = Label(self.menu_frame, text="Select Quiz", font="Helvetica 12", justify=CENTER, padx=10,
                                     pady=10)
        self.selection_label.grid(row=1)

        self.operations_frame = Frame()
        self.operations_frame.grid()

        # Addition button, passes operation as "addition" to generate addition questions in function

        self.addition_button = Button(self.operations_frame, text="Addition +",
                                      command=lambda: self.generate_questions("Addition"), padx=10, pady=10,
                                      font="Helvetica 12", bg="cyan")
        self.addition_button.grid(row=4, column=1)

        # Subtraction button, passes operation as "subtraction" to generate subtraction questions in function

        self.subtraction_button = Button(self.operations_frame, text="Subtraction -",
                                         command=lambda: self.generate_questions("Subtraction"), padx=10, pady=10,
                                         font="Helvetica 12", bg="magenta")
        self.subtraction_button.grid(row=4, column=2)

        # Multiplication button, passes operation as "multiplication" to generate multiplication questions in function

        self.multiplication_button = Button(self.operations_frame, text="Multiplication x",
                                            command=lambda: self.generate_questions("Multiplication"), padx=10, pady=10,
                                            font="Helvetica 12", bg="orange")
        self.multiplication_button.grid(row=4, column=3)

        # Division button, passes oepration as "division" to generate division questions in function

        self.division_button = Button(self.operations_frame, text="Division /",
                                      command=lambda: self.generate_questions("Division"), padx=10, pady=10,
                                      font="Helvetica 12", bg="yellow")
        self.division_button.grid(row=4, column=4)

        self.quiz_frame = Frame()
        self.quiz_frame.grid()

        # Operation label

        self.operation_label = Label(self.quiz_frame, text="", justify=CENTER)
        self.operation_label.grid(row=1, column=0)

        # Start button that calls the display question function, to display the first generated question

        self.start_button = Button(self.quiz_frame, text="Start", command=lambda: self.display_question(),
                                   state=DISABLED, justify=CENTER, padx=5, pady=5, font="Helvetica 12", bg="white")
        self.start_button.grid(row=2, column=0)

        # Where all the questions show

        self.question_label = Label(self.quiz_frame, text="Questions will appear here.", justify=CENTER,
                                    font="Helvetica 12", padx=10, pady=10)
        self.question_label.grid(row=3, column=0)

        # Where the user enters their answers

        self.answer_entry = Entry(self.quiz_frame, state=DISABLED, justify=CENTER, font="Helvetica 12")
        self.answer_entry.grid(row=4, column=0)

        # Where the validation output is shown e.g. "correct", "incorrect", "enter a number!"

        self.result_label = Label(self.quiz_frame, text="", justify=CENTER, font="Helvetica 12")
        self.result_label.grid(row=5, column=0)

        self.buttons_frame = Frame()
        self.buttons_frame.grid()

        # Check button to check whether or not the user's answer is valid, and then if it is correct or incorrect

        self.check_button = Button(self.buttons_frame, text="Check", state=DISABLED, command=lambda: self.check(),
                                   padx=5, pady=5, font="Helvetica 12", bg="LightGoldenrod")
        self.check_button.grid(row=0, column=0)

        # Nex button to call the next function - determining what happens next in the program

        self.next_button = Button(self.buttons_frame, text="Next", state=DISABLED, command=lambda: self.next(), padx=5,
                                  pady=5, font="Helvetica 12", bg="LightGoldenrod1")
        self.next_button.grid(row=0, column=1)

        # The user can choose to quit at any time, enabling the four operation buttons again in doing so

        self.quit_button = Button(self.buttons_frame, text="Quit", state=DISABLED, command=self.close_quiz, padx=5,
                                  pady=5, font="Helvetica 12", bg="LightGoldenrod2")
        self.quit_button.grid(row=0, column=2)

        # The history button, enabled only when at least one quiz has been completed, and has the quiz history string passed into it to display full history

        self.history_button = Button(self.buttons_frame, state=DISABLED, text="View History",
                                     command=lambda: self.show_results(self.quiz_history), padx=5, pady=5,
                                     font="Helvetica 12", bg="LightGoldenrod3")
        self.history_button.grid(row=0, column=3)

        self.export_frame = Frame()
        self.export_frame.grid()

        # The export button, enabled only when at least one quiz has been completed, and has the quiz history passed into it to export full history

        self.show_export_button = Button(self.export_frame, text="Export", justify=CENTER, state=DISABLED,
                                         command=lambda: self.export(self.quiz_history), padx=100, pady=5,
                                         font="Helvetica 12", bg="#9A9AFF")
        self.show_export_button.grid(row=1, column=0)

        # The fun zone button, activated only when the user scores 100% one any given quiz

        self.fun_zone_button = Button(self.export_frame, text="Fun Zone", justify=CENTER, state=DISABLED,
                                      command=self.fun, padx=100, pady=5, font="Helvetica 12", bg="gold")
        self.fun_zone_button.grid(row=1, column=1)

        # The help button, which opens the Help/Instructions window, open at all times

        self.help_button = Button(self.export_frame, text="Help", justify=CENTER, command=self.help, padx=100, pady=5,
                                  font="Helvetica 12", bg="silver")
        self.help_button.grid(row=1, column=2)

        # Function to open the export window, with the full quiz history as a parameter

    def export(self, quiz_history):
        Export(self, quiz_history)

        # Function to open the fun window

    def fun(self):
        Fun(self)

        # Function to open the help window

    def help(self):
        Help(self)

        # Function to generate questions, using the selected operation from the menu above

    def generate_questions(self, operation):
        # No access to fun zone, even after viewing it once after scoreing 100%
        self.fun_zone_button.config(state=DISABLED)
        # The number of questions asked set back to zero each time a new quiz starts
        self.question_number = 0
        # The score set back to zero each time a new quiz starts
        self.score = 0
        # The number of questions answered correctly set back to zero each time a quiz starts
        self.correct_number = 0
        # The question list, answers list and correct answers list are all emptied at the start of a new quiz, to hold new questions/answers/scores
        self.question_list.clear()
        self.answers.clear()
        self.correct_answers.clear()
        # The statistics of the last quiz is emptied
        self.quiz_string = ""
        # For the number of questions per quiz, two numbers, between the constant boundaries, are generated
        for i in range(self.no_questions):
            num1 = random.randint(self.lowest_number, self.highest_number)
            num2 = random.randint(self.lowest_number, self.highest_number)
            # Based on the selected operation, a question (and corresponding answer) is formed using these numbers.
            if operation == "Addition":
                question = "{} + {} = ?".format(num1, num2)
                correct_answer = num1 + num2

            elif operation == "Subtraction":
                question = "{} - {} = ?".format(num1, num2)
                correct_answer = num1 - num2

            elif operation == "Multiplication":
                question = "{} x {} = ?".format(num1, num2)
                correct_answer = num1 * num2

            else:
                while num1 % num2 != 0:
                    # Ensures division questions are doable for age group i.e. uncomplicated to do manually
                    num1 = random.randint(self.lowest_number, self.highest_number)
                    num2 = random.randint(self.lowest_number, self.highest_number)
                question = "{} / {} = ?".format(num1, num2)
                correct_answer = num1 / num2

            self.question_list.append(question)
            self.correct_answers.append(correct_answer)

            # The lists are updated above, and the user is free to start the quiz
            self.start_button.config(state=NORMAL)

    # A function to display the questions, starting from the first
    def display_question(self):
        # The users are able to enter an answer, quit, check their answer
        # The users are not able to restart the quiz, choose another operation, move onto the next question etc
        self.answer_entry.config(state=NORMAL)
        self.quit_button.config(state=NORMAL)
        self.start_button.config(state=DISABLED)
        self.question_label.configure(text=self.question_list[self.question_number])
        self.check_button.config(state=NORMAL)
        self.history_button.config(state=DISABLED)
        self.addition_button.config(state=DISABLED)
        self.subtraction_button.config(state=DISABLED)
        self.multiplication_button.config(state=DISABLED)
        self.division_button.config(state=DISABLED)

        # The check function validates input and processes to give appropriate output

    def check(self):
        self.check_button.config(state=NORMAL)
        answer = self.answer_entry.get()
        # Answer retrieved
        # Answer is only accepted if it is int/float, but not string or blank
        # The user is forced to give the valid input before being able to progress further
        try:

            if float(answer) == float(self.correct_answers[self.question_number]):
                self.correct_number += 1
                # If the user's answer matches the corresponding correct answer, one is added to the number of questions answered correctly
                self.result_label.configure(text="Correct!", fg="green")
                # Gives output "correct"
            else:
                self.result_label.configure(text="Incorrect!", fg="red")
                # Otherwise gives output "incorrect"

            self.answers.append(answer)
            # Answers list updated
            self.next_button.config(state=NORMAL)
            # User able to proceed to next question
            self.answer_entry.configure(bg="white")

        except ValueError:
            # Forces the user to add valid input i.e. a number or integer, no blanks or strings
            self.result_label.configure(text="Enter a number!")
            self.answer_entry.configure(bg="red")

    # The next function, which determines what happens next in the quiz, called when next button is clicked, or after the answer has been checked
    def next(self):
        self.check_button.config(state=NORMAL)
        self.question_number += 1
        # One is added to the number of questions asked/answered
        self.result_label.configure(text="")
        # Answer entry cleared
        self.answer_entry.delete(0, END)
        # If the quiz iz complete:
        if self.question_number == len(self.question_list):
            # self.show_export_button.config(state=NORMAL)
            self.quiz_number += 1
            # One is added to the quiz number (or number of quizzes)
            # The user is unable to do any more questions, but can view the Quiz History

            self.next_button.config(state=DISABLED)
            self.history_button.config(state=NORMAL)
            self.question_label.configure(text="")
            # The user is unable to start a new quiz without selecting one of the four operations
            self.start_button.config(state=DISABLED)
            # The user can only export quiz history if they have completed at least 1 quiz
            if self.quiz_number >= 1:
                self.show_export_button.config(state=NORMAL)
            # The application carries on until the number of quizzes has reached the maximum, in which case the operation buttons remain disabled after completing the last quiz
            if self.quiz_number != self.max_quiz_number:
                self.addition_button.config(state=NORMAL)
                self.subtraction_button.config(state=NORMAL)
                self.multiplication_button.config(state=NORMAL)
                self.division_button.config(state=NORMAL)
            self.answer_entry.delete(0, END)
            self.answer_entry.config(state=DISABLED)
            self.result_label.configure(text="")
            # Control buttons are disabled
            self.quit_button.config(state=DISABLED)
            self.check_button.config(state=DISABLED)
            # The score for quiz is correctly calculated
            self.score += self.correct_number / self.question_number * 100
            # The score is shown
            self.question_label.configure(text="Score: {}%".format(self.score))
            # Fun zone is activated if the score is 100%
            if self.score == 100:
                self.fun_zone_button.config(state=NORMAL)
            # For each question in the list, the quiz string is updated to include the question, correct answers and user's answer
            for question in self.question_list:
                index = self.question_list.index(question)
                self.quiz_string += question + "    " + str(
                    self.correct_answers[index]) + "     " + "You entered: " + str(self.answers[index]) + "\n"

            # The overall quiz history includes the quiz number, score and quiz string, for each quiz

            self.quiz_history += "Quiz no. " + str(self.quiz_number) + "\n" + "Score: " + str(
                self.score) + "%" + "\n" + self.quiz_string + "\n"

            # The user cannot quit as the quiz has finished, but can view the History

            self.history_button.config(state=NORMAL)

            self.quit_button.config(state=DISABLED)

        else:
            # shows the next question, unable make further progress until the answer is processed
            self.display_question()
            self.next_button.config(state=DISABLED)

    # The quiz closes

    def close_quiz(self):
        # Question label clears
        self.question_label.configure(text="")
        # The user is able to choose any of the four operations
        self.addition_button.config(state=NORMAL)
        self.subtraction_button.config(state=NORMAL)
        self.multiplication_button.config(state=NORMAL)
        self.division_button.config(state=NORMAL)
        # The answer entry clears and they cannot operate a quiz until they have selected a new operation
        self.answer_entry.delete(0, END)
        self.answer_entry.config(state=DISABLED)
        self.result_label.configure(text="")
        self.quit_button.config(state=DISABLED)
        self.next_button.config(state=DISABLED)
        self.check_button.config(state=DISABLED)
        self.start_button.config(state=DISABLED)

    # Function to show the result, or history, into which the overall quiz history is passed
    def show_results(self, quiz_history):
        Results(self, quiz_history)


# The Results window, where the quiz history is shown
class Results:
    def __init__(self, partner, quiz_history):
        self.results_box = Toplevel()
        self.results_box.protocol('WM_DELETE_WINDOW', partial(self.close_results, partner))

        self.results_frame = Frame(self.results_box, width=300, padx=10, pady=10)
        self.results_frame.grid()

        self.response_label = Label(self.results_frame, text="Response", justify=CENTER, pady=10, font="Helvetica 16")
        self.response_label.grid(row=0)

        self.heading_label = Label(self.results_frame, text="Questions, Correct Answers, Your Answers", justify=CENTER,
                                   pady=10, font="Helvetica 12")
        self.heading_label.grid(row=1)

        self.quiz = Label(self.results_frame, text=quiz_history, justify=CENTER, font="Helvetica 8")
        self.quiz.grid(row=2)

        # Displays the quiz history passed as a parameter above

        self.back_button = Button(self.results_frame, text="Back", command=partial(self.close_results, partner), padx=5,
                                  pady=5, font="Helvetica 12", bg="white")
        self.back_button.grid()

        # Closes Results window

    def close_results(self, partner):
        self.results_box.destroy()


# Fun Zone window
class Fun:
    def __init__(self, partner):
        self.fun_box = Toplevel()
        self.fun_box.protocol('WM_DELETE_WINDOW', partial(self.close_fun, partner))

        self.fun_frame = Frame(self.fun_box, width=300, padx=10, pady=10)
        self.fun_frame.grid()

        # List of fun maths jokes/facts

        self.fun_list = ["Why was six scared of seven? \n Because seven eight nine!",
                         "You don't know maths until you do maths.", "The number 2 is the only even prime number.",
                         "Mathematicians like maths not because they are good at it, but because they like to take on challenges.",
                         "Practice makes perfect!", "Why was the geometry adorable? \n Because it had acute angles!",
                         "All the internal angles in a triangle add to 180 degrees.",
                         "Parallel lines have so much in common...it's a shame they will never meet!",
                         "Which tables do you not have to learn? Dinner tables!",
                         "Why did the teacher get upset when the student called her average? \n Because it was a 'mean' thing to say!"]

        self.response_label = Label(self.fun_frame, text="Fun Zone", justify=CENTER, pady=10, font="Helvetica 16")
        self.response_label.grid(row=0)

        # Fact is randomly chosen

        self.fun_fact = random.choice(self.fun_list)

        # Random fact is displayed

        self.fun = Label(self.fun_frame, text=self.fun_fact, justify=CENTER, font="Helvetica 10")
        self.fun.grid(row=2)

        self.back_button = Button(self.fun_frame, text="Back", command=partial(self.close_fun, partner), padx=5,
                                  pady=10, font="Helvetica 12", bg="white")
        self.back_button.grid()

        partner.fun_zone_button.config(state=DISABLED)

        # Closes Fun window

    def close_fun(self, partner):
        self.fun_box.destroy()


# Help/Instructions class

class Help:
    def __init__(self, partner):
        self.help_box = Toplevel()
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, padx=10, pady=10)
        self.help_frame.grid()

        self.heading = Label(self.help_frame, text="Help/Instructions", font="Helvetica 16")
        self.heading.grid(row=1)

        # Instructions are displayed

        self.help = Label(self.help_frame, font="Helvetica 10",
                          text="Choose a quiz from the four operations.\nEverytime you score a 100%, you get access to Fun Zone, where you get a cool Maths Fact or Maths joke as a treat!\nYou can complete up to four quizzes in one session.\n",
                          justify=CENTER)
        self.help.grid(row=2)

        self.back_button = Button(self.help_frame, text="Back", command=partial(self.close_help, partner),
                                  font="Helvetica 12", padx=5, pady=5, bg="white")
        self.back_button.grid(row=3)

        # Closes Help window

    def close_help(self, partner):
        self.help_box.destroy()


# Export window, with quiz history passed as parameter to write to a text file and export
class Export:
    def __init__(self, partner, quiz_history):
        background = "white"
        partner.show_export_button.config(state=DISABLED)
        self.export_box = Toplevel()
        # Headings, buttons and labels outlined below
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))
        self.export_frame = Frame(self.export_box, width=300, bg=background)
        self.export_frame.grid()

        self.how_heading = Label(self.export_frame, text="Export", bg=background, font="Helvetica 16")
        self.how_heading.grid(row=0)

        self.export = Label(self.export_frame, font="Helvetica 12",
                            text="Save your quiz session history to a text file.", justify=LEFT, width=40,
                            bg=background)
        self.export.grid(row=1)

        # Warning

        self.export_text = Label(self.export_frame, font="Helvetica 12",
                                 text="If the filename you enter below already exists, its content will be replaced with your quiz history from this session.",
                                 justify=LEFT, fg="maroon", padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)

        # The user enters a filename below

        self.filename_entry = Entry(self.export_frame, width=20, justify=LEFT, font="Helvetica 12")
        self.filename_entry.grid(row=3, pady=10)

        # Shows the potential error in filename

        self.save_error_label = Label(self.export_frame, text="", fg="red", bg=background)
        self.save_error_label.grid(row=4)

        self.save_cancel_frame = Frame(self.export_frame)
        self.save_cancel_frame.grid(row=5, pady=10)
        # The save history function is called when the save button is clicked - to confirm the validity of the filename
        self.save_button = Button(self.save_cancel_frame, padx=5, pady=5, font="Helvetica 12", text="Save",
                                  command=partial(lambda: self.save_quiz(partner, quiz_history)))
        self.save_button.grid(row=5, column=0)
        # The window closes should the user choose to click Cancel
        self.cancel_button = Button(self.save_cancel_frame, padx=5, pady=5, font="Helvetica 12", text="Cancel",
                                    command=partial(self.close_export, partner), bg="white")
        self.cancel_button.grid(row=5, column=1)

        # Close export function called to close the Export window if user cancels

    def close_export(self, partner):
        partner.show_export_button.config(state=NORMAL)
        self.export_box.destroy()
        # The save history function that confirms the validity of the filename before successfully exporting it

    def save_quiz(self, partner, quiz_history):
        valid_char = "[A-Za-z0-9_]"  # Common way out outlining filename conditions
        has_error = "no"
        # User enters filename here
        filename = self.filename_entry.get()
        print(filename)
        # Checks filename to rule out blank spaces and apostrophes - forces the user to enter a valid filename
        for letter in filename:
            if re.match(valid_char, letter):
                continue
            elif letter == " ":
                problem = "(no spaces allowed)"
            else:
                problem = ("(no {}'s allowed)".format(letter))
            has_error = "yes"
            break

        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

        # If there are errors, the type of error is displayed
        if has_error == "yes":
            self.save_error_label.config(text="Invalid filename - {}".format(problem))
            self.filename_entry.config(bg="pink")
            print()
        else:  # Otherwise, the file is successfully exported
            filename = filename + ".txt"
            f = open(filename, "w+")
            # Quiz number, score, questions, answers and correct answers all written to text file, per quiz completed
            for item in quiz_history:
                f.write(item)
            f.close()

            self.close_export(partner)  # Export window closes after operation is successfully complete


# main routine

if __name__ == "__main__":
    root = Tk()
    root.title("Maths Quiz")
    something = Quiz()
    root.mainloop()