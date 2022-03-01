class Wordle_Benchmark:
    """
    A class to run a series of Wordle Games with a single Wordle_Agent. It will
        implement either repeated tests of a single agent. Envisioned uses
        include being a way to measure the effect of algorithm changes within
        an Agent.
    Inputs: the name of a class that implements a Wordle Game (e.g.
        Wordle_Game, the default); the name of a class that can play the game
        in the passed-in game class (e.g. Wordle_Agent_LetterFreq, the
        default); a number of rounds (default = 500).
    Outputs: a report on the outcomes of the requested number of games in one
        of several output formats (default: text).
    """
    import sys
    from Wordle_Game import Wordle_Game
    from Wordle_Agent_LetterFreq import Wordle_Agent_LetterFreq

    def __init__(self, game_class=Wordle_Game, agent_class=Wordle_Agent_LetterFreq, rounds=100, output_format='text', debug=False):
        """
        Initiate the Wordle_Benchmark object
        """

        self.debug=debug # control debugging output
        self.valid_output_formats=['text']
        self.game_class = game_class
        self.agent_class = agent_class
        self.default_rounds = 100
        self.default_output_format = 'text'
        self.game_counter = 0 # number of games completed

        if isinstance(rounds, int) and rounds > 0: # sanity check the rounds argument value
            self.rounds = rounds
        else:
            self.rounds = self.default_rounds

        if output_format in self.valid_output_formats: # sanity check the output_format value
            self.output_format = output_format
        else:
            self.output_format = self.default_output_format

        self.benchmark_result_order = [1,2,3,4,5,6,'X'] # default display_order of results
        self.benchmark_histogram = {} # will be keyed by end round number, with X=failure

        for r in self.benchmark_result_order: # initialize allowed values
            self.benchmark_histogram[r] = 0

    def start_benchmark(self, verbose=False):
        """
        Performs the benchmark.
        Inputs: verbose (default =False) controls whether or not to print
            progress messages
        Outputs: the results of the benchmarking.
        """

        for i in range(self.rounds): # start benchmarking
            wg = self.game_class()
            wa = self.agent_class(wg)
            wa.play(wg)
            if wg.game_won is True: # count a win by the round number

                #if wg.round_counter not in self.benchmark_histogram.keys(): # initialize outcome value
                #    self.benchmark_histogram[wg.round_counter] = 0

                self.benchmark_histogram[wg.round_counter] += 1

            else: # it's a loss
                #if 'X' not in self.benchmark_histogram.keys(): # initialize outcome value
                #    self.benchmark_histogram['X'] = 0

                self.benchmark_histogram['X'] += 1

            if verbose is True or self.debug: # print out some progress metrics for the users. They get twitchy otherwise.

                if (i+1) % 25 == 0:
                    print(f"Round {i+1} complete", file=self.sys.stderr)

        self.output_benchmark_report()

    def output_benchmark_report(self):
        """
        Create the benchmark report in the requested format
        Inputs: none.
        Outputs: a report in the requested format.
        """

        if self.output_format.lower() == 'text': # make a text report

            if self.debug:
                print("In Wordle_Benchmark.output_benchmark_report(), requesting a text report", file=self.sys.stderr)

            self._create_text_benchmark_report()

        else: # whaa? Should have caught this error, so do this by default

            if self.debug:
                print(f"WARNING: uncaught bad argument in Wordle_Benchmark.output_benchmark_report(). output_format argument {self.output_format} not a valid choice. Defaulting to text.", file=self.sys.stderr)

            self._create_text_benchmark_report()

    def _create_text_benchmark_report(self):
        """
        Create a text-based benchmark report.
        Inputs: none.
        Outputs: a textual report of the results.
        """
        if self.debug:
            print(f"In Wordle_Benchmark._create_text_benchmark_report(): creating a text report", file=self.sys.stderr)

        report = 'Benchmark Report\n'
        report += '================\n'
        report += 'Round   Wins\n'
        report += '------------\n'

        for round in self.benchmark_result_order:
            report += f"{round:<5}{self.benchmark_histogram[round]:>7}\n"

        print(report)

    def __str__(self):
        """
        Print out the benchmark parameters.
        Inputs: none.
        Outputs: string representation of the benchmark object
        """

        report = f"Wordle Benchmark (rounds={self.rounds}"
        report += f", game class={str(self.game_class)}"
        report += f", agent class={str(self.agent_class)}"
        report += f", output format={self.output_format}"
        report += ")"

        return report
