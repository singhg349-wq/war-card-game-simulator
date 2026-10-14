# War Card Game Simulator

![tests](https://github.com/singhg349-wq/war-card-game-simulator/actions/workflows/tests.yml/badge.svg)

The classic card game War in object-oriented Python, played between a player and the computer. Cards, decks and piles are modelled as classes, and `Card` overloads the comparison operators, so cards can be compared and sorted with `<`, `>` and `==` like numbers.

## How the game works

A shuffled 52-card deck is split evenly between the player and the computer. Each round, both sides play their top card, and the higher **rank** takes both cards into its win pile. If the ranks match, it's **war**: each side burns three cards face down and plays a fourth, and the higher rank takes the whole pot. A tie during a war starts another war on top of the same pot, so the pot keeps growing until someone wins it.

If one side doesn't have enough cards left for a war, it forfeits the pot to the other side. If neither side does, each gets back the cards it put in. No card is ever lost: the tests check that all 52 cards are accounted for at the end of every game.

The game ends after a set number of rounds (26 by default) or when a draw pile runs out. Whoever has won more cards wins.

## Running

```bash
python3 game_of_cards.py              # random game
python3 game_of_cards.py --seed 3     # the same game every time
python3 game_of_cards.py --rounds 100
```

Only the standard library is needed (Python 3.8+).

## Example output

```
$ python3 game_of_cards.py --seed 3
Player plays 5 of Diamonds, Computer plays Queen of Diamonds
Player plays 9 of Clubs, Computer plays 8 of Spades
...
Player plays Jack of Clubs, Computer plays Jack of Spades
  Same rank: WAR!
  War face-off: Player 4 of Spades, Computer 6 of Clubs (pot: 10 cards)
  Computer wins the war and takes 10 cards
...
Computer wins!
Game Over! Winner: Computer
Cards won - Player: 22, Computer: 30
Wars won - Player: 0, Computer: 1
Player's highest card: Ace of Spades
Player's most common suit: Clubs
Player's win pile: 9 of Clubs, 8 of Spades, 9 of Diamonds, ...
```

## Design notes

- **Operator overloading with a full ordering:** `Card` implements `__lt__`, `__le__`, `__gt__`, `__ge__`, `__eq__`, `__ne__` and `__hash__`, comparing by rank first and suit as a tiebreaker (Clubs < Diamonds < Hearts < Spades). That gives every card a unique position, so `max()` and `sorted()` work directly on piles. Rounds, though, are decided by `Card.value()`, which is rank only, because in War two cards of the same rank are a tie.
- **Recursive war resolution:** `go_to_war` calls itself when the face-off ties again, passing the same growing `pot` list. A chain of ties builds one larger pot with no separate bookkeeping.
- **Fair pot handling:** cards go into the pot in player, computer, player, computer order. If neither side can afford a war, `pot[0::2]` and `pot[1::2]` hand each side back exactly the cards it put in.
- **Repeatable games:** the shuffle uses `random.Random(seed)`, so `--seed` reproduces a game exactly. The tests rely on this.
- **Most common suit:** ties go to the higher suit, so a non-empty pile always reports a suit.

## Tests

```bash
python3 -m unittest -v
```

`test_game.py` checks card comparisons, that matching ranks start a war, that all 52 cards survive thousands of seeded games, and the pile helpers. The tests run automatically on every push through GitHub Actions.

## License

MIT

## Author

Gurshmeer Singh
