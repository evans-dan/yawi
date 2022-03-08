class Wordle_Game:
    """
    A single game of Wordle
    Does not implement 'hard mode' where any revealed hints must be used in
    subsequent guesses
    """
    import random
    import sys

    def __init__(self, max_rounds=6, word_length=5, word_list_file='words.txt', answer_list_file=None, debug=False, hard_mode=False):
        """
        Create a new Wordle_Game object.
        Inputs: Default settings are Wordle-like, with a default word list as
            the five-letter words found in /usr/share/dict/words on an Ubuntu
            20 machine; word_list_file can be any readable file with one word
            per line; words will be size-checked during file parsing.
            Hard mode means that any revealed letters (correct or included)
            must be used in subsequent guesses.
        Outputs: a Wordle_Game object ready to take guesses and play.
        """
        # Game constants:
        self.debug = debug
        self.max_rounds = max_rounds
        self.word_length = word_length
        self.word_list_file = word_list_file
        self.answer_list_file = answer_list_file

        # Word lists:
        self.word_list = set(self._parse_word_list(self.word_list_file))
        # If a dedicated answer list is used, append it to the word list.
        self.answer_list = self._parse_word_list(self.answer_list_file)
        if len(self.answer_list):
                self.word_list.update(self.answer_list)

        # Game state:
        self.round_counter = 0
        self.guesses = []
        self.scores = []
        self.__secret_word = '' # the word a player is trying to guess. Not available outside the class
        self.game_won = None # set to true when the secret word is guessed; false if round limit is hit before that happens
        self.messages = [] # all  output from interactions with the game are appended here
        self._hard_mode = hard_mode # if True, revealed letters (correct or included) must be used in subsequent guesses
        self._revealed_letters = [] # a list of letters that have been revealed (either included or correct) for use with hard mode
        self._choose_secret_word() # grab a word after the list is initialized

    def _choose_secret_word(self):
        """
        Sets the secret word as a random word from the list of words in self.word_list
        Inputs: None
        Outputs: none; changes local attributes
        """
        # Use the dedicated answer list if there is one, otherwise use the full word list.
        word_list = self.answer_list
        if len(word_list) == 0:
                word_list = list(self.word_list)
        self.__secret_word = self.random.choice(word_list)
        if self.debug:
                print(f"Secret word is {self.__secret_word}", file=self.sys.stderr)

    def _parse_word_list(self, pathname):
        """
        Parse the supplied word list file into a list. Opens and parses the specified pathname.
        Inputs: None
        Outputs: a list of uppercased words from the word source that match the defined word length
        """
        wl = []
        if pathname == None:
               return wl
        with open(pathname, "r") as fh:
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

            valid_word = True
            if guess.upper() not in self.word_list: # don't hold guesses not in the word list against the player

                self.messages.append(f"{guess.upper()} not a legal guess, round count still {self.round_counter}")
                valid_word = False

            hard_mode_pass = True
            if self._hard_mode: # ensure guess contains all revealed letters

                for rev_letter in self._revealed_letters:
                    if rev_letter not in guess:
                        self.messages.append(f"{guess.upper()} does not include all revealed letters, round count still {self.round_counter}")
                        hard_mode_pass = False

            if valid_word and hard_mode_pass: # requirements passed, so score the test

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

        guess_score = ['.'] * self.word_length
        guess = list(self.guesses[-1])
        secret = list(self.__secret_word)

        # Matching must be done in phases to avoid over-crediting a letter
        # or a position. For example, when the same letter appears twice in
        # a guess, but only once in the answer: the second letter is a miss
        # not a mismatch.

        # Find all exact matches. On match, remove letter from future matching
        # but retain letter positions.
        for i in range(self.word_length):
            if guess[i] == secret[i]:
                guess_score[i] = guess[i].upper()
                guess[i] = ' '
                secret[i] = ' '

                if guess[i] not in self._revealed_letters: # add to list of revealed letters for hard mode
                    self._revealed_letters.append(guess[i].upper())

        # Find any still-matchable but misplaced letters, removing them from
        # future consideration.
        for i in range(self.word_length):
            if guess[i] != ' ' and guess[i] in secret:
                guess_score[i] = guess[i].lower()
                secret.remove(guess[i])

                if guess[i] not in self._revealed_letters: # add to list of revealed letters for hard mode
                    self._revealed_letters.append(guess[i].upper())

        return "".join(guess_score)

    def __str__(self):
        """
        Print out the game parameters
        Inputs: none.
        Outputs: string representation of some of the game settings
        """
        report = f"Wordle Game (maximum rounds={self.max_rounds}"
        report += f", word length={self.word_length}"
        report += f", word list={self.word_list_file}"
        report += f", word count={len(self.word_list)}"
        report += f", hard mode={self._hard_mode}"
        if len(self.answer_list):
                report += f", answer list={self.answer_list_file}"
                report += f", answer count={len(self.answer_list)}"
        report += ")"

        return report


import unittest

class Test_Wordle_Game(unittest.TestCase):
        import tempfile

        def test_bad_word_list(self):
                with self.assertRaisesRegex(FileNotFoundError, r"::NOPE::"):
                        game = Wordle_Game(word_list_file='::NOPE::')

        def test_bad_answer_list(self):
                with self.assertRaisesRegex(FileNotFoundError, r"::MISSING::"):
                        game = Wordle_Game(answer_list_file='::MISSING::')

        def make_word_file(self, word_list):
                if len(word_list) == 0:
                        return None
                word_file = self.tempfile.NamedTemporaryFile(mode="wt")
                for word in word_list:
                        print(word, file=word_file)
                word_file.flush()
                return word_file

        def validate_words(self, word_list, expected):
                self.assertEqual(len(word_list), len(expected))
                for word in expected:
                        self.assertTrue(word in word_list)

        def test_uppercasing(self):
                incoming = ["drink", "vOdKa", "YUMMY"]
                expected = ["DRINK", "VODKA", "YUMMY"]

                word_file = self.make_word_file(incoming)
                game = Wordle_Game(word_list_file=word_file.name)
                self.validate_words(game.word_list, expected)

        def test_word_length_respected(self):
                incoming = ["give", "me", "all", "you", "got", "right", "now", "dude"]
                expected = ["GIVE", "DUDE"]

                word_file = self.make_word_file(incoming)
                game = Wordle_Game(word_length=4, word_list_file=word_file.name)
                self.validate_words(game.word_list, expected)

        def test_duplicates_eliminated(self):
                incoming = ["OnE", "Two", "oNe"]
                expected = ["ONE", "TWO"]

                word_file = self.make_word_file(incoming)
                game = Wordle_Game(word_length=3, word_list_file=word_file.name)
                self.validate_words(game.word_list, expected)

        def test_guess_score(self):
            # "guess" must be non-empty to initialize the game, but it will
            # be ignored because we're calling _score_guess directly.
            guesses = ["hello"]
            answers = ["vivid"]
            expected = [
                            ["snack", "....."],
                            ["wordy", "...d."],
                            ["votes", "V...."],
                            ["irate", "i...."],
                            ["igigi", "i.i.."],
                            ["vitai", "VI..i"],
                            ["vidai", "VId.i"],
                            ["divid", ".IVID"],
                            ["viviv", "VIVI."],
                    ]

            guess_file = self.make_word_file(guesses)
            answer_file = self.make_word_file(answers)

            game = Wordle_Game(max_rounds=len(expected), word_list_file=guess_file.name, answer_list_file=answer_file.name)

            for guess, score in expected:
                    game.guesses.append(guess.upper())
                    self.assertEqual(score, game._score_guess())

        def test_choose_from_answer_list(self):
                guesses = ["eeeeK", "nopes", "sosad"]
                answers = ["goody", "smart", "wheee"]

                guess_file = self.make_word_file(guesses)
                answer_file = self.make_word_file(answers)

                # Selected word must be in answers if answer list given.
                game = Wordle_Game(word_list_file=guess_file.name, answer_list_file=answer_file.name)
                won = False
                for word in answers:
                        game.parse_guess(word.lower())
                        if game.game_won:
                                won = True
                self.assertTrue(won)

                # Selected word must be in guesses if no answer list given.
                game = Wordle_Game(word_list_file=guess_file.name)
                won = False
                for word in guesses:
                        game.parse_guess(word.lower())
                        if game.game_won:
                                won = True
                self.assertTrue(won)

        def test_hard_mode_off(self):
            """
            Ensure that the game will work as intended when hard mode is not
                turned on. This is test_guess_score() with hard_mode=False
            """
            # "guess" must be non-empty to initialize the game, but it will
            # be ignored because we're calling _score_guess directly.
            guesses = ["hello"]
            answers = ["vivid"]
            expected = [
                            ["snack", "....."],
                            ["wordy", "...d."],
                            ["votes", "V...."],
                            ["irate", "i...."],
                            ["igigi", "i.i.."],
                            ["vitai", "VI..i"],
                            ["vidai", "VId.i"],
                            ["divid", ".IVID"],
                            ["viviv", "VIVI."],
                    ]

            guess_file = self.make_word_file(guesses)
            answer_file = self.make_word_file(answers)

            game = Wordle_Game(max_rounds=len(expected), word_list_file=guess_file.name, answer_list_file=answer_file.name, hard_mode=False)


            for guess, score in expected:
                    game.guesses.append(guess.upper())
                    self.assertEqual(score, game._score_guess())

        def test_hard_mode_on_good_guesses(self):
            """
            Ensure that hard mode allows guesses that include revealed letters
            """
            # "guess" must be non-empty to initialize the game, but it will
            # be ignored because we're calling _score_guess directly.
            guesses = ["hello"]
            answers = ["vivid"]
            expected = [
                            ["snack", "....."],
                            ["wordy", "...d."],
                            ["dotes", "d...."],
                            ["loved", "..V.D"],
                            ["david", "..VID"],
                            ["vavid", "V.VID"],
                            ["vivid", "VIVID"]
                    ]

            guess_file = self.make_word_file(guesses)
            answer_file = self.make_word_file(answers)

            game = Wordle_Game(max_rounds=len(expected), word_list_file=guess_file.name, answer_list_file=answer_file.name, hard_mode=True)

            for guess, score in expected:
                    game.guesses.append(guess.upper())
                    self.assertEqual(score, game._score_guess())

        def test_hard_mode_on_bad_guesses(self):
            """
            Ensure that hard mode disallows guesses that do not include revealed letters
            """
            # "guess" must be non-empty to initialize the game, but it will
            # be ignored because we're calling _score_guess directly.
            guesses = ["hello", "snack", "wordy", "simon", "vivid"]
            answers = ["vivid"]
            bad_guesses = [
                "snack", # reveals nothing, round_count now 1
                "wordy", # reveals d, round_count now 2
                "simon" # does not include a d, guess rejected, round_count still 2
            ]

            guess_file = self.make_word_file(guesses)
            answer_file = self.make_word_file(answers)

            game = Wordle_Game(max_rounds=len(bad_guesses), word_list_file=guess_file.name, answer_list_file=answer_file.name, hard_mode=True)

            for bg in bad_guesses:

                game.parse_guess(bg)

            self.assertEqual(game.round_counter, 2)

if __name__ == '__main__':
    unittest.main()
