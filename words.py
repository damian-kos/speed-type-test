from random import randint


class Words():

    def __init__(self):
        self.min_lines = 0
        self.words_to_textbox = self.fetch_words()

    # Initializes a set of words.
    def fetch_words(self):
        with open("english_dict.txt") as f:
            lines = f.readlines()
        # World record for WPM on keyboard is 219 in 2005.
        # So range 250 of words i senoguh.
        words = []
        for i in range(0, 250):
            words.append(lines[randint(0, len(lines))].replace("\n", ""))
        return words
