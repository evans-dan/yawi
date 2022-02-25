from Wordle_Agent import Wordle_Agent
class Wordle_Agent_LetterFreq(Wordle_Agent):
    """
    An agent to play Wordle, which extends the Wordle_Agent class.
    This agent will attempt to calculate the next guess based on the frequency
    of letters in the word list.
    """
    import re
    def __init__(self, game):
        """
        Augment the base class for this type of Agent
        Inputs: a Wordle_Game object
        Outputs: None. Modifies local attributes.
        """
        super().__init__(game) # instantiate the base class
        self.letter_counts = {} # position independent letter counts
        self.letter_freqs = {}  # position independent letter frequencies
        self.remaining_word_scores = {} # the remaining words and their scores. Starts full and will be reduced
        self._start_setup() # perform setup based on the available information

    def _start_setup(self):
        """
        Execute setup steps before making the first guess.
        Inputs: none.
        Outputs: none.
        """
        # initialize to zero, then calculate
        for w in self.word_list:
            self.remaining_word_scores[w] = 0

        self._calculate_letter_freqs() # calculate letter frequencies from words in the word list
        self._calculate_word_freq_scores() # calculate a score for each word in the list

    def _build_match_regex(self):
        """
        Build a regex pattern object that will match words that follow the
            rules of what we know about included and correct letters.
        Inputs: none; reads local attributes
        Outputs: a compiled re object.
        """
        patt_str = ''

        for i in range(self.word_length): # build an appropriately long regex from what is known

            if self.correct_letters[i] != '-': # a correctly placed letter so fix it in the regex

                patt_str += self.correct_letters[i]

            else: # include absence information (i.e., a returned lower case N means we can toss any word with an N in that position)

                without_patt = '' # a string to hold letters that are NOT in a particular position
                for j in range(len(self.guesses)):

                    # the guessed letter isn't in this position so add it to the regex pattern
                    if self.results[j][i] == '.' or self.results[j][i] == self.results[j][i].lower():

                        without_patt += self.guesses[j][i].upper()

                if without_patt != '': # add the pattern of letters not included in this position

                    patt_str += "[^{0}]".format(without_patt)

                else: # can match any letter

                    patt_str += "."

        return self.re.compile(patt_str)

    def _calculate_letter_freqs(self):
        """
        Calculate position-independent letter frequencies from the words in
            the word list parsed from the game object.
        Inputs: none.
        Outputs. None. Changes local attributes.
        """

        # reset counter dicts
        self.letter_counts = {}
        self.letter_freqs = {}

        for w in self.remaining_word_scores.keys(): # for each remaining word

            for i in range(self.word_length): # for each position

                if w[i] not in self.letter_counts: # initialize the letter

                    self.letter_counts[w[i]] = 0

                self.letter_counts[w[i]] += 1 # count an occurrence of this letter

        lowest_count_letter = min(self.letter_counts, key=lambda key: self.letter_counts[key])
        # use this to normalize the scores to be a multiple of the least frequent letter
        # i.e., if Q is the least frequent letter, frequency of Q = 1, and E ~= 55.

        for l in self.letter_counts.keys(): # turn counts into frequencies normalized to the lowest value
            self.letter_freqs[l] = self.letter_counts[l] / self.letter_counts[lowest_count_letter]

    def _calculate_word_freq_scores(self):
        """
        Calculate the letter frequency scores for each word remaining in the
            remaining word dict.
        Inputs: None.
        Outputs: none. Modifies local attributes.
        """
        for w in self.remaining_word_scores.keys():
            self.remaining_word_scores[w] = self._score_word(w)

    def _reduce_remaining_word_scores(self):
        """
        Reduce the remaining_word_scores dict given what we have learned through
            the scoring strings returned from the game object.
        Inputs: none.
        Outputs: none. Modifies local attributes.
        """

        to_remove = [] # words to remove from the dict
        correct_patt = '' # a pattern of letters in the correct places
        base_patt = self.re.compile('[^\-]')

        correct_patt = self._build_match_regex()

        for w in self.remaining_word_scores.keys(): # for each remaining guessable word

            # least stringent test: does the word contain an included letter?

            has_included_letter = True # edge case of first guess having no overlap with the secret word
            if (len(self.included_letters.keys()) > 0):
                has_included_letter = False

                for i in self.included_letters.keys():

                    if i in w:  # we have a hit so keep the word

                        has_included_letter = True

            # more stringent: does the letter match the pattern of correct letters?

            matches_regex = True

            if self.re.match(correct_patt, w) is None: # no match object = no _build_match_regex

                matches_regex = False

            # most stringent: does the word contain a banned letter?

            no_incorrect_letters = True
            for i in self.incorrect_letters.keys():

                if i in w:

                    no_incorrect_letters = False

            # do we keep this word or not?
            if (has_included_letter is True) and (matches_regex is True) and (no_incorrect_letters is True):

                keep_word = True

            else:

                keep_word = False
                to_remove.append(w)

        for r in to_remove: # drop all the removed words
            del self.remaining_word_scores[r]

    def _score_word(self, word):
        """
        calculate the frequency-based score for a word.
        Inputs: a word.
        Outputs: a float.
        """
        return sum([self.letter_freqs[l] for l in word])

    def _get_best_scoring_word(self):
        """
        Return the word with the highest letterfreq score
        Inputs: none.
        Outputs: the word with the highest score in the remaining_word_scores
            list.
        """
        return max(self.remaining_word_scores, key=lambda key: self.remaining_word_scores[key])

    def play(self, game):
        """
        Play the Wordle game from the passed-in Wordle_Game object.
        The agent will play the game autonomously to its conclusion.
        Inputs: a Wordle_Game object
        Outputs: changes local attributes, prints messages
        """
        while game.game_won is None: # until win or loss

            # set up the letter frequencies and word scores based on the current word list
            self._calculate_letter_freqs() # calculate letter frequencies from words in the word list
            self._calculate_word_freq_scores() # calculate a score for each word in the list

            # choose the best starting word
            best_word = self._get_best_scoring_word()

            # submit our current best guess and remove from further consideration
            game.parse_guess(best_word)
            del self.remaining_word_scores[best_word]

            # parse the returned score
            self.guesses.append(best_word)
            self.results.append(game.messages[-1])
            self._record_guess_results(self.results[-1])

            # reduce the wordlist based on the score
            self._reduce_remaining_word_scores()

        self.outcome = game.game_won

        for i in range(len(self.guesses)):
            print("Round {0}: guess: {1} score {2}".format(i+1, self.guesses[i], self.results[i]))

        if self.outcome is True:

            print("Game won.")

        else:

            print("Game lost.")

    def __str__(self):
        """
        A human-friendly representation of the agent's state.
        """
        return "Wordle LetterFreq Agent (incorrect letters=" + ','.join(self.incorrect_letters.keys()) + " included letters=" + ','.join(self.included_letters.keys()) + " correct letters=" + ''.join(self.correct_letters) + ")"
