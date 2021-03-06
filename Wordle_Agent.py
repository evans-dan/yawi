class Wordle_Agent:
    """
    Base class shared by all agents capable of playing the game implemented in
    Wordle_Game.
    """
    def __init__(self, game, debug=False):
        """
        Things shared by all Agents
        """
        self.debug = debug
        self.guesses = [] # list of guesses made
        self.results = [] # list of guess results/scores
        self.word_list = [] # the list of possible words
        self.word_length = 0 # the length of words in play
        self.correct_letters = [] # right letter in the right place
        self.included_letters = {} # right letter in the wrong place
        self.incorrect_letters = {} # letters not in the secret word
        self.outcome = None # whether the agent won or lost the game
        self._parse_game_settings(game) # grab the publicly available info from the game object

    def _parse_game_settings(self, game):
        """
        Copies game settings from the Wordle_Game object game.
        Inputs: a previously-instantiated Wordle_Game object
        Outputs: none; populates local attribute.
        """
        self.word_list = game.word_list
        self.word_length = game.word_length
        for i in range(game.word_length): # set up a list to hold correct letters
            self.correct_letters.append('-')

    def _record_guess_results(self, score):
        """
        Records the results of a guess for what letters are correct, included,
        and incorrect.
        Inputs: a score string from passing a guess to a Wordle_Game object.
        Outputs: none; changes local attributes.
        """
        if self.debug:
            print(f"Score was {self.results[-1]}", file=self.sys.stderr)
        results = list(self.results[-1])
        for i in range(len(results)): # for each score character
            letter = self.guesses[-1][i].upper()
            if results[i] == letter: # right letter, right place
                self.correct_letters[i] = letter
                results[i] = ' '
                # letter now properly placed, so remove it from included dict if the count reaches 0
                if letter in self.included_letters:
                    self.included_letters[letter] -= 1
                    if self.included_letters[letter] == 0:
                        del self.included_letters[letter]

        for i in range(len(results)): # for each score character
            letter = self.guesses[-1][i].upper()
            if results[i] == ' ':
                # Already handled.
                continue
            elif results[i] == letter.lower(): # right letter, wrong place
                self.included_letters.setdefault(letter, 0)
                self.included_letters[letter] += 1
                results[i] = ' '
            elif results[i] == '.': # letter is a miss
                # Wait for next pass.
                continue
            else: # wat
                raise ValueError("How did this happen?")

        for i in range(len(results)): # for each score character
            letter = self.guesses[-1][i].upper()
            if results[i] == ' ':
                # Already handled.
                continue
            elif results[i] == '.': # letter is a miss
                if not letter in self.correct_letters and not letter in self.included_letters:
                    self.incorrect_letters[letter] = 1
            else: # wat
                raise ValueError("How did this happen?")

    def play(self, game):
        """
        Plays the passed-in previously instantiated game found in a Wordle_Game
            object
        Inputs: a Wordle_Game object
        Outputs: messages; changes to local attributes
        """
        pass

    def __str__(self):
        """
        A human-friendly representation of the agent's state
        """
        return "Wordle Agent (incorrect letters=" + ','.join(self.incorrect_letters) + " included letters=" + ','.join(self.included_letters.keys()) + " correct letters=" + ''.join(self.correct_letters) + ")"
