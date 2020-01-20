from random import sample, choice
import re

all_suits = ['clubs', 'diamonds', 'hearts', 'spades']
all_ranks = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

raise_regex = re.compile('raise (\d+)')

def get_raise_amount(string):
    return int(raise_regex.match(string).group(1))    

def get_hand_values(table, hands):
    return {player:get_hand_value(table + hands.get(player)) for player in hands.keys()}

def get_hand_value(hand):
    return 0

def get_flush(hand):
    for suit in all_suits:
        if 

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.name = '{} of {}'.format(self.rank, self.suit)

class Deck:
    def __init__(self):
        self.cards = []
        for suit in all_suits:
            for rank in all_ranks:
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
        while answer not in ['fold', option] and (raise_regex.match(answer) is None or get_raise_amount(string) < min(stakes.values())):
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
            self.stakes[p] = get_raise_amount(move)


    def play_round(self):
        if len(self.active_players) > 1:
            for p in self.active_players:
                move = p.get_move(self.table, self.hands.get(p), self.stakes)
                self.register_move(p,move)
            while not all(self.stakes.get(ap) == self.stakes.get(self.active_players[0]) for ap in self.active_players):
                for p in self.active_players:
                    move = p.get_move(self.table, self.hands.get(p), self.stakes)
                    self.register_move(p,move)

    def get_outcome(self):
        if len(self.active_players) == 1:
            print('{} wins, being the only active player'.format(self.active_players[0].name))
            winner = active_players[0]
        else:
            hands = get_hand_values(self.table, [p:h for p,h in self.hands.items() if p in self.active_players])


    def play(self):
        self.play_round()
        self.table.extend(self.deck.pull_cards(3))
        self.play_round()
        self.table.append(self.deck.pull_card())
        self.play_round()
        self.table.append(self.deck.pull_card())
        self.play_round()
        self.get_outcome()


p1 = Player('Lars', 100)
p2 = Player('Tim', 200)
g = Game([p1,p2])
g.play()
