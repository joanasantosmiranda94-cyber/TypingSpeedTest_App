from tkinter import *
import random

class TypingSpeed:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.config(padx=20, pady=20)
        self.root.resizable(False, False)

        # Game data
        self.words = [
            "python", "keyboard", "typing", "speed", "programming",
            "function", "variable", "loop", "string", "integer",
            "boolean", "condition", "syntax", "debug", "compile",
            "algorithm", "object", "class", "method", "import",
            "random", "canvas", "window", "button", "entry",
            "label", "frame", "widget", "event", "timer",
            "score", "accuracy", "result", "restart", "start",
            "pause", "input", "output", "logic", "array",
            "list", "tuple", "dictionary", "index", "value"
        ]

        self.current_word = ""
        self.score = 0
        self.best_score = 0
        self.time_left = 60
        self.timer_running = False

        self.create_widgets()

    # -------------------- GUI --------------------
    def create_widgets(self):
        # Top frame
        top_frame = Frame(self.root, bg="lightgray")
        top_frame.pack(pady=10, fill="x")

        Label(top_frame, text="Your score:", bg="lightgray").pack(side=LEFT, padx=10)
        self.score_label = Label(top_frame, text="0", bg="lightgray")
        self.score_label.pack(side=LEFT)

        Label(top_frame, text="Best score:", bg="lightgray").pack(side=LEFT, padx=10)
        self.best_score_label = Label(top_frame, text="0", bg="lightgray")
        self.best_score_label.pack(side=LEFT)

        Label(top_frame, text="WPM:", bg="lightgray").pack(side=LEFT, padx=10)
        self.wpm_label = Label(top_frame, text="0", bg="lightgray")
        self.wpm_label.pack(side=LEFT, padx=5)

        self.timer_label = Label(
            top_frame, text=f"Time: {self.time_left}",
            bg="lightgray", font=("Arial", 12, "bold")
        )
        self.timer_label.pack(side=RIGHT, padx=10)

        # Middle frame
        middle_frame = Frame(self.root)
        middle_frame.pack(pady=10)

        self.wordsboard = Canvas(
            middle_frame, width=500, height=200,
            bg="lightgray", highlightthickness=1,
            highlightbackground="black"
        )
        self.wordsboard.pack()

        # Bottom frame
        bottom_frame = Frame(self.root)
        bottom_frame.pack(pady=10)

        self.words_entry = Entry(bottom_frame, width=56)
        self.words_entry.pack()
        self.words_entry.bind("<KeyRelease>", self.start_game)
        self.words_entry.bind("<Return>", self.check_word)

        self.restart_btn = Button(
            bottom_frame, text="Restart",
            width=15, command=self.restart_game
        )
        self.restart_btn.pack(pady=10)

        self.load_new_word()

    # -------------------- Game logic --------------------
    def load_new_word(self):
        self.wordsboard.delete("all")

        new_word = random.choice(self.words)
        while new_word == self.current_word:
            new_word = random.choice(self.words)

        self.current_word = new_word
        self.wordsboard.create_text(
            250, 100,
            text=self.current_word,
            font=("Arial", 28, "bold")
        )
        self.words_entry.delete(0, END)

    def check_word(self, event):
        if self.time_left <= 0 or not self.timer_running:
            return
        if self.words_entry.get().strip() == self.current_word:
            self.score += 1
        self.load_new_word()

    def update_score(self):
        self.score_label.config(text=str(self.score))
        if self.score > self.best_score:
            self.best_score = self.score
            self.best_score_label.config(text=str(self.best_score))

    def update_wpm(self):
        minutes = 60 / 60  # tempo do jogo em minutos (1 min)
        wpm = int(self.score / minutes)
        self.wpm_label.config(text=str(wpm))

    def restart_game(self):
        self.score = 0
        self.time_left = 60
        self.timer_running = False

        self.timer_label.config(text="Time: 60")
        self.score_label.config(text="0")

        self.words_entry.config(state="normal")
        self.words_entry.delete(0, END)
        self.words_entry.focus()

        self.wordsboard.delete("all")
        self.load_new_word()

    # -------------------- Timer --------------------
    def start_game(self, event=None):
        if not self.timer_running and self.words_entry.get():
            self.timer_running = True
            self.countdown()

    def countdown(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.root.after(1000, self.countdown)
        else:
            self.end_game()

    def end_game(self):
        self.timer_label.config(text="Time: 0")
        self.words_entry.config(state="disabled")

        self.wordsboard.delete("all")
        self.wordsboard.create_text(
            250, 75,
            text=f"Your time is up, your score was {self.score} words",
            font=("Arial", 20, "bold"),
            fill="black"
        )

        self.update_score()  # atualiza score e best score
        self.update_wpm()  # atualiza o WPM


# -------------------- MAIN --------------------
if __name__ == "__main__":
    root = Tk()
    app = TypingSpeed(root)
    root.mainloop()
