import contextlib
import io
import unittest

from game_of_cards import Card, Deck, Game, Pile


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


class CardTests(unittest.TestCase):
    def test_rank_then_suit_ordering(self):
        self.assertLess(Card('9', 'S'), Card('T', 'C'))
        self.assertLess(Card('K', 'C'), Card('K', 'S'))
        self.assertEqual(Card('A', 'H'), Card('A', 'H'))
        self.assertNotEqual(Card('A', 'H'), Card('A', 'D'))

    def test_value_ignores_suit(self):
        self.assertEqual(Card('Q', 'C').value(), Card('Q', 'S').value())

    def test_invalid_card(self):
        with self.assertRaises(ValueError):
            Card('1', 'S')

    def test_readable_str(self):
        self.assertEqual(str(Card('T', 'H')), "10 of Hearts")


class DeckAndPileTests(unittest.TestCase):
    def test_deck_has_52_unique_cards(self):
        self.assertEqual(len(set(Deck().cards)), 52)

    def test_most_common_suit_tie_goes_to_higher_suit(self):
        pile = Pile([Card('2', 'C'), Card('3', 'S')])
        self.assertEqual(pile.most_common_suit(), 'S')
        self.assertIsNone(Pile().most_common_suit())

    def test_find_highest(self):
        pile = Pile([Card('A', 'C'), Card('A', 'S'), Card('K', 'S')])
        self.assertEqual(pile.find_highest(), Card('A', 'S'))


class GameTests(unittest.TestCase):
    def all_cards(self, g):
        return (g.player_draw_pile.cards + g.computer_draw_pile.cards
                + g.player_win_pile.cards + g.computer_win_pile.cards)

    def test_matching_ranks_start_a_war(self):
        g = Game(seed=0)
        g.player_draw_pile = Pile([Card('7', 'C')] + [Card(r, 'D') for r in '2345'])
        g.computer_draw_pile = Pile([Card('7', 'S')] + [Card(r, 'H') for r in '234A'])
        quiet(g.start_game, 1)
        self.assertEqual(g.computer_win_pile.pile_size(), 10)
        self.assertEqual(g.wars_won['c'], 1)

    def test_no_cards_lost_or_duplicated(self):
        for seed in range(2000):
            for rounds in (26, 500):
                g = Game(seed=seed)
                quiet(g.start_game, rounds)
                cards = self.all_cards(g)
                self.assertEqual(len(cards), 52, f"seed {seed}")
                self.assertEqual(len(set(cards)), 52, f"seed {seed}")

    def test_seed_is_repeatable(self):
        a, b = Game(seed=42), Game(seed=42)
        self.assertEqual(a.player_draw_pile.cards, b.player_draw_pile.cards)


if __name__ == "__main__":
    unittest.main()
