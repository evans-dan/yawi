from Wordle_Game import Wordle_Game
wg = Wordle_Game(debug=True)
print(wg)
#help(wg)

from Wordle_Agent import Wordle_Agent
wa = Wordle_Agent(wg, debug=True)
print(wa)
#help(wa)

from Wordle_Agent_LetterFreq import Wordle_Agent_LetterFreq
walf = Wordle_Agent_LetterFreq(wg, debug=True)
print(walf)
#help(walf)

walf.play(wg)
