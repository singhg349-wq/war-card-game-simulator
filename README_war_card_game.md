# War Card Game Simulator

A Python implementation of the classic card game War, played between a simulated player and computer. Includes a full object-oriented card/deck/pile model with overloaded comparison operators, so cards can be compared directly with `<`, `>`, and `==` just like numbers.

## What it does

A standard 52-card deck is shuffled and split evenly between the player and computer. Each round, both sides play their top card — whoever plays the higher-ranked card wins both cards and adds them to their win pile. A tie triggers "war": both sides burn three cards into the pot and play one more card face-off, with the winner taking the entire pot (including the burned cards). Ties during a war escalate recursively, growing the pot until someone wins it. The game ends after a fixed number of rounds or when either side runs out of cards to draw, and the winner is whoever accumulated more cards.

## Features

- Full `Card` class with rank/suit comparison logic (`2`–`10`, `J`, `Q`, `K`, `A`, across `C`/`D`/`H`/`S`), including tie-breaking by suit
- `Deck` class that builds and shuffles a complete 52-card deck
- `Pile` class shared by both draw piles and win piles, supporting drawing, adding cards, finding the highest card, and finding the most common suit
- Recursive "war" resolution that correctly escalates through repeated ties
- End-of-game summary: winner, each side's win pile size, the player's highest card won, and their most common suit won

## Running

```
python3 game_of_cards.py
```

Runs a full 26-round game automatically and prints each round as it's played — no arguments needed.

## Example output

During play, each round prints as it's resolved:
```
Player plays Card(rank='2',suit='S'), Computer plays Card(rank='T',suit='S')
Player plays Card(rank='5',suit='D'), Computer plays Card(rank='7',suit='S')
...
Computer wins!
```

End-of-game summary:
```
Game Over! Winner: Computer
Peace offerings - Player: 0, Computer: 0
Player's highest card: Card(rank='A',suit='S')
Player's most common suit: None
Player's win pile: Card(rank='5',suit='S'),Card(rank='5',suit='H'),...
```

## Design notes

- **Operator overloading for game logic**: `Card` implements `__lt__`, `__le__`, `__gt__`, `__ge__`, `__eq__`, and `__ne__`, comparing by rank first and suit as a tiebreaker. This means `Pile.find_highest()` and the round-comparison logic in `Game` never need special-case comparison code — they just use plain `>`/`<` and let the `Card` class define what "higher" means.

- **Recursive war resolution**: rather than using a loop with manually tracked state, `go_to_war` calls itself again when the face-off is also a tie, passing along the same growing `pot` list. Each recursive call adds three more burned cards plus a new face-off pair, so a chain of consecutive ties naturally builds one larger pot instead of needing separate bookkeeping for "how many times have we gone to war."

- **War requires at least 4 cards**: before burning cards, `go_to_war` checks that both draw piles have at least 4 cards left. If a side doesn't, the function returns without resolving that round — a documented edge case rather than a crash, though it does mean the pot from an unresolved war isn't added to either win pile, so those specific cards don't end up counted in the final result.

- **`peace_offerings` is tracked but not yet used**: the `Game` class keeps a `peace_offerings` counter for each side and prints it in the summary, but no code currently increments it — it's a hook for a rule that isn't implemented in this version, which is why it always prints `0` for both sides.

## Author

Gurshmeer Singh
