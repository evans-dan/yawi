global_word_list_file = 'words.txt'
#global_word_list_file = 'words_wordle_nytimes.txt'
class Wordle_Game:
    """
    A single game of Wordle
    Does not implement 'hard mode' where any revealed hints must be used in
    subsequent guesses
    """
    import random

    def __init__(self, max_rounds=6, word_length=5, word_list_file=global_word_list_file):
        """
        Create a new Wordle_Game object.
        Inputs: Default settings are Wordle-like, with a default word list as
            the five-letter words found in /usr/share/dict/words on an Ubuntu
            20 machine; word_list_file can be any readable file with one word
            per line; words will be size-checked during file parsing.
        Outputs: a Wordle_Game object ready to take guesses and play.
        """
        self.max_rounds = max_rounds
        self.word_list_file = global_word_list_file
        self.round_counter = 0
        self.word_length = word_length
        self.word_list = self._parse_word_list()
        self.guesses = []
        self.scores = []
        self.__secret_word = '' # the word a player is trying to guess. Not available outside the class
        self.game_won = None # set to true when the secret word is guessed; false if round limit is hit before that happens
        self.messages = [] # all  output from interactions with the game are appended here
        self._choose_secret_word() # grab a word after the list is initialized

    def _choose_secret_word(self):
        """
        Sets the secret word as a random word from the list of words in self.word_list
        Inputs: None
        Outputs: none; changes local attributes
        """
        self.__secret_word = self.word_list[self.random.randint(0,len(self.word_list))]

    def _parse_word_list(self):
        """
        Parse the supplied word list file into a list. Parses the value stored in self.word_list_file
        Inputs: None
        Outputs: a list of words from the global word source that match the defined word length
        """
        wl = []
        with open(self.word_list_file, "r") as fh:
            word = fh.readline()
            while word: # for each word in the file
                word = str.strip(word).upper()

                if(len(word) == self.word_length):

                    wl.append(word)

                word = fh.readline()

        fh.close()
        return wl

    def parse_guess(self, guess):
        """
        Parse a single guess from the player, score it, and return the result.
        Inputs: a single string
        Outputs: Adds result messages to the local messages queue: scoring, and
            success/failure/error messages.
        """

        if self.game_won is None: # the game hasn't been won or lost yet

            if guess.upper() not in self.word_list: # don't hold guesses not in the word list against the player

                self.messages.append("{0} not a legal guess, round count still {1}".format(guess.upper(), self.round_counter))

            else:

                self.round_counter += 1
                self.guesses.append(guess.upper())
                self.messages.append(self._score_guess())

                if self.guesses[-1] == self.__secret_word: # player guessed the secret word!

                    self.game_won = True

                else:

                    if self.round_counter == self.max_rounds: # that was the last round, so no more guessing

                        self.game_won = False

    def _score_guess(self):
        """
        Score the guess. This will include letters that are:
            right (right letter, right place): upper case
            included (right letter, wrong place): lower case
            missing (not in the word): a dot
        Inputs: none.
        Outputs: scoring string of upper/lower/dot characters.
        """

        guess_score = []
        guess = self.guesses[-1]
        answer = ''

        for i in range(len(guess)):
            if guess[i] == self.__secret_word[i]:
                guess_score.append(guess[i].upper())
            elif guess[i] in self.__secret_word:
                guess_score.append(guess[i].lower())
            else:
                guess_score.append('.')

        return "".join(guess_score)

    def __str__(self):
        """
        Print out the game parameters
        Inputs: none.
        Outputs: string representation of some of the game settings
        """

        return "Wordle Game (maximum rounds=" + str(self.max_rounds) + ", word length=" + str(self.word_length) + ", word list=" + str(self.word_list_file) + ", word count=" + str(len(self.word_list)) + ")"
