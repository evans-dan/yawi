from Wordle_Game import Wordle_Game
wg = Wordle_Game()
print(wg)
#help(wg)

from Wordle_Agent import Wordle_Agent
wa = Wordle_Agent(wg)
print(wa)
#help(wa)

from Wordle_Agent_LetterFreq import Wordle_Agent_LetterFreq
walf = Wordle_Agent_LetterFreq(wg)
print(walf)
#help(walf)

walf.play(wg)
