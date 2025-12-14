
Memory Card Game - Project Write up


Overview

This basic memory card game (concentration/matching pairs) was created in Python with the tkinter graphical user interface. The game shuffles the deck, reads distinct card labels (words) from a text file (cards.txt), duplicates them to create pairs, and displays them in a 4x4 grid.  The player attempts to match pairings after clicking cards to disclose the text.

Why I selected this project

A memory game is a single-file project that, while still being doable within the project's time limits, can illustrate numerous programming concepts needed for the course..

How the project meets the course requirements

- Loops: `for` loops used to create widgets, iterate files, and process data.
- Variables: uses strings, numbers, lists, and tuples throughout.
- Functions: separated functionality into methods and functions.
- Processing Data: reads card words from `cards.txt`, writes scores to `scores.csv`.
- Graphics: GUI implemented with `tkinter`.
- Exception Handling: file I/O and parsing are surrounded by try/except blocks with user-friendly messages.
- Classes: includes `Card` and `MemoryGame` classes.
- GUI: uses `tkinter` for the user interface.

Files included

- memory_game.py      -> Main program
- cards.txt           -> Sample card words (one per line)
- scores.csv          -> Scores file (CSV), initially with header
- README.txt          -> This file
- flowchart.png       -> Simple flowchart of the program logic

Pseudocode / Algorithm

1. Read unique words from cards.txt.
2. Verify there are enough unique words to fill half the board.
3. Duplicate the list so every word appears twice.
4. Shuffle the combined list.
5. Create a grid of Card objects (buttons) using tkinter.
6. On user click:
   - If it's the first card, reveal it.
   - If it's the second card, reveal it and check match:
       - If match: mark both as matched and disable them.
       - Else: hide both after a short delay.
   - Increment move counter and update the timer display.
7. When all pairs matched, prompt the user to save score and show win message.
8. Scores are appended to scores.csv in CSV format.

Possible Enhancements

- Support variable board sizes selected by the user (e.g., 2x4, 4x4, 6x6).
- Add images instead of words (load image files listed in cards.txt).
- Add sound effects on match/miss.
- Improve styling and animations.

Challenges anticipated

- Ensuring images scale correctly if images used.
- Handling various sizes of cards file (too few or too many entries).
- Cross-platform differences in tkinter fonts/appearance.

