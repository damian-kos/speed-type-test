from tkinter import Tk, Frame, Text, Entry, Label, Button
from words import Words


class Gui():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.config()
        self.gui_frames()
        self.variables()

    def gui_frames(self):
        """" Defines GUI and put elemets in place """
        self.textbox_frame()
        self.words_in_textbox = self.textbox_tkinter()
        self.input_box = self.input_tkinter()
        self.stats_label_frame = self.stats_frame()
        self.wpm_frame = self.words_per_minute()
        self.cpm_frame = self.characters_per_minute()
        self.timer = self.timer_create()
        self.restart_button_frame = self.restart_button()

    def variables(self):
        """ Defines initial variables. They are later initialized 
        when program is restarted """
        # With every next word it is placed at its beginning.
        self.textbox_cursor_placement = 0
        self.word_count = 0
        self.words_entered_by_user = []
        self.current_word = self.loaded_words_from_dict[self.word_count]
        self.mistake_count = 0
        self.correct_count = 0
        self.cpm = 0
        self.end_results_frame = None
        self.time_remaining = 0
        self.countdown_is_on = False

    def textbox_frame(self):
        """ Textbox Frame setup"""
        self.text_frame = Frame(self.root, padx=50, pady=50)
        self.text_frame.place(relx=.5, rely=.4, anchor="c")

    def textbox_tkinter(self):
        """ Defines a Textbox with words for user to type in."""
        self.words_in_textbox = Words()
        self.loaded_words_from_dict = self.words_in_textbox.words_to_textbox
        self.text = Text(self.text_frame, bg="#848a85", width=40,
                         height=3, font=("Arial", 28), wrap="word")
        self.text.grid(row=0)
        # Both works, choose later on which suits better.
        # for word in text_box.words_in_textbox:
        #     self.text.insert("end", f"{word} ")
        self.text.insert("end", self.loaded_words_from_dict)
        self.text["state"] = "disabled"

        return (self.text)

    def restart_program(self):
        """ Destroys frames if necessary and recreates them to restart a
        program. Initializes initial variables. Rebuilds frames. """
        self.words_in_textbox.destroy()
        self.words_in_textbox = self.textbox_tkinter()
        self.wpm_frame = self.words_per_minute()
        self.cpm_frame = self.characters_per_minute()
        self.variables()
        self.highlight_current_word()
        self.input_word.config(state="normal")
        self.timer_label.configure(text="Time: 60s")
        self.result_frame.destroy()
        self.input_word.delete(0, "end")
        print(f"{self.current_word}")

    def restart_button(self):
        """ Restarts program."""
        Button(self.text_frame, text="Restart",
               command=self.restart_program).grid()

    def input_tkinter(self):
        """ Puts Entry box in text_frame """
        self.input_word = Entry(self.text_frame, width=40, font=(
            "Arial", 18))
        self.input_word.grid(pady=20)

    def results(self):
        """ After countdown is finished it creates a label with final
        results """
        self.result_frame = Frame(self.root)
        self.result_frame.place(relx=.5, rely=.8, anchor="c")
        end_results = {"Correct words: ": self.correct_count,
                       "Wrong words: ": self.mistake_count,
                       "Keystrokes: ": self.cpm
                       }
        for result in end_results:
            Label(self.result_frame,
                  text=f"{result}{end_results[result]}", width=20).grid(pady=5)

    def stats_frame(self):
        """ Creates a frame for countdown, wpm and cpm records. It is
        updated as users inputs words """
        self.stats_frame = Frame(self.root, bg="white")
        self.stats_frame.grid(padx=200, pady=100)

    def timer_create(self):
        """ Puts countdown timer in place """
        self.timer_label = Label(
            self.stats_label_frame, text="Timer: 60s", width=10)
        self.timer_label.grid(padx=100, column=0, row=0)

    def words_per_minute(self):
        """ Puts WPM label in place"""
        self.wpm_label = Label(
            self.stats_label_frame, text="WPM: ", width=10)
        self.wpm_label.grid(padx=100, column=1, row=0)

    def characters_per_minute(self):
        """ Puts CPM label in place"""
        self.cpm_label = Label(
            self.stats_label_frame, text="CPM: ", width=10)
        self.cpm_label.grid(padx=100, column=2, row=0)

    def get_word_from_input(self, event=None):
        """ Gets words from user input in Entry widget\n.
        Deletes whitespace characters from it.\n
        Appends list of words entered by user.\n
        Empties Entry widget later on."""
        self.word_to_check = self.input_word.get().replace(" ", "")
        self.check_if_word_is_correct()
        self.words_entered_by_user.append(self.word_to_check)
        self.input_word.delete(0, "end")

    def move_cursor(self, event=None):
        """ When countdown timer is running. Using word from user input.
        Moves cursor on the beginning of current word, starting with 0.
        Adds word count. Loads current_word from list of words loaded
        from dictionary of words. Scrolls text with users typing
        progress.
        """
        if self.countdown_is_on:
            self.get_word_from_input()
            self.textbox_cursor_placement += len(self.current_word)+1
            self.word_count += 1
            self.current_word = self.loaded_words_from_dict[self.word_count]
            self.text.see(
                f"{1.0} + {self.textbox_cursor_placement + 50} chars")
            print(f"{self.current_word} : {self.current_word_range}")
            self.highlight_current_word()
            self.config_wpm_label()
            self.config_cpm_label()

    def enter_word(self):
        """ Sends a user's entry """
        self.root.bind("<space>", lambda event: self.move_cursor())

    def get_current_word_index_range(self):
        """ Current word index range excluding whitespace after it."""
        self.current_word_range = (
            f"{1.0} + {self.textbox_cursor_placement} chars",
            f"{1.0} + "
            f"{self.textbox_cursor_placement  + len(self.current_word)} chars"
        )
        return self.current_word_range

    def check_if_word_is_correct(self):
        """ Check if words entered by user is correct. 
        Using words range. Highlights mistakes in red.\n
        Correct in green. Adds counts accordingly to correct or mistake
        count.
        """
        self.get_current_word_index_range()
        if self.word_to_check != self.current_word:
            self.mistake_count += 1
            self.text.tag_add(
                "mistake",
                self.current_word_range[0],
                self.current_word_range[1]
            )
            self.text.tag_config(
                "mistake", background="#848a85", foreground="red"
            )
            return
        if self.word_to_check == self.current_word:
            self.correct_count += 1
            self.text.tag_add(
                "correct",
                self.current_word_range[0],
                self.current_word_range[1]
            )
            self.text.tag_config(
                "correct", background="#848a85", foreground="#0d6918"
            )
            return

    def highlight_current_word(self):
        """ Highlights current word in green filled border"""
        self.get_current_word_index_range()
        self.text.tag_add(
            "highlight_current",
            self.current_word_range[0],
            self.current_word_range[1])
        self.text.tag_config("highlight_current",
                             background="#1b5913", foreground="#d3e3d1")

    def countdown(self, time_remaining=None):
        """ Countdown timer. When time is down Entry widget is disabled.
        """
        if time_remaining is not None:
            self.time_remaining = time_remaining
        if self.time_remaining <= 0:
            self.timer_label.configure(text="Time is up!")
            # Disables Entry widget
            self.input_word.config(state="disabled")
            # Puts results frame in place
            self.results()
            self.countdown_is_on = False
        else:
            self.timer_label.configure(text=f"Time: {self.time_remaining}s")
            self.time_remaining -= 1
            self.root.after(1000, self.countdown)

    def start_timer(self):
        """ If timer is not running it can be run """
        if not self.countdown_is_on:
            self.countdown(60)
        self.countdown_is_on = True

    def timer_bind(self):
        """ As soon as user starts typing and timer is not running 
        already it starts to countdown
        """
        self.root.bind("<KeyPress>", lambda event: self.start_timer())

    # Words per minute label config section
    """ Displays correct words per minute
    """

    def config_wpm_label(self):
        self.wpm_label.configure(text=f"WPM: {self.correct_count}")

    # Characters per minute label config section
    def config_cpm_label(self):
        """ Displays characters per minute """
        self.cpm = sum(len(word) for word in self.words_entered_by_user)
        self.cpm_label.configure(text=f"CPM: {self.cpm}")


window = Gui()
window.enter_word()
window.highlight_current_word()
window.timer_bind()
window.root.mainloop()
