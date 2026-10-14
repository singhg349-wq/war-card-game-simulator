# Author - Gurshmeer Singh
"""War card game simulator: a player vs. the computer.

Usage:
    python3 game_of_cards.py                 # 26 rounds, random shuffle
    python3 game_of_cards.py --seed 7        # same game every time
    python3 game_of_cards.py --rounds 100
"""

import argparse
import random


class Card:
    Suits = {'C': 0, 'D': 1, 'H': 2, 'S': 3}
    Ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
             'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    SUIT_NAMES = {'C': 'Clubs', 'D': 'Diamonds', 'H': 'Hearts', 'S': 'Spades'}
    RANK_NAMES = {'T': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King', 'A': 'Ace'}

    def __init__(self, rank, suit):
        if rank not in self.Ranks or suit not in self.Suits:
            raise ValueError("Invalid rank or suit")
        self.rank = rank
        self.suit = suit

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def value(self):
        """Rank value only (2-14). War rounds are decided on this; suits don't count."""
        return self.Ranks[self.rank]

    def __repr__(self):
        return f"Card(rank='{self.rank}',suit='{self.suit}')"

    def __str__(self):
        return f"{self.RANK_NAMES.get(self.rank, self.rank)} of {self.SUIT_NAMES[self.suit]}"

    # Full ordering: rank first, suit as the tiebreaker. Used for sorting and
    # for finding the highest card in a pile.
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        if self.rank == other.rank:
            return self.Suits[self.suit] < self.Suits[other.suit]
        return self.Ranks[self.rank] < self.Ranks[other.rank]

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.rank, self.suit))


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Card.Ranks for suit in Card.Suits]

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"Deck({self.cards})"

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

    def shuffle(self, rng=random):
        rng.shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop(0)
        return None


class Pile:
    def __init__(self, cards=None):
        self.cards = list(cards) if cards else []

    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)
        return None

    def add_cards(self, cards):
        if not isinstance(cards, list):
            cards = [cards]
        self.cards += cards

    def pile_size(self):
        return len(self.cards)

    def find_highest(self):
        return max(self.cards) if self.cards else None

    def most_common_suit(self):
        """Suit that appears most often. Ties go to the higher suit (S > H > D > C)."""
        if not self.cards:
            return None
        counts = {}
        for card in self.cards:
            counts[card.suit] = counts.get(card.suit, 0) + 1
        return max(counts, key=lambda suit: (counts[suit], Card.Suits[suit]))

    def get_pile(self):
        return self.cards

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)


class Game:
    def __init__(self, seed=None):
        deck = Deck()
        deck.shuffle(random.Random(seed))
        self.player_draw_pile = Pile(deck.cards[:26])
        self.computer_draw_pile = Pile(deck.cards[26:])
        self.player_win_pile = Pile()
        self.computer_win_pile = Pile()
        self.wars_won = {'p': 0, 'c': 0}

    def start_game(self, rounds):
        for _ in range(rounds):
            if not self.player_draw_pile.pile_size() or not self.computer_draw_pile.pile_size():
                break
            p_card = self.player_draw_pile.draw_card()
            c_card = self.computer_draw_pile.draw_card()
            print(f"Player plays {p_card}, Computer plays {c_card}")

            if p_card.value() > c_card.value():
                self.player_win_pile.add_cards([p_card, c_card])
            elif p_card.value() < c_card.value():
                self.computer_win_pile.add_cards([p_card, c_card])
            else:
                print("  Same rank: WAR!")
                self.go_to_war([p_card, c_card])

    def go_to_war(self, pot):
        """Each side burns three cards and plays a fourth; higher rank takes the whole pot.

        The pot alternates player, computer, player, computer, ... so it can be
        handed back fairly if neither side can afford the war.
        """
        p_can = self.player_draw_pile.pile_size() >= 4
        c_can = self.computer_draw_pile.pile_size() >= 4
        if not (p_can and c_can):
            if p_can:      # computer can't keep going, so it forfeits the pot
                self._award(pot, 'p')
            elif c_can:    # player can't keep going
                self._award(pot, 'c')
            else:          # nobody can: each side gets back the cards it put in
                self.player_win_pile.add_cards(pot[0::2])
                self.computer_win_pile.add_cards(pot[1::2])
                print("  Neither side has enough cards for war; cards returned.")
            return

        for _ in range(3):  # burn three cards each
            pot.append(self.player_draw_pile.draw_card())
            pot.append(self.computer_draw_pile.draw_card())

        p_face = self.player_draw_pile.draw_card()
        c_face = self.computer_draw_pile.draw_card()
        pot.extend([p_face, c_face])
        print(f"  War face-off: Player {p_face}, Computer {c_face} (pot: {len(pot)} cards)")

        if p_face.value() > c_face.value():
            self._award(pot, 'p')
        elif p_face.value() < c_face.value():
            self._award(pot, 'c')
        else:
            print("  Tied again: another WAR!")
            self.go_to_war(pot)

    def _award(self, pot, side):
        pile = self.player_win_pile if side == 'p' else self.computer_win_pile
        pile.add_cards(pot)
        self.wars_won[side] += 1
        print(f"  {'Player' if side == 'p' else 'Computer'} wins the war and takes {len(pot)} cards")

    def print_winner(self):
        p, c = self.player_win_pile.pile_size(), self.computer_win_pile.pile_size()
        if p > c:
            print("Player wins!")
            return "p"
        if c > p:
            print("Computer wins!")
            return "c"
        print("It's a tie!")
        return "t"

    def summary(self, result):
        names = {'p': 'Player', 'c': 'Computer', 't': 'Tie'}
        print(f"Game Over! Winner: {names[result]}")
        print(f"Cards won - Player: {self.player_win_pile.pile_size()}, "
              f"Computer: {self.computer_win_pile.pile_size()}")
        print(f"Wars won - Player: {self.wars_won['p']}, Computer: {self.wars_won['c']}")
        print(f"Player's highest card: {self.player_win_pile.find_highest()}")
        suit = self.player_win_pile.most_common_suit()
        print(f"Player's most common suit: {Card.SUIT_NAMES.get(suit, 'None')}")
        print(f"Player's win pile: {self.player_win_pile}")


def main():
    parser = argparse.ArgumentParser(description="Play a game of War: player vs. computer.")
    parser.add_argument("--rounds", type=int, default=26, help="maximum rounds (default 26)")
    parser.add_argument("--seed", type=int, help="shuffle seed, for a repeatable game")
    args = parser.parse_args()

    game = Game(seed=args.seed)
    game.start_game(args.rounds)
    game.summary(game.print_winner())


if __name__ == "__main__":
    main()
