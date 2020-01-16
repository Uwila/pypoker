from random import sample, choice
import re

raise_regex = re.compile('raise (\d+)')


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.name = '{} of {}'.format(self.rank, self.suit)

class Deck:
    def __init__(self):
        self.cards = []
        for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
            for rank in ['ace', '2', '3', '4', '5', '6', '7',
                         '8', '9', '10', 'jack', 'queen', 'king']:
                self.cards.append(Card(suit,rank))

    def pull_card(self):
        c = choice(self.cards)
        self.cards.remove(c)
        return c

    def pull_cards(self, amount):
        return [self.pull_card() for _ in range(amount)]

class Player:
    def __init__(self, name, money=100):
        self.money = money
        self.name = name

    def get_move(self, table, hand, stakes):
        option = 'check' if stakes.get(self) == max(stakes.values()) else 'match'

        print('{}, your cards are {}, the cards on the table are {}, your stake is {} and the other stakes are {}. You can "fold", "{}" or raise'\
              .format(
                  self.name,
                  ', '.join(c.name for c in hand),
                  ', '.join(c.name for c in table),
                  stakes.get(self),
                  ', '.join('{} with {}'.format(p.name, stakes.get(p)) for p in stakes.keys() if p is not self),
                  option,
              )
        )

        answer = ''
        # TODO: Do not allow raises downwards
        while answer not in ['fold', option] and raise_regex.match(answer) is None:
            answer = input('Type: "fold", "{}", or "raise [to amount]"'.format(option))
        return answer

class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.active_players = players
        self.table = []
        self.hands = {player: self.deck.pull_cards(2) for player in players}
        self.stakes = {player: 0 for player in players}
        self.max_stake = 0


    def register_move(self, player, move):
        p = player # TODO: Clean this up

        if move == 'fold':
            self.active_players.remove(p)
        elif move == 'match':
            self.stakes[p] = max(self.stakes.values())
        elif move != 'check':
            self.stakes[p] = int(raise_regex.match(move).group(1))


    def play_round(self):
        if len(self.active_players) > 1:
            for p in self.active_players:
                move = p.get_move(self.table, self.hands.get(p), self.stakes)
                self.register_move(p,move)
            while not all(self.stakes.get(ap) == self.stakes.get(self.active_players[0]) for ap in self.active_players):
                for p in self.active_players:
                    move = p.get_move(self.table, self.hands.get(p), self.stakes)
                    self.register_move(p,move)


    def play(self):
        self.play_round()
        self.table.extend(self.deck.pull_cards(3))
        self.play_round()
        self.table.append(self.deck.pull_card())
        self.play_round()
        self.table.append(self.deck.pull_card())
        self.play_round()


p1 = Player('Lars', 100)
p2 = Player('Tim', 200)
g = Game([p1,p2])
