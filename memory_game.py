
"""
memory_game.py
A simple Memory Card Game with a tkinter GUI that reads card labels (words) from a text file.
Features:
- Reads unique card words from cards.txt, duplicates them to make pairs, shuffles, and lays them out in a grid.
- Uses classes (Card, MemoryGame).
- Uses loops, lists, tuples, dictionaries, functions.
- Saves high scores (moves + time) to scores.csv.
- Exception handling for file errors.
- GUI built with tkinter (graphics).
Run: python3 memory_game.py
Requires: Python 3.x (tkinter standard library)
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import random
import time
import csv
import os

CARDS_FILE = "cards.txt"
SCORES_FILE = "scores.csv"

class Card:
    """Represents a single card in the memory game."""
    def __init__(self, master, text, command):
        self.master = master
        self.text = text            # word shown when flipped
        self.is_revealed = False
        self.is_matched = False
        self.button = tk.Button(master, text="", width=12, height=6,
                                command=command, font=("Helvetica", 10, "bold"))
    def reveal(self):
        if not self.is_revealed and not self.is_matched:
            self.button.config(text=self.text, state="disabled")
            self.is_revealed = True
    def hide(self):
        if not self.is_matched:
            self.button.config(text="", state="normal")
            self.is_revealed = False
    def match(self):
        self.is_matched = True
        self.button.config(relief="sunken", bg="#d9f2d9")  # subtle visual for matched

class MemoryGame:
    """Main game class managing state, GUI, and game logic."""
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Card Game - Words from File")
        self.root.resizable(False, False)
        self.cards = []             # list of Card objects
        self.first_card = None
        self.second_card = None
        self.locked = False         # prevents clicks while checking
        self.moves = 0
        self.matches = 0
        self.start_time = None
        self.elapsed_time = 0
        self.grid_size = (4, 4)     # rows, cols -> default 4x4 (16 cards)
        self.setup_ui()

        # Try to load card words and start game
        try:
            words = self.load_card_words(CARDS_FILE)
            self.start_new_game(words)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load cards: {e}")

    def setup_ui(self):
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.grid(row=0, column=0, sticky="ew")

        self.info_label = tk.Label(control_frame, text="Moves: 0    Time: 0s", font=("Helvetica", 12))
        self.info_label.grid(row=0, column=0, padx=5)

        new_btn = tk.Button(control_frame, text="Restart", command=self.restart, width=10)
        new_btn.grid(row=0, column=1, padx=5)

        load_btn = tk.Button(control_frame, text="Load Cards File", command=self.choose_cards_file, width=15)
        load_btn.grid(row=0, column=2, padx=5)

        save_btn = tk.Button(control_frame, text="Save Score", command=self.save_score_prompt, width=10)
        save_btn.grid(row=0, column=3, padx=5)

        high_btn = tk.Button(control_frame, text="View High Scores", command=self.show_high_scores, width=15)
        high_btn.grid(row=0, column=4, padx=5)

        board_frame = tk.Frame(self.root, padx=10, pady=10)
        board_frame.grid(row=1, column=0)
        self.board_frame = board_frame

    def load_card_words(self, filename):
        """Reads unique card words from a text file (one word/phrase per line).
        Returns a list of words. Raises exception on problems."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"'{filename}' not found in current directory.")
        words = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    words.append(line)
        unique_words = list(dict.fromkeys(words))  # preserve order and remove duplicates
        # Ensure there are enough words to fill grid (grid_size total / 2)
        needed_pairs = (self.grid_size[0] * self.grid_size[1]) // 2
        if len(unique_words) < needed_pairs:
            raise ValueError(f"Not enough unique words in {filename}. Need {needed_pairs}, found {len(unique_words)}.")
        return unique_words[:needed_pairs]

    def start_new_game(self, words):
        """Initialize and display a new shuffled board using the given list of unique words."""
        # Reset state
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        self.cards.clear()
        self.first_card = None
        self.second_card = None
        self.moves = 0
        self.matches = 0
        self.locked = False
        self.start_time = time.time()
        self.update_info_label()

        # Prepare the deck: duplicate each word to create pairs, shuffle
        deck = []
        for w in words:
            deck.append(w)
            deck.append(w)
        random.shuffle(deck)

        rows, cols = self.grid_size
        # Create Card objects and place them in a grid
        idx = 0
        for r in range(rows):
            for c in range(cols):
                word = deck[idx]
                card = Card(self.board_frame, word, command=lambda i=idx: self.on_card_click(i))
                card.button.grid(row=r, column=c, padx=5, pady=5)
                self.cards.append(card)
                idx += 1

    def on_card_click(self, index):
        """Handle user clicking a card."""
        if self.locked:
            return
        card = self.cards[index]
        if card.is_revealed or card.is_matched:
            return
        card.reveal()

        if self.first_card is None:
            self.first_card = (index, card)
            return
        else:
            self.second_card = (index, card)
            self.locked = True
            # Check match after a short delay to allow user to see second card
            self.root.after(600, self.check_for_match)

    def check_for_match(self):
        """Compare the two selected cards, update game state."""
        i1, c1 = self.first_card
        i2, c2 = self.second_card
        if c1.text == c2.text:
            c1.match()
            c2.match()
            self.matches += 1
        else:
            # Not a match: hide both
            c1.hide()
            c2.hide()
        self.moves += 1
        self.first_card = None
        self.second_card = None
        self.locked = False
        self.update_info_label()

        # Check for win
        total_pairs = (self.grid_size[0] * self.grid_size[1]) // 2
        if self.matches >= total_pairs:
            self.elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("You win!", f"You matched all pairs!\nMoves: {self.moves}\nTime: {self.elapsed_time} seconds")
            # Optionally prompt to save score
            self.save_score_prompt(win=True)

    def update_info_label(self):
        """Update moves and timer info label."""
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
        else:
            elapsed = 0
        self.info_label.config(text=f"Moves: {self.moves}    Time: {elapsed}s")

    def restart(self):
        """Restart with the same cards file (simple restart)."""
        try:
            words = self.load_card_words(CARDS_FILE)
            self.start_new_game(words)
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't restart: {e}")

    def choose_cards_file(self):
        """Let user pick a different cards file; then restart game with it."""
        fname = filedialog.askopenfilename(title="Choose cards file", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if fname:
            try:
                # Copy chosen file to working CARDS_FILE path by reading and writing
                with open(fname, "r", encoding="utf-8") as src:
                    content = src.read()
                with open(CARDS_FILE, "w", encoding="utf-8") as dst:
                    dst.write(content)
                words = self.load_card_words(CARDS_FILE)
                self.start_new_game(words)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load selected file: {e}")

    def save_score_prompt(self, win=False):
        """Prompt the player to enter their name and save the score to CSV."""
        if self.matches == 0 and not win:
            messagebox.showinfo("No score", "No matches yet to save.")
            return
        name = simpledialog.askstring("Save score", "Enter your name (or initials):")
        if not name:
            return
        elapsed = int(time.time() - self.start_time) if self.start_time else 0
        try:
            self.append_score_csv(name, self.moves, elapsed)
            messagebox.showinfo("Saved", "Score saved to scores.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save score: {e}")

    def append_score_csv(self, name, moves, seconds):
        """Append a score row to SCORES_FILE. Creates file with headers if missing."""
        header = ["name","moves","time_seconds"]
        file_exists = os.path.exists(SCORES_FILE)
        with open(SCORES_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow([name, moves, seconds])

    def show_high_scores(self):
        """Read scores.csv and show top 10 by fewest moves, then fastest time as tiebreaker."""
        if not os.path.exists(SCORES_FILE):
            messagebox.showinfo("No scores", "No scores recorded yet.")
            return
        try:
            rows = []
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        rows.append((r["name"], int(r["moves"]), int(r["time_seconds"])))
                    except Exception:
                        continue
            if not rows:
                messagebox.showinfo("No scores", "No valid scores in the file.")
                return
            # sort by moves asc, then time asc
            rows.sort(key=lambda x: (x[1], x[2]))
            display = "Top scores:\n"
            for i, (n, m, t) in enumerate(rows[:10], start=1):
                display += f"{i}. {n} — Moves: {m}, Time: {t}s\n"
            messagebox.showinfo("High Scores", display)
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't read scores: {e}")

def main():
    # Ensure cards file exists in current directory; if not, create a sample one
    if not os.path.exists(CARDS_FILE):
        sample = ["Apple","Banana","Cherry","Dog","Elephant","Flower","Guitar","House"]
        with open(CARDS_FILE, "w", encoding="utf-8") as f:
            for word in sample:
                f.write(word + "\n")
    root = tk.Tk()
    game = MemoryGame(root)
    # Update timer every second
    def timer_tick():
        game.update_info_label()
        root.after(1000, timer_tick)
    root.after(1000, timer_tick)
    root.mainloop()

if __name__ == "__main__":
    main()
