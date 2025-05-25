import random

WHITEBOARD = ' '  
RANK = [4, 3, 2, 1]  # Ranking corresponds to points

class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position     
        self.hand = []               
        self.score = 0               
        self.hand_class = ()   # Store one round of card type information      

    def __repr__(self):
        return f"{self.name}(pos={self.position+1}, score={self.score})"   # Print players' information


def create_players():
    players = []
    seat = 0
    while seat < 4:
        name = input(f"Please enter the name of the {seat+1} player:")
        if name != "":
            players.append(Player(name, seat))   # Save player name and record current seat
            seat += 1
    return players


def create_wall():
    wall = [
        '1','1','1','1', 
        '2','2','2','2',
        '3','3','3','3', 
        '4','4','4','4',
        '5','5','5','5', 
        '6','6','6','6',
        '7','7','7','7', 
        '8','8','8','8',
        '9','9','9','9', 
        WHITEBOARD, WHITEBOARD, WHITEBOARD, WHITEBOARD
    ]    # Build card wall
    random.shuffle(wall) 
    return wall


def card_value(card):
    if card == WHITEBOARD:
        return 0.5     # Whiteboard scored 0.5 points
    else:
        return int(card)


def evaluate_hand(hand):
    a = hand[0]
    b = hand[1]
    va = card_value(a)
    vb = card_value(b)

    # The 28KANG is the largest card type
    if (va == 2 and vb == 8) or (va == 8 and vb == 2):
        return (4, 0, abs(va - vb))
    
    # pairs
    if va == vb:
        if a == WHITEBOARD:
            score = 10
        else:
            score = va
        return (3, score, 0)

    # Points
    total = va + vb
    true_point = total % 10
    if true_point != 0:
        category = 2
    else:
        category = 1
    return (category, true_point, abs(va - vb))


def compare_hand_class(h1, h2):
    # Compare card types according to the rules: 28KANG>pairs>points>0
    if h1[0] != h2[0]:
        return h1[0] < h2[0]  # Compare category
    if h1[1] != h2[1]:
        return h1[1] < h2[1]  # Compare main score
    return h1[2] < h2[2]      # Compare differnce


def deal_round(order, wall):
    i = 0
    while i < len(order):
        p = order[i]
        c1 = wall.pop(0)
        c2 = wall.pop(0)
        p.hand = [c1, c2]   # The player obtains two cards in hand
        p.hand_class = evaluate_hand(p.hand)   # Update card type
        i += 1


def assign_points(order):
    ranking = []
    i = 0
    while i < len(order):
        ranking.append(order[i])
        i += 1
    n = len(ranking)
    
    # Bubble sort
    i = 0
    while i < n:
        j = 0
        while j < n - i - 1:
            if compare_hand_class(ranking[j].hand_class, ranking[j+1].hand_class):
                ranking[j], ranking[j+1] = ranking[j+1], ranking[j]
            j += 1
        i += 1
    
    # The same card type earns the same score, take the higher value
    prev = None
    rank_index = -1
    k = 0
    while k < len(ranking):
        p = ranking[k]
        if prev is None or p.hand_class != prev:
            rank_index += 1
            prev = p.hand_class
        if rank_index < len(RANK):
            pts = RANK[rank_index]
        else:
            pts = RANK[-1]
        p.score += pts
        k += 1


def print_round(order, d1, d2, wall):

    print(f"Dice:{d1} + {d2} = {d1+d2}")

    print("This round hand:")
    pos = 1
    while pos <= len(order):
        p = order[pos-1]
        print(f"{pos}. {p.name}: {p.hand[0]} & {p.hand[1]}")
        pos += 1
    
    line = ""
    i = 0
    while i < len(order):
        entry = f"{order[i].name}={order[i].score}"
        if i == 0:
            line = entry
        else:
            line += " | " + entry
        i += 1

    print("SCORE:" + line)

    print("REST:" + str(len(wall)))


def sort_players_by_score(players):
    # Ranking in descending order of total score
    n = len(players)
    i = 0
    while i < n:
        max_index = i
        j = i + 1
        while j < n:
            if players[j].score > players[max_index].score:
                max_index = j
            j += 1
        if max_index != i:
            players[i], players[max_index] = players[max_index], players[i]
        i += 1


def main():
    # Create players and shuffle cards
    players = create_players()
    wall = create_wall()

    while True: # Control Loop
        # The number of dice determines the first player to get the cards
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        start = (d1 + d2) % 4
        # Construct a list of card issuance order
        order = []
        index = start
        count = 0
        while count < 4:
            order.append(players[index])
            if index < 3:
                index += 1
            else:
                index = 0
            count += 1
        # Deal, score, and output
        deal_round(order, wall)
        assign_points(order)
        print_round(order, d1, d2, wall)

        # If there are no remaining cards, the loop will automatically end
        if len(wall) == 0:
            print("There are not enough cards left to play another round of the game")
            break

        # At the end of each small wheel game, ask if you want to continue. If the answer is not yes, end the game immediately
        answer = input("Continue to next round?(yes/no):").lower()
        if answer != "yes":
            print("The game ended halfway.")
            break
    
    # Final ranking display
    print("Final Score Ranking:")
    sort_players_by_score(players)
    r = 1
    while r <= len(players):
        p = players[r-1]
        print(f"{r}. {p.name} — {p.score}")
        r += 1

if __name__ == "__main__":
    main()