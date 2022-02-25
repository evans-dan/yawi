yawi - Yet Another Wordle Implementation

# Overview
Like 63% of the devs on the planet, I decided to make a wordle clone. This is
the base class for the game itself.

Version 0.1 - the base game and a single Agent

# Release Notes
* v0.1 (2022-02-24)
  * modification of the base Wordle_Game class to hide some internal functions and attributes.
  * Addition of the base Wordle_Agent class as well as the first Agent built off of it, Wordle_Agent_LetterFreq.
  * Cleaned up some of the docstrings for classes and functions.

# Usage Example
```
# This will play one game of yawi

from Wordle_Game import Wordle_Game
wg = Wordle_Game()

from Wordle_Agent import Wordle_Agent
wa = Wordle_Agent(wg)

from Wordle_Agent_LetterFreq import Wordle_Agent_LetterFreq
walf = Wordle_Agent_LetterFreq(wg)

walf.play(wg)
```

# Future Development
- A "tournament" class that will allow for a series of games to be played by the same agent; pit two (or more?) agents head to head on the same word; or both.
- More and/or improved Agents that will play games with various approaches.
  - better first-word choice
  - position-aware letter frequency
  - di/tri-gram frequency
  - an ML-based approach that learns the rules
- implement "hard mode"
