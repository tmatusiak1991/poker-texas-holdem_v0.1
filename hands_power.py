from basic_deck import get_figures

def get_hands_rank(hand: int):
    hands_rank = {1: "High card", 2: "Pair",3: "Two pairs", 4: "Three", 5: "Straight", 6: "Flush", 7: "Full house", 8: "Four of", 9: "Straight flush", 10: "Royal flush"}
    highest_hand = hands_rank.get(hand)
    return highest_hand

def get_figures_power(hand: tuple):
    figures = get_figures()
    # el_1 = hand, e.g flush, straight etc.
    # el_2 = checking figures dict from basic_deck file to get card power, e.g. "power" of "A" = 14
    # el_3 -> same as above, but it is possible for some hans that there is no el_3, so for those "power" = 0
    el_1 = hand[0]
    el_2 = figures.get(hand[1])
    if hand[2] == 0:
        el_3 = 0
    else :
        el_3 = figures.get(hand[2])

    return (el_1, el_2, el_3)

def evaluate_hands_power(player_hand: tuple, computer_hand: tuple):
    player_hand_power = get_figures_power(player_hand)
    computer_hand_power = get_figures_power(computer_hand)
    # Evaluating power of hands to determine who won the round

    # if both tuples are equal, there is draw
    if player_hand_power == computer_hand_power:
        return "Draw"

    # Further checking of power, this can definitely be written better; to be changed in future version

    if player_hand_power[0] > computer_hand_power[0]:
        return "player_won"
    elif player_hand_power[0] < computer_hand_power[0]:
        return "computer_won"
    
    if player_hand_power[1] > computer_hand_power[1]:
        return "player_won"
    elif player_hand_power[1] < computer_hand_power[1]:
        return "computer_won"
    
    if player_hand_power[2] > computer_hand_power[2]:
        return "player_won"
    elif player_hand_power[2] < computer_hand_power[2]:
        return "computer_won"